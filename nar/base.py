"""

"""

import sys
from functools import wraps
from collections import defaultdict
import logging
from six import with_metaclass
from .errors import ResourceExistsError


logger = logging.getLogger("nar")


registry = {
    'names': {},
    'types': {}
}

# todo: add namespaces to avoid name clashes, e.g. "Person" exists in several namespaces
def register_class(target_class):
    registry['names'][target_class.__name__] = target_class
    if hasattr(target_class, 'type'):
        registry['types'][tuple(target_class.type)] = target_class


def lookup(class_name):
    return registry['names'][class_name]


def lookup_type(class_type):
    return registry['types'][tuple(class_type)]


def generate_cache_key(qd):
    """From a query dict, generate an object suitable as a key for caching"""
    cache_key = []
    for key in sorted(qd):
        value = qd[key]
        if isinstance(value, (list, tuple)):
            sub_key = []
            for sub_value in value:
                sub_key.append(generate_cache_key(sub_value))
            cache_key.append(tuple(sub_key))
        else:
            assert isinstance(value, (str, int, float))
            cache_key.append((key, value))
    return tuple(cache_key)


class Registry(type):
    """Metaclass for registering Knowledge Graph classes"""

    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)
        return cls


#class KGObject(object, metaclass=Registry):
class KGObject(with_metaclass(Registry, object)):
    """Base class for Knowledge Graph objects"""
    cache = {}
    save_cache = defaultdict(dict)

    def __init__(self, id=None, instance=None, **properties):
        for key, value in properties.items():
            if key not in self.property_names:
                raise TypeError("{self.__class__.__name__} got an unexpected keyword argument '{key}'".format(self=self, key=key))
            else:
                setattr(self, key, value)
        self.id = id
        self.instance = instance

    def __repr__(self):
        return ('{self.__class__.__name__}('
                '{self.name!r} {self.id!r})'.format(self=self))

    @classmethod
    def from_kg_instance(self, instance, client, use_cache=True):
        raise NotImplementedError("To be implemented by child class")

    @classmethod
    def from_uri(cls, uri, client, use_cache=True):
        return cls.from_kg_instance(client.instance_from_full_uri(uri, use_cache=use_cache),
                                    client,
                                    use_cache=use_cache)

    @classmethod
    def from_uuid(cls, uuid, client):
        if len(uuid) == 0:
            raise ValueError("Empty UUID")
        # todo: better checking of UUID format
        instance = client.instance_from_uuid(cls.path, uuid)
        if instance is None:
            return None
        else:
            return cls.from_kg_instance(instance, client)

    @property
    def uuid(self):
        return self.id.split("/")[-1]

    @classmethod
    def list(cls, client, size=100, **filters):
        """List all objects of this type in the Knowledge Graph"""
        return client.list(cls, size=size)

    @property
    def _existence_query(self):
        # Note that this default implementation should in
        # many cases be over-ridden.
        # It assumes that "name" is unique within instances of a given type,
        # which may often not be the case.
        return {
            "path": "schema:name",
            "op": "eq",
            "value": self.name
        }

    def exists(self, client):
        """Check if this object already exists in the KnowledgeGraph"""
        if self.id:
            return True
        else:
            context = {"schema": "http://schema.org/",
                       "prov": "http://www.w3.org/ns/prov#"},
            query_filter = self._existence_query
            query_cache_key = generate_cache_key(query_filter)
            if query_cache_key in self.save_cache[self.__class__]:
                # Because the KnowledgeGraph is only eventually consistent, an instance
                # that has just been written to Nexus may not appear in the query.
                # Therefore we cache the query when creating an instance and
                # where exists() returns True
                self.id = self.save_cache[self.__class__][query_cache_key]
                return True
            else:
                response = client.filter_query(self.path, query_filter, context)
                if response:
                    self.id = response[0].data["@id"]
                    KGObject.save_cache[self.__class__][query_cache_key] = self.id
                return bool(response)

    def _save(self, data, client, exists_ok=True):
        """docstring"""
        if self.id:
            # instance.data should be identical to data at this point
            self.instance = client.update_instance(self.instance)
            logger.info("Updating {self.instance.id}".format(self=self))
        else:
            if self.exists(client):
                if exists_ok:
                    logger.info("Not updating {self.__class__.__name__}, already exists (id={self.id})".format(self=self))
                    return
                else:
                    raise ResourceExistsError("Already exists in the Knowledge Graph: {self!r}".format(self=self))
            instance = client.create_new_instance(self.__class__.path, data)
            self.id = instance.data["@id"]
            self.instance = instance
            KGObject.cache[self.id] = self
            KGObject.save_cache[self.__class__][generate_cache_key(self._existence_query)] = self.id

    def delete(self, client):
        """Deprecate"""
        client.delete_instance(self.instance)

    @classmethod
    def by_name(cls, name, client):
        return client.by_name(cls, name)

    @property
    def rev(self):
        if self.instance:
            return self.instance.data.get("nxv:rev", None)
        else:
            return None

    def resolve(self, client):
        """To avoid having to check if a child attribute is a proxy or a real object,
        a real object resolves to itself.
        """
        return self


