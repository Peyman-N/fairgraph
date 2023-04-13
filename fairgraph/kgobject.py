"""

"""

# Copyright 2018-2020 CNRS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from collections import defaultdict
import logging
from uuid import UUID
from warnings import warn
from typing import Any, Tuple, Dict, List, Optional, TYPE_CHECKING, Union

from requests.exceptions import HTTPError

try:
    from tabulate import tabulate

    have_tabulate = True
except ImportError:
    have_tabulate = False
from .utility import expand_uri, as_list, ActivityLog
from .registry import lookup_type
from .queries import Query
from .errors import AuthorizationError, ResourceExistsError
from .caching import object_cache, save_cache, generate_cache_key
from .base import RepresentsSingleObject, ContainsMetadata, SupportsQuerying, IRI, JSONdict
from .kgproxy import KGProxy

if TYPE_CHECKING:
    from .fields import Field
    from .client import KGClient


logger = logging.getLogger("fairgraph")


def get_filter_value(filters: Dict[str, Any], field: Field) -> Union[str, List[str]]:
    value = filters[field.name]

    def is_valid(val):
        return isinstance(val, (IRI, UUID, *field.types)) or (isinstance(val, KGProxy) and val.cls in field.types)

    if isinstance(value, list) and len(value) > 0:
        valid_type = all(is_valid(item) for item in value)
        have_multiple = True
    else:
        valid_type = is_valid(value)
        have_multiple = False
    if not valid_type:
        if field.name == "hash":  # bit of a hack
            filter_value = value
        elif isinstance(value, str) and value.startswith("http"):  # for @id
            filter_value = value
        else:
            raise TypeError("{} must be of type {}, not {}".format(field.name, field.types, type(value)))
    filter_items = []
    for item in as_list(value):
        if isinstance(item, IRI):
            filter_item = item.value
        elif hasattr(item, "id"):
            filter_item = item.id
        elif isinstance(item, UUID):
            # todo: consider using client.uri_from_uuid()
            # would require passing client as arg
            filter_item = f"https://kg.ebrains.eu/api/instances/{item}"
        elif isinstance(item, str) and "+" in item:  # workaround for KG bug
            invalid_char_index = item.index("+")
            if invalid_char_index < 3:
                raise ValueError(f"Cannot use {item} as filter, contains invalid characters")
            filter_item = item[:invalid_char_index]
            warn(f"Truncating filter value {item} --> {filter_item}")
        else:
            filter_item = item
        filter_items.append(filter_item)
    if have_multiple:
        return filter_items
    else:
        return filter_items[0]


