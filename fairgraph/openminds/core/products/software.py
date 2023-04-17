"""
Structured information on a software tool (concept level).
"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field


class Software(KGObject):
    """
    Structured information on a software tool (concept level).
    """

    default_space = "software"
    type_ = ["https://openminds.ebrains.eu/core/Software"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("name", str, "vocab:fullName", required=True, doc="Whole, non-abbreviated name of the software."),
        Field(
            "alias", str, "vocab:shortName", required=True, doc="Shortened or fully abbreviated name of the software."
        ),
        Field(
            "custodians",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:custodian",
            multiple=True,
            doc="The 'custodian' is a legal person who is responsible for the content and quality of the data, metadata, and/or code of a research product.",
        ),
        Field(
            "description",
            str,
            "vocab:description",
            required=True,
            doc="Longer statement or account giving the characteristics of the software.",
        ),
        Field(
            "developers",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:developer",
            multiple=True,
            required=True,
            doc="Legal person that creates or improves products or services (e.g., software, applications, etc.).",
        ),
        Field(
            "digital_identifier",
            ["openminds.core.DOI", "openminds.core.RRID", "openminds.core.SWHID"],
            "vocab:digitalIdentifier",
            doc="Digital handle to identify objects or legal persons.",
        ),
        Field(
            "versions",
            "openminds.core.SoftwareVersion",
            "vocab:hasVersion",
            multiple=True,
            required=True,
            doc="Reference to variants of an original.",
        ),
        Field("homepage", IRI, "vocab:homepage", doc="Main website of the software."),
        Field(
            "how_to_cite",
            str,
            "vocab:howToCite",
            doc="Preferred format for citing a particular object or legal person.",
        ),
    ]
    existence_query_fields = ("alias",)

    def __init__(
        self,
        name=None,
        alias=None,
        custodians=None,
        description=None,
        developers=None,
        digital_identifier=None,
        versions=None,
        homepage=None,
        how_to_cite=None,
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
            alias=alias,
            custodians=custodians,
            description=description,
            developers=developers,
            digital_identifier=digital_identifier,
            versions=versions,
            homepage=homepage,
            how_to_cite=how_to_cite,
        )
