"""

"""

# this file was auto-generated

from datetime import datetime
from fairgraph.base import KGObject
from fairgraph.fields import Field


class LaunchConfiguration(KGObject):
    """
    
    """
    space = "model"
    type = ["https://openminds.ebrains.eu/computation/LaunchConfiguration"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the launch configuration."),
        Field("name", str, "vocab:name", multiple=False, required=False,
              doc="Word or phrase that constitutes the distinctive designation of a being or thing."),
        Field("executable", str, "vocab:executable", multiple=False, required=True,
              doc="no description available"),
        Field("argumentss", str, "vocab:arguments", multiple=True, required=False,
              doc="no description available"),
        Field("environment_variables", "openminds.core.ParameterSet", "vocab:environmentVariables", multiple=False, required=False,
              doc="no description available"),
        
    ]
    existence_query_fields = None