class KGObject(ContainsMetadata, RepresentsSingleObject, SupportsQuerying):
    """Base class for Knowledge Graph objects"""

    fields: List[Field] = []
    existence_query_fields: Tuple[str, ...] = ("name",)
    # Note that this default value of existence_query_fields should in
    # many cases be over-ridden.
    # It assumes that "name" is unique within instances of a given type,
    # which may often not be the case.

    def __init__(
        self,
        id: Optional[str] = None,
        data: Optional[JSONdict] = None,
        space: Optional[str] = None,
        scope: Optional[str] = None,
        **properties,
    ):
        self.id = id
        self._space = space
        self.scope = scope
        self.allow_update = True
        super().__init__(data=data, **properties)

    def __repr__(self):
        template_parts = (
            "{}={{self.{}!r}}".format(field.name, field.name)
            for field in self.fields
            if getattr(self, field.name) is not None
        )
        template = "{self.__class__.__name__}(" + ", ".join(template_parts) + ", space={self.space}, id={self.id})"
        return template.format(self=self)

    @property
    def space(self) -> Union[str, None]:
        if self._raw_remote_data:
            if "https://schema.hbp.eu/myQuery/space" in self._raw_remote_data:
                self._space = self._raw_remote_data["https://schema.hbp.eu/myQuery/space"]
            elif "https://core.kg.ebrains.eu/vocab/meta/space" in self._raw_remote_data:
                self._space = self._raw_remote_data["https://core.kg.ebrains.eu/vocab/meta/space"]
        return self._space

    @classmethod
    def from_kg_instance(cls, data: JSONdict, client: KGClient, scope: Optional[str] = None):
        deserialized_data = cls._deserialize_data(data, client, include_id=True)
        return cls(id=data["@id"], data=data, scope=scope, **deserialized_data)

    # @classmethod
    # def _fix_keys(cls, data):
    #     """
    #     The KG Query API does not allow the same field name to be used twice in a document.
    #     This is a problem when resolving linked nodes which use the same field names
    #     as the 'parent'. As a workaround, we prefix the field names in the linked node
    #     with the class name.
    #     This method removes this prefix.
    #     This feels like a kludge, and I'd be happy to find a better solution.
    #     """
    #     prefix = cls.__name__ + "__"
    #     for key in list(data):
    #         # need to use list() in previous line to avoid
    #         # "dictionary keys changed during iteration" error in Python 3.8+
    #         if key.startswith(prefix):
    #             fixed_key = key.replace(prefix, "")
    #             data[fixed_key] = data.pop(key)
    #     return data

    @classmethod
    def from_uri(
        cls,
        uri: str,
        client: KGClient,
        use_cache: bool = True,
        scope: str = "released",
        follow_links: int = 0,
    ):
        if follow_links:
            query = cls._get_query_definition(client, normalized_filters={}, space=None, follow_links=follow_links)
            results = client.query({}, query, instance_id=client.uuid_from_uri(uri), size=1, scope=scope).data
            if results:
                data = results[0]
                data["@context"] = cls.context
            else:
                data = None
        else:
            data = client.instance_from_full_uri(uri, use_cache=use_cache, scope=scope)
        if data is None:
            return None
        else:
            return cls.from_kg_instance(data, client, scope=scope)

    @classmethod
    def from_uuid(
        cls,
        uuid: str,
        client: KGClient,
        use_cache: bool = True,
        scope: str = "released",
        follow_links: int = 0,
    ):
        logger.info("Attempting to retrieve {} with uuid {}".format(cls.__name__, uuid))
        if len(uuid) == 0:
            raise ValueError("Empty UUID")
        try:
            val = UUID(uuid, version=4)  # check validity of uuid
        except ValueError as err:
            raise ValueError("{} - {}".format(err, uuid))
        uri = cls.uri_from_uuid(uuid, client)
        return cls.from_uri(uri, client, use_cache=use_cache, scope=scope, follow_links=follow_links)

    @classmethod
    def from_id(
        cls,
        id: str,
        client: KGClient,
        use_cache: bool = True,
        scope: str = "released",
        follow_links: int = 0,
    ):
        if hasattr(cls, "type_") and cls.type_:
            if id.startswith("http"):
                return cls.from_uri(id, client, use_cache=use_cache, scope=scope, follow_links=follow_links)
            else:
                return cls.from_uuid(id, client, use_cache=use_cache, scope=scope, follow_links=follow_links)
        else:
            if id.startswith("http"):
                uri = id
            else:
                uri = client.uri_from_uuid(id)
            if follow_links > 0:
                raise NotImplementedError
            data = client.instance_from_full_uri(uri, use_cache=use_cache, scope=scope)
            cls_from_data = lookup_type(data["@type"])
            return cls_from_data.from_kg_instance(data, client, scope=scope)

    @classmethod
    def from_alias(
        cls,
        alias: str,
        client: KGClient,
        space: Optional[str] = None,
        scope: str = "released",
        follow_links: int = 0,
    ):
        if "alias" not in cls.field_names:
            raise AttributeError(f"{cls.__name__} doesn't have an 'alias' field")
        candidates = as_list(
            cls.list(
                client,
                size=20,
                from_index=0,
                api="query",
                scope=scope,
                space=space,
                alias=alias,
                follow_links=follow_links,
            )
        )
        if len(candidates) == 0:
            return None
        elif len(candidates) == 1:
            return candidates[0]
        else:  # KG query does a "contains" lookup, so can get multiple results
            for candidate in candidates:
                if candidate.alias == alias:
                    return candidate
            warn(
                "Multiple objects found with a similar alias, but none match exactly." "Returning the first one found."
            )
            return candidates[0]

    @property
    def uuid(self) -> Union[str, None]:
        # todo: consider using client._kg_client.uuid_from_absolute_id
        if self.id is not None:
            return self.id.split("/")[-1]
        else:
            return None

    @classmethod
    def uri_from_uuid(cls, uuid: str, client: KGClient) -> str:
        return client.uri_from_uuid(uuid)

    @classmethod
    def _get_query_definition(
        cls,
        client: KGClient,
        normalized_filters: Union[Dict[str, Any], None],
        space: Optional[str] = None,
        follow_links: int = 0,
        use_stored_query: bool = False,
    ):
        if follow_links:
            query_type = f"resolved-{follow_links}"
        else:
            query_type = "simple"
        if normalized_filters is None:
            filter_keys = None
        else:
            filter_keys = list(normalized_filters.keys())
        query = None
        if use_stored_query:
            query_label = cls.get_query_label(query_type, space, filter_keys)
            query = client.retrieve_query(query_label)
        if query is None:
            query = cls.generate_query(
                query_type,
                space,
                client=client,
                filter_keys=filter_keys,
                follow_links=follow_links,
            )
            if use_stored_query:
                client.store_query(query_label, query, space=space)
        return query

    @classmethod
    def normalize_filter(cls, filter_dict: Dict[str, Any]) -> Dict[str, Any]:
        filter_queries = {}
        for field in cls.fields:
            if field.name in filter_dict:
                filter_queries[field.name] = get_filter_value(filter_dict, field)
        return filter_queries

    @classmethod
    def list(
        cls,
        client: KGClient,
        size: int = 100,
        from_index: int = 0,
        api: str = "auto",
        scope: str = "released",
        space: Optional[str] = None,
        follow_links: int = 0,
        **filters,
    ) -> List[KGObject]:
        """List all objects of this type in the Knowledge Graph"""

        if api == "auto":
            if filters:
                api = "query"
            else:
                api = "core"

        if api == "query":
            normalized_filters = cls.normalize_filter(filters) or None
            query = cls._get_query_definition(client, normalized_filters, space, follow_links=follow_links)
            instances = client.query(
                normalized_filters,
                query,
                space=space,
                from_index=from_index,
                size=size,
                scope=scope,
            ).data
            for instance in instances:
                instance["@context"] = cls.context
        elif api == "core":
            if filters:
                raise ValueError("Cannot use filters with api='core'")
            if follow_links:
                raise NotImplementedError("Following links with api='core' not yet implemented")
            instances = client.list(cls.type_, space=space, from_index=from_index, size=size, scope=scope).data
        else:
            raise ValueError("'api' must be either 'query', 'core', or 'auto'")

        return [cls.from_kg_instance(instance, client, scope=scope) for instance in instances]

    @classmethod
    def count(
        cls,
        client: KGClient,
        api: str = "auto",
        scope: str = "released",
        space: Optional[str] = None,
        **filters,
    ) -> int:
        if api == "auto":
            if filters:
                api = "query"
            else:
                api = "core"
        if api == "query":
            normalized_filters = cls.normalize_filter(filters) or None
            query = cls._get_query_definition(client, normalized_filters, space)
            response = client.query(normalized_filters, query, space=space, from_index=0, size=1, scope=scope)
        elif api == "core":
            if filters:
                raise ValueError("Cannot use filters with api='core'")
            response = client.list(cls.type_, space=space, scope=scope, from_index=0, size=1)
        return response.total

    def _build_existence_query(self) -> Union[None, Dict[str, Any]]:
        if self.existence_query_fields is None:
            return None

        query_fields = []
        for field_name in self.existence_query_fields:
            for field in self.fields:
                if field.name == field_name:
                    query_fields.append(field)
                    break
        if len(query_fields) < 1:
            raise Exception("Empty existence query for class {}".format(self.__class__.__name__))
        query = {}
        for field in query_fields:
            value = field.serialize(getattr(self, field.name), follow_links=False)
            if isinstance(value, dict) and "@id" in value:
                value = value["@id"]
            query[field.name] = value
        return query

    def _update_empty_fields(self, data: JSONdict, client: KGClient):
        """Replace any empty fields (value None) with the supplied data"""
        cls = self.__class__
        deserialized_data = cls._deserialize_data(data, client, include_id=True)
        for field in cls.fields:
            current_value = getattr(self, field.name, None)
            if current_value is None:
                value = deserialized_data[field.name]
                setattr(self, field.name, value)
        assert self.remote_data is not None
        for key, value in data.items():
            expanded_path = expand_uri(key, cls.context)
            assert isinstance(expanded_path, str)
            self.remote_data[expanded_path] = data[key]

    def __eq__(self, other):
        return not self.__ne__(other)

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return True
        if self.id and other.id and self.id != other.id:
            return True
        for field in self.fields:
            val_self = getattr(self, field.name)
            val_other = getattr(other, field.name)
            if val_self != val_other:
                return True
        return False

    def diff(self, other):
        differences = defaultdict(dict)
        if not isinstance(other, self.__class__):
            differences["type"] = (self.__class__, other.__class__)
        else:
            if self.id != other.id:
                differences["id"] = (self.id, other.id)
            for field in self.fields:
                val_self = getattr(self, field.name)
                val_other = getattr(other, field.name)
                if val_self != val_other:
                    differences["fields"][field.name] = (val_self, val_other)
        return differences

    def exists(self, client: KGClient) -> bool:
        """Check if this object already exists in the KnowledgeGraph"""

        if self.id:
            # Since the KG now allows user-specified IDs we can't assume that the presence of
            # an id means the object exists
            data = client.instance_from_full_uri(
                self.id, use_cache=True, scope=self.scope or "any", require_full_data=False
            )
            if self._raw_remote_data is None:
                self._raw_remote_data = data
            obj_exists = bool(data)
            if obj_exists:
                self._update_empty_fields(data, client)  # also updates `remote_data`
            return obj_exists
        else:
            query_filter = self._build_existence_query()

            if query_filter is None:
                # if there's no existence query and no ID, we allow
                # duplicate entries
                return False
            else:
                try:
                    query_cache_key = generate_cache_key(query_filter)
                except TypeError as err:
                    raise TypeError(f"Error in generating cache key for {self.__class__.__name__} object: {err}")
                if query_cache_key in save_cache[self.__class__]:
                    # Because the KnowledgeGraph is only eventually consistent, an instance
                    # that has just been written to the KG may not appear in the query.
                    # Therefore we cache the query when creating an instance and
                    # where exists() returns True
                    self.id = save_cache[self.__class__][query_cache_key]
                    cached_obj = object_cache.get(self.id)
                    if cached_obj and cached_obj.remote_data:
                        self._raw_remote_data = cached_obj._raw_remote_data
                        self.remote_data = cached_obj.remote_data  # copy or update needed?
                    return True

                normalized_filters = self.__class__.normalize_filter(query_filter) or None
                query = self.__class__._get_query_definition(client, normalized_filters)
                instances = client.query(normalized_filters, query, size=1, scope="any").data

                if instances:
                    self.id = instances[0]["@id"]
                    assert isinstance(self.id, str)
                    save_cache[self.__class__][query_cache_key] = self.id
                    self._update_empty_fields(instances[0], client)  # also updates `remote_data`
                return bool(instances)

    def modified_data(self) -> JSONdict:
        current_data = self.to_jsonld(include_empty_fields=True, follow_links=False)
        modified_data = {}
        for key, current_value in current_data.items():
            if not key.startswith("@"):
                assert key.startswith("http")  # keys should all be expanded by this point
                assert self.remote_data is not None
                remote_value = self.remote_data.get(key, None)
                if current_value != remote_value:
                    modified_data[key] = current_value
        return modified_data

    def save(
        self,
        client: KGClient,
        space: Optional[str] = None,
        recursive: bool = True,
        activity_log: Optional[ActivityLog] = None,
        replace: bool = False,
        ignore_auth_errors: bool = False,
    ):
        if recursive:
            for field in self.fields:
                if field.intrinsic:
                    values = getattr(self, field.name)
                    for value in as_list(values):
                        if isinstance(value, ContainsMetadata):
                            target_space: Optional[str]
                            if value.space:
                                target_space = value.space
                            elif (
                                isinstance(value, KGObject)
                                and value.__class__.default_space == "controlled"
                                and value.exists(client)
                                and value.space == "controlled"
                            ):
                                continue
                            elif space is None and self.space is not None:
                                target_space = self.space
                            else:
                                target_space = space
                            if target_space == "controlled":
                                assert isinstance(value, KGObject)  # for type checking
                                if value.exists(client) and value.space == "controlled":
                                    continue
                                else:
                                    raise Exception("Cannot write to controlled space")
                            value.save(
                                client,
                                space=target_space,
                                recursive=True,
                                activity_log=activity_log,
                            )
        if space is None:
            if self.space is None:
                space = self.__class__.default_space
            else:
                space = self.space
        logger.info(f"Saving a {self.__class__.__name__} in space {space}")
        if self.exists(client):
            if not self.allow_update:
                logger.info(f"  - not updating {self.__class__.__name__}(id={self.id}), update not allowed by user")
                if activity_log:
                    activity_log.update(item=self, delta=None, space=space, entry_type="no-op")
            else:
                # update
                local_data = self.to_jsonld()
                if replace:
                    logger.info(f"  - replacing - {self.__class__.__name__}(id={self.id})")
                    if activity_log:
                        activity_log.update(item=self, delta=local_data, space=space, entry_type="replacement")
                    try:
                        client.replace_instance(self.uuid, local_data)
                        # what does this return? Can we use it to update `remote_data`?
                    except AuthorizationError as err:
                        if ignore_auth_errors:
                            logger.error(str(err))
                        else:
                            raise
                    else:
                        self.remote_data = local_data
                else:
                    modified_data = self.modified_data()
                    if modified_data:
                        logger.info(
                            f"  - updating - {self.__class__.__name__}(id={self.id}) - fields changed: {modified_data.keys()}"
                        )
                        skip_update = False
                        if "vocab:storageSize" in modified_data:
                            warn("Removing storage size from update because this field is currently locked by the KG")
                            modified_data.pop("vocab:storageSize")
                            skip_update = len(modified_data) == 0

                        if skip_update:
                            if activity_log:
                                activity_log.update(item=self, delta=None, space=space, entry_type="no-op")
                        else:
                            try:
                                client.update_instance(self.uuid, modified_data)
                            except AuthorizationError as err:
                                if ignore_auth_errors:
                                    logger.error(str(err))
                                else:
                                    raise
                            else:
                                self.remote_data = local_data
                            if activity_log:
                                activity_log.update(
                                    item=self,
                                    delta=modified_data,
                                    space=space,
                                    entry_type="update",
                                )
                    else:
                        logger.info(f"  - not updating {self.__class__.__name__}(id={self.id}), unchanged")
                        if activity_log:
                            activity_log.update(item=self, delta=None, space=space, entry_type="no-op")
        else:
            # create new
            local_data = self.to_jsonld()
            logger.info("  - creating instance with data {}".format(local_data))
            try:
                instance_data = client.create_new_instance(
                    local_data, space or self.__class__.default_space, instance_id=self.uuid
                )
            except (AuthorizationError, ResourceExistsError) as err:
                if ignore_auth_errors:
                    logger.error(str(err))
                    if activity_log:
                        activity_log.update(
                            item=self,
                            delta=local_data,
                            space=self.space,
                            entry_type="create-error",
                        )
                else:
                    raise
            else:
                self.id = instance_data["@id"]
                self._raw_remote_data = instance_data
                self.remote_data = local_data
                if activity_log:
                    activity_log.update(item=self, delta=instance_data, space=self.space, entry_type="create")
        # not handled yet: save existing object to new space - requires changing uuid
        if self.id:
            logger.debug("Updating cache for object {}. Current state: {}".format(self.id, self.to_jsonld()))
            object_cache[self.id] = self
        else:
            logger.warning("Object has no id - see log for the underlying error")

    def delete(self, client: KGClient, ignore_not_found: bool = True):
        """Deprecate"""
        client.delete_instance(self.uuid, ignore_not_found=ignore_not_found)
        if self.id in object_cache:
            object_cache.pop(self.id)

    @classmethod
    def by_name(
        cls,
        name: str,
        client: KGClient,
        match: str = "equals",
        all: bool = False,
        space: Optional[str] = None,
        scope: str = "released",
        follow_links: int = 0,
    ) -> Union[KGObject, List[KGObject], None]:
        objects = cls.list(client, space=space, scope=scope, api="query", name=name, follow_links=follow_links)
        if match == "equals":
            objects = [obj for obj in objects if hasattr(obj, "name") and obj.name == name]
        if len(objects) == 0:
            return None
        elif len(objects) == 1:
            return objects[0]
        elif all:
            return objects
        else:
            warn("Multiple objects with the same name, returning the first. " "Use 'all=True' to retrieve them all")
            return objects[0]

    def show(self, max_width: Optional[int] = None):
        if not have_tabulate:
            raise Exception("You need to install the tabulate module to use the `show()` method")
        data = [("id", self.id), ("space", self.space)] + [
            (field.name, str(getattr(self, field.name, None))) for field in self.fields
        ]
        if max_width:
            value_column_width = max_width - max(len(item[0]) for item in data)

            def fit_column(value):
                strv = value
                if len(strv) > value_column_width:
                    strv = strv[: value_column_width - 4] + " ..."
                return strv

            data = [(k, fit_column(v)) for k, v in data]
        print(tabulate(data, tablefmt="plain"))
        # return tabulate(data, tablefmt='html') - also see  https://bitbucket.org/astanin/python-tabulate/issues/57/html-class-options-for-tables

    @classmethod
    def generate_query(
        cls,
        query_type: str,
        space: Union[str, None],
        client: KGClient,
        filter_keys: Optional[List[str]] = None,
        follow_links: int = 0,
    ) -> Union[Dict[str, Any], None]:
        """

        query_type: "simple" or "resolved-n"
        """

        query_label = cls.get_query_label(query_type, space, filter_keys)
        if space == "myspace":
            real_space = client._private_space
        else:
            real_space = space
        query = Query(
            node_type=cls.type_[0],
            label=query_label,
            space=real_space,
            properties=cls.generate_query_properties(filter_keys, follow_links=follow_links),
        )
        return query.serialize()

    @classmethod
    def get_query_label(cls, query_type: str, space: Union[str, None], filter_keys: Optional[List[str]] = None) -> str:
        if space and "private" in space:  # temporary work-around
            label = f"fg-{cls.__name__}-{query_type}-myspace"
        else:
            label = f"fg-{cls.__name__}-{query_type}-{space}"
        if filter_keys:
            label += f"-filters-{'-'.join(sorted(filter_keys))}"
        return label

    @classmethod
    def store_queries(cls, space: str, client: KGClient):
        for query_type, follow_links in (("simple", 0), ("resolved-1", 1)):
            query_label = cls.get_query_label(query_type, space)
            query_definition = cls.generate_query(query_type, space, client, follow_links=follow_links)
            try:
                client.store_query(query_label, query_definition, space=space or cls.default_space)
            except HTTPError as err:
                if err.response.status_code == 401:
                    warn("Unable to store query with id '{}': {}".format(query_label, err.response.text))
                else:
                    raise

    @classmethod
    def retrieve_query(
        cls,
        query_type: str,
        space: Union[str, None],
        client: KGClient,
        filter_keys: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        query_label = cls.get_query_label(query_type, space, filter_keys)
        return client.retrieve_query(query_label)

    def children(self, client: KGClient, follow_links: int = 0) -> List[RepresentsSingleObject]:
        if follow_links:
            self.resolve(client, follow_links=follow_links)
        all_children = []
        for field in self.fields:
            if field.is_link:
                children = as_list(getattr(self, field.name))
                all_children.extend(children)
                if follow_links:
                    for child in children:
                        all_children.extend(child.children(client))
        return all_children

    def export(self, path: str, single_file: bool = False):
        """
        Export metadata as files in JSON-LD format.

        If any objects do not have IDs, these will be generated.

        If `single_file` is False, then `path` must be the path to a directory,
        and each object will be exported as a file named for the object ID.

        If `single_file` is True, then `path` should be the path to a file
        with extension ".jsonld". This file will contain metadata for all objects.
        """
        raise NotImplementedError("todo")