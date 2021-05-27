"""
Structured information on a person.
"""

# this file was auto-generated

from datetime import datetime
from fairgraph.base import KGObject
from fairgraph.fields import Field


class Person(KGObject):
    """
    Structured information on a person.
    """
    space = "model"
    type = ["https://openminds.ebrains.eu/core/Person"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("digital_identifiers", "openminds.core.ORCID", "vocab:digitalIdentifier", multiple=True, required=False,
              doc="Digital handle to identify objects or legal persons."),
        Field("contact_information", "openminds.core.ContactInformation", "vocab:contactInformation", multiple=False, required=False,
              doc="Any available way used to contact a person or business (e.g., address, phone number, email address, etc.)."),
        Field("family_name", str, "vocab:familyName", multiple=False, required=False,
              doc="Name borne in common by members of a family."),
        Field("given_name", str, "vocab:givenName", multiple=False, required=True,
              doc="Name given to a person, including all potential middle names, but excluding the family name."),
        Field("affiliations", "openminds.core.Affiliation", "vocab:affiliation", multiple=True, required=False,
              doc="Declaration of a person being closely associated to an organization."),
        
    ]
    existence_query_fields = None