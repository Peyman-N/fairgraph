"""

"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph.base_v3 import KGObjectV3, IRI
from fairgraph.fields import Field




class SoftwareVersion(KGObjectV3):
    """

    """
    default_space = "software"
    type = ["https://openminds.ebrains.eu/core/SoftwareVersion"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/"
    }
    fields = [
        Field("application_categories", "openminds.controlledterms.SoftwareApplicationCategory", "vocab:applicationCategory", multiple=True, required=True,
              doc="Distinct class that groups software programs which perform a similar task or set of tasks."),
        Field("developers", ["openminds.core.Organization", "openminds.core.Person"], "vocab:developer", multiple=True, required=False,
              doc="Legal person that creates or improves products or services (e.g., software, applications, etc.)."),
        Field("devices", "openminds.controlledterms.OperatingDevice", "vocab:device", multiple=True, required=True,
              doc="Piece of equipment or mechanism (hardware) designed to serve a special purpose or perform a special function."),
        Field("digital_identifier", ["openminds.core.DOI", "openminds.core.SWHID"], "vocab:digitalIdentifier", multiple=False, required=False,
              doc="Digital handle to identify objects or legal persons."),
        Field("has_components", "openminds.core.SoftwareVersion", "vocab:hasComponent", multiple=True, required=False,
              doc="Reference to an element of a collection."),
        Field("features", "openminds.controlledterms.SoftwareFeature", "vocab:feature", multiple=True, required=True,
              doc="Structure, form, or appearance that characterizes the software version."),
        Field("requirements", str, "vocab:requirement", multiple=True, required=False,
              doc="Something essential to the existence, occurrence or function of something else."),
        Field("input_formats", "openminds.core.ContentType", "vocab:inputFormat", multiple=True, required=False,
              doc="Format of data that is put into a process or machine."),
        Field("is_alternative_version_of", "openminds.core.SoftwareVersion", "vocab:isAlternativeVersionOf", multiple=True, required=False,
              doc="Reference to an original form where the essence was preserved, but presented in an alternative form."),
        Field("is_new_version_of", "openminds.core.SoftwareVersion", "vocab:isNewVersionOf", multiple=False, required=False,
              doc="Reference to a previous (potentially outdated) particular form of something."),
        Field("languages", "openminds.controlledterms.Language", "vocab:language", multiple=True, required=True,
              doc="System of communication (words, their pronunciation, and the methods of combining them) used and understood by a particular community."),
        Field("licenses", "openminds.core.License", "vocab:license", multiple=True, required=True,
              doc="Grant by a party to another party as an element of an agreement between those parties that permits to do, use, or own something."),
        Field("operating_systems", "openminds.controlledterms.OperatingSystem", "vocab:operatingSystem", multiple=True, required=True,
              doc="Software that controls the operation of a computer and directs the processing of programs."),
        Field("output_formats", "openminds.core.ContentType", "vocab:outputFormat", multiple=True, required=False,
              doc="Format of data that comes out of, is delivered or produced by a process or machine."),
        Field("programming_languages", "openminds.controlledterms.ProgrammingLanguage", "vocab:programmingLanguage", multiple=True, required=True,
              doc="Distinct set of instructions for computer programs in order to produce various kinds of output."),
        Field("accessibility", "openminds.controlledterms.ProductAccessibility", "vocab:accessibility", multiple=False, required=True,
              doc="Level to which something is accessible to the software version."),
        Field("copyright", "openminds.core.Copyright", "vocab:copyright", multiple=False, required=False,
              doc="Exclusive and assignable legal right of an originator to reproduce, publish, sell, or distribute the matter and form of a creative work for a defined time period."),
        Field("custodians", ["openminds.core.Organization", "openminds.core.Person"], "vocab:custodian", multiple=True, required=False,
              doc="Legal person entrusted with guarding and maintaining property or records."),
        Field("description", str, "vocab:description", multiple=False, required=False,
              doc="Longer statement or account giving the characteristics of the software version."),
        Field("full_documentation", ["openminds.core.DOI", "openminds.core.File", "openminds.core.URL"], "vocab:fullDocumentation", multiple=False, required=True,
              doc="Non-abridged instructions, comments, and information for using a particular product."),
        Field("name", str, "vocab:fullName", multiple=False, required=False,
              doc="Whole, non-abbreviated name of the software version."),
        Field("funding", "openminds.core.Funding", "vocab:funding", multiple=True, required=False,
              doc="Money provided by a legal person for a particular purpose."),
        Field("homepage", "openminds.core.URL", "vocab:homepage", multiple=False, required=False,
              doc="Main website of the software version."),
        Field("how_to_cite", str, "vocab:howToCite", multiple=False, required=False,
              doc="Preferred format for citing a particular object or legal person."),
        Field("keywords", ["openminds.controlledterms.BiologicalOrder", "openminds.controlledterms.BiologicalSex", "openminds.controlledterms.CellType", "openminds.controlledterms.Disease", "openminds.controlledterms.DiseaseModel", "openminds.controlledterms.Handedness", "openminds.controlledterms.Organ", "openminds.controlledterms.Phenotype", "openminds.controlledterms.Species", "openminds.controlledterms.Strain", "openminds.controlledterms.TermSuggestion", "openminds.controlledterms.UBERONParcellation", "openminds.sands.CustomAnatomicalEntity", "openminds.sands.ParcellationEntity", "openminds.sands.ParcellationEntityVersion"], "vocab:keyword", multiple=True, required=False,
              doc="Significant word or concept that are representative of the software version."),
        Field("other_contributions", "openminds.core.Contribution", "vocab:otherContribution", multiple=True, required=False,
              doc="Giving or supplying of something (such as money or time) as a part or share other than what is covered elsewhere."),
        Field("related_publications", ["openminds.core.DOI", "openminds.core.ISBN"], "vocab:relatedPublication", multiple=True, required=False,
              doc="Reference to something that was made available for the general public to see or buy."),
        Field("release_date", date, "vocab:releaseDate", multiple=False, required=True,
              doc="Fixed date on which a product is due to become or was made available for the general public to see or buy"),
        Field("repository", "openminds.core.FileRepository", "vocab:repository", multiple=False, required=False,
              doc="Place, room, or container where something is deposited or stored."),
        Field("alias", str, "vocab:shortName", multiple=False, required=True,
              doc="Shortened or fully abbreviated name of the software version."),
        Field("support_channels", str, "vocab:supportChannel", multiple=True, required=False,
              doc="Way of communication used to interact with users or customers."),
        Field("version_identifier", str, "vocab:versionIdentifier", multiple=False, required=True,
              doc="Term or code used to identify the version of something."),
        Field("version_innovation", str, "vocab:versionInnovation", multiple=False, required=True,
              doc="Documentation on what changed in comparison to a previously published form of something."),

    ]
    existence_query_fields = ('alias', 'version_identifier')