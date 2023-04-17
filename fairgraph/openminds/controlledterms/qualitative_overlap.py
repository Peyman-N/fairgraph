"""

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - is homologous to
         - A set/object (A) has the same relative position, function, or structure as a set/object (B).
       * - is identical to
         - A set/object (A) is identical to another set/object (B) if they look exactly the same.
       * - is subset of
         - A set/object (A) is a subset of another set/object (B) if (A) and (B) are not equal, but all elements/incidents of (A) are also elements/incidents of (B).
       * - partially overlaps with
         - Two sets/objects (A and B) partially overlap when some elements/incidents are part of both original objects (A and B).
       * - is superset of
         - A set/object (A) is a superset of another set/object (B) if (A) and (B) are not equal, but all elements/incidents of (B) are also elements/incidents of (A).

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class QualitativeOverlap(KGObject):
    """

    .. list-table:: **Possible values**
       :widths: 20 80
       :header-rows: 0

       * - is homologous to
         - A set/object (A) has the same relative position, function, or structure as a set/object (B).
       * - is identical to
         - A set/object (A) is identical to another set/object (B) if they look exactly the same.
       * - is subset of
         - A set/object (A) is a subset of another set/object (B) if (A) and (B) are not equal, but all elements/incidents of (A) are also elements/incidents of (B).
       * - partially overlaps with
         - Two sets/objects (A and B) partially overlap when some elements/incidents are part of both original objects (A and B).
       * - is superset of
         - A set/object (A) is a superset of another set/object (B) if (A) and (B) are not equal, but all elements/incidents of (B) are also elements/incidents of (A).

    """

    default_space = "controlled"
    type_ = ["https://openminds.ebrains.eu/controlledTerms/QualitativeOverlap"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field(
            "name",
            str,
            "vocab:name",
            required=True,
            doc="Word or phrase that constitutes the distinctive designation of the qualitative overlap.",
        ),
        Field(
            "definition",
            str,
            "vocab:definition",
            doc="Short, but precise statement of the meaning of a word, word group, sign or a symbol.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            doc="Longer statement or account giving the characteristics of the qualitative overlap.",
        ),
        Field(
            "interlex_identifier",
            IRI,
            "vocab:interlexIdentifier",
            doc="Persistent identifier for a term registered in the InterLex project.",
        ),
        Field(
            "knowledge_space_link",
            IRI,
            "vocab:knowledgeSpaceLink",
            doc="Persistent link to an encyclopedia entry in the Knowledge Space project.",
        ),
        Field(
            "preferred_ontology_identifier",
            IRI,
            "vocab:preferredOntologyIdentifier",
            doc="Persistent identifier of a preferred ontological term.",
        ),
        Field(
            "synonyms",
            str,
            "vocab:synonym",
            multiple=True,
            doc="Words or expressions used in the same language that have the same or nearly the same meaning in some or all senses.",
        ),
    ]
    existence_query_fields = ("name",)

    def __init__(
        self,
        name=None,
        definition=None,
        description=None,
        interlex_identifier=None,
        knowledge_space_link=None,
        preferred_ontology_identifier=None,
        synonyms=None,
        id=None,
        data=None,
        space=None,
        scope=None,
    ):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            name=name,
            definition=definition,
            description=description,
            interlex_identifier=interlex_identifier,
            knowledge_space_link=knowledge_space_link,
            preferred_ontology_identifier=preferred_ontology_identifier,
            synonyms=synonyms,
        )
