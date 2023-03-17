"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base import EmbeddedMetadata, IRI
from fairgraph.fields import Field




class ViewerSpecification(EmbeddedMetadata):
    """

    """
    type_ = ["https://openminds.ebrains.eu/sands/ViewerSpecification"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("additional_remarks", str, "vocab:additionalRemarks", multiple=False, required=False,
              doc="Mention of what deserves additional attention or notice."),
        Field("anchor_point", "openminds.sands.CoordinatePoint", "vocab:anchorPoint", multiple=False, required=True,
              doc="no description available"),
        Field("camera_position", "openminds.sands.CoordinatePoint", "vocab:cameraPosition", multiple=False, required=False,
              doc="no description available"),
        Field("preferred_display_color", ["openminds.controlledterms.Colormap", "openminds.sands.SingleColor"], "vocab:preferredDisplayColor", multiple=False, required=False,
              doc="no description available"),

    ]

    def __init__(self, additional_remarks=None, anchor_point=None, camera_position=None, preferred_display_color=None, id=None, data=None, space=None, scope=None):
        return super().__init__(id=id, data=data, space=space, scope=scope, additional_remarks=additional_remarks, anchor_point=anchor_point, camera_position=camera_position, preferred_display_color=preferred_display_color)