def cache(f):
    @wraps(f)
    def wrapper(cls, instance, client, use_cache=True):
        if use_cache and instance.data["@id"] in KGObject.cache:
            obj = KGObject.cache[instance.data["@id"]]
            #print(f"Found in cache: {obj.id}")
            return obj
        else:
            obj = f(cls, instance, client)
            KGObject.cache[obj.id] = obj
            #print(f"Added to cache: {obj.id}")
            return obj
    return wrapper


class OntologyTerm(object):
    """docstring"""

    def __init__(self, label, iri=None, strict=False):
        self.label = label
        self.iri = iri or self.iri_map.get(label)
        if strict:
            if self.iri is None:
                raise ValueError("No IRI found for label {}".format(label))

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.label!r}, {self.iri!r})')
        return ('{self.__class__.__name__}('
                '{self.label!r}, {self.iri!r})'.format(self=self))

    def to_jsonld(self):
        return {'@id': self.iri,
                'label': self.label}

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        return cls(data["label"], data["@id"])


class KGProxy(object):
    """docstring"""

    def __init__(self, cls, uri):
        if isinstance(cls, str):
            self.cls = lookup(cls)
        else:
            self.cls = cls
        self.id = uri

    @property
    def type(self):
        return self.cls.type

    def resolve(self, client):
        """docstring"""
        if self.id in KGObject.cache:
            return KGObject.cache[self.id]
        else:
            obj = self.cls.from_uri(self.id, client)
            KGObject.cache[self.id] = obj
            return obj

    def __repr__(self):
        #return (f'{self.__class__.__name__}('
        #        f'{self.cls!r}, {self.id!r})')
        return ('{self.__class__.__name__}('
                '{self.cls!r}, {self.id!r})'.format(self=self))

    def delete(self, client):
        """Delete the instance which this proxy represents"""
        obj = self.resolve(client)
        obj.delete(client)


class KGQuery(object):
    """docstring"""

    def __init__(self, cls, filter, context):
        if isinstance(cls, str):
            self.cls = lookup(cls)
        else:
            self.cls = cls
        self.filter = filter
        self.context = context

    def resolve(self, client):
        instances = client.filter_query(
            path=self.cls.path,
            filter=self.filter,
            context=self.context,
            size=10000
        )
        objects = [self.cls.from_kg_instance(instance, client)
                   for instance in instances]
        for obj in objects:
            KGObject.cache[obj.id] = obj
        if len(instances) == 1:
            return objects[0]
        else:
            return objects


class Distribution(object):

    def __init__(self, location, size=None, digest=None, digest_method=None, content_type=None,
                 original_file_name=None):
        self.location = location
        self.size = size
        self.digest = digest
        self.digest_method = digest_method
        self.content_type = content_type
        self.original_file_name = original_file_name

    @classmethod
    def from_jsonld(cls, data):
        if data is None:
            return None
        if "contentSize" in data:
            size = data["contentSize"]["value"]
            if data["contentSize"]["unit"] != "byte":
                raise NotImplementedError()
        else:
            size = None
        if "digest" in data:
            digest = data["digest"]["value"]
            digest_method = data["digest"]["algorithm"]
        else:
            digest = None
            digest_method = None
        return cls(data["downloadURL"], size, digest, digest_method, data.get("mediaType"),
                   data.get("originalFileName"))

    def to_jsonld(self):
        data = {
            "@context": "https://nexus-int.humanbrainproject.org/v0/contexts/nexus/core/distribution/v0.1.0",  # todo: needs to adapt to Nexus instance
            "downloadURL": self.location
        }
        if self.size:
            data["contentSize"] = {
                "unit": "byte",
                "value": self.size
            }
        if self.digest:
            data["digest"]= {
                "algorithm": self.digest_method,  # e.g. "SHA-256"
                "value": self.digest
            },
        if self.content_type:
            data["mediaType"] = self.content_type
        if self.original_file_name:  # not sure if this is part of the schema, or just an annotation
            data["originalFileName"] = self.original_file_name
        return data


def build_kg_object(cls, data):
    """
    Build a KGObject, a KGProxy, or a list of such, based on the data provided.

    This takes care of the JSON-LD quirk that you get a list if there are multiple
    objects, but you get the object directly if there is only one.

    Returns `None` if data is None.
    """

    if data is None:
        return None

    if not isinstance(data, list):
        if not isinstance(data, dict):
            raise ValueError("data must be a list or dict")
        if "@list" in data:
            assert len(data) == 1
            data = data["@list"]
        else:
            data = [data]

    objects = []
    for item in data:
        if cls is None:
            cls = lookup_type(item["@type"])

        if issubclass(cls, OntologyTerm):
            obj = cls.from_jsonld(item)
        elif issubclass(cls, KGObject):
            obj = KGProxy(cls, item["@id"])
        elif cls is Distribution:
            obj = cls.from_jsonld(item)
        else:
            raise ValueError("cls must be a KGObject, OntologyTerm or Distribution")
        objects.append(obj)

    if len(objects) == 1:
        return objects[0]
    else:
        return objects


def as_list(obj):
    if obj is None:
        return []
    try:
        L = list(obj)
    except TypeError:
        L = [obj]
    return L
