"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class FileRepositoryStructure(KGObject):
    """ """

    default_space = "files"
    type_ = ["https://openminds.ebrains.eu/core/FileRepositoryStructure"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("lookup_label", str, "vocab:lookupLabel", doc="no description available"),
        Field(
            "file_path_patterns",
            "openminds.core.FilePathPattern",
            "vocab:filePathPattern",
            multiple=True,
            required=True,
            doc="no description available",
        ),
    ]
    existence_query_fields = ("lookup_label",)

    def __init__(self, lookup_label=None, file_path_patterns=None, id=None, data=None, space=None, scope=None):
        return super().__init__(
            id=id,
            space=space,
            scope=scope,
            data=data,
            lookup_label=lookup_label,
            file_path_patterns=file_path_patterns,
        )
