"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base import EmbeddedMetadata, IRI
from fairgraph.fields import Field




class ParcellationTerminology(EmbeddedMetadata):
    """

    """
    type_ = ["https://openminds.ebrains.eu/sands/ParcellationTerminology"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("data_locations", "openminds.core.File", "vocab:dataLocation", multiple=True, required=False,
              doc="no description available"),
        Field("entities", "openminds.sands.ParcellationEntity", "vocab:hasEntity", multiple=True, required=True,
              doc="no description available"),
        Field("ontology_identifiers", str, "vocab:ontologyIdentifier", multiple=True, required=False,
              doc="Term or code used to identify the parcellation terminology registered within a particular ontology."),

    ]
