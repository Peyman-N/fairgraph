"""
Structured information about a specific implementation of a validation test.
"""

# this file was auto-generated

from datetime import date, datetime
from fairgraph import KGObject, IRI
from fairgraph.fields import Field

from fairgraph.errors import ResolutionFailure
from .validation_test import ValidationTest


class ValidationTestVersion(KGObject):
    """
    Structured information about a specific implementation of a validation test.
    """

    default_space = "computation"
    type_ = ["https://openminds.ebrains.eu/computation/ValidationTestVersion"]
    context = {
        "schema": "http://schema.org/",
        "kg": "https://kg.ebrains.eu/api/instances/",
        "vocab": "https://openminds.ebrains.eu/vocab/",
        "terms": "https://openminds.ebrains.eu/controlledTerms/",
        "core": "https://openminds.ebrains.eu/core/",
    }
    fields = [
        Field("name", str, "vocab:fullName", doc="Whole, non-abbreviated name of the validation test version."),
        Field(
            "alias",
            str,
            "vocab:shortName",
            required=True,
            doc="Shortened or fully abbreviated name of the validation test version.",
        ),
        Field(
            "accessibility",
            "openminds.controlledterms.ProductAccessibility",
            "vocab:accessibility",
            required=True,
            doc="Level to which something is accessible to the validation test version.",
        ),
        Field(
            "configuration",
            [
                "openminds.core.Configuration",
                "openminds.core.File",
                "openminds.core.PropertyValueList",
                "openminds.core.WebResource",
            ],
            "vocab:configuration",
            doc="no description available",
        ),
        Field(
            "copyright",
            "openminds.core.Copyright",
            "vocab:copyright",
            doc="Exclusive and assignable legal right of an originator to reproduce, publish, sell, or distribute the matter and form of a creative work for a defined time period.",
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
            doc="Longer statement or account giving the characteristics of the validation test version.",
        ),
        Field(
            "developers",
            ["openminds.core.Consortium", "openminds.core.Organization", "openminds.core.Person"],
            "vocab:developer",
            multiple=True,
            doc="Legal person that creates or improves products or services (e.g., software, applications, etc.).",
        ),
        Field(
            "digital_identifier",
            "openminds.core.DOI",
            "vocab:digitalIdentifier",
            doc="Digital handle to identify objects or legal persons.",
        ),
        Field("entry_point", str, "vocab:entryPoint", doc="no description available"),
        Field(
            "format",
            "openminds.core.ContentType",
            "vocab:format",
            required=True,
            doc="Method of digitally organizing and structuring data or information.",
        ),
        Field(
            "full_documentation",
            ["openminds.core.DOI", "openminds.core.File", "openminds.core.WebResource"],
            "vocab:fullDocumentation",
            required=True,
            doc="Non-abridged instructions, comments, and information for using a particular product.",
        ),
        Field(
            "funding",
            "openminds.core.Funding",
            "vocab:funding",
            multiple=True,
            doc="Money provided by a legal person for a particular purpose.",
        ),
        Field("homepage", IRI, "vocab:homepage", doc="Main website of the validation test version."),
        Field(
            "how_to_cite",
            str,
            "vocab:howToCite",
            doc="Preferred format for citing a particular object or legal person.",
        ),
        Field(
            "is_alternative_version_of",
            "openminds.computation.ValidationTestVersion",
            "vocab:isAlternativeVersionOf",
            multiple=True,
            doc="Reference to an original form where the essence was preserved, but presented in an alternative form.",
        ),
        Field(
            "is_new_version_of",
            "openminds.computation.ValidationTestVersion",
            "vocab:isNewVersionOf",
            doc="Reference to a previous (potentially outdated) particular form of something.",
        ),
        Field(
            "keywords",
            [
                "openminds.controlledterms.ActionStatusType",
                "openminds.controlledterms.AgeCategory",
                "openminds.controlledterms.AnalysisTechnique",
                "openminds.controlledterms.AnatomicalAxesOrientation",
                "openminds.controlledterms.AnatomicalIdentificationType",
                "openminds.controlledterms.AnatomicalPlane",
                "openminds.controlledterms.AnnotationCriteriaType",
                "openminds.controlledterms.AnnotationType",
                "openminds.controlledterms.AtlasType",
                "openminds.controlledterms.AuditoryStimulusType",
                "openminds.controlledterms.BiologicalOrder",
                "openminds.controlledterms.BiologicalSex",
                "openminds.controlledterms.BreedingType",
                "openminds.controlledterms.CellCultureType",
                "openminds.controlledterms.CellType",
                "openminds.controlledterms.ChemicalMixtureType",
                "openminds.controlledterms.Colormap",
                "openminds.controlledterms.ContributionType",
                "openminds.controlledterms.CranialWindowConstructionType",
                "openminds.controlledterms.CranialWindowReinforcementType",
                "openminds.controlledterms.CriteriaQualityType",
                "openminds.controlledterms.DataType",
                "openminds.controlledterms.DeviceType",
                "openminds.controlledterms.DifferenceMeasure",
                "openminds.controlledterms.Disease",
                "openminds.controlledterms.DiseaseModel",
                "openminds.controlledterms.EducationalLevel",
                "openminds.controlledterms.ElectricalStimulusType",
                "openminds.controlledterms.EthicsAssessment",
                "openminds.controlledterms.ExperimentalApproach",
                "openminds.controlledterms.FileBundleGrouping",
                "openminds.controlledterms.FileRepositoryType",
                "openminds.controlledterms.FileUsageRole",
                "openminds.controlledterms.GeneticStrainType",
                "openminds.controlledterms.GustatoryStimulusType",
                "openminds.controlledterms.Handedness",
                "openminds.controlledterms.Language",
                "openminds.controlledterms.Laterality",
                "openminds.controlledterms.LearningResourceType",
                "openminds.controlledterms.MeasuredQuantity",
                "openminds.controlledterms.MetaDataModelType",
                "openminds.controlledterms.ModelAbstractionLevel",
                "openminds.controlledterms.ModelScope",
                "openminds.controlledterms.MolecularEntity",
                "openminds.controlledterms.OlfactoryStimulusType",
                "openminds.controlledterms.OperatingDevice",
                "openminds.controlledterms.OperatingSystem",
                "openminds.controlledterms.OpticalStimulusType",
                "openminds.controlledterms.Organ",
                "openminds.controlledterms.OrganismSubstance",
                "openminds.controlledterms.OrganismSystem",
                "openminds.controlledterms.PatchClampVariation",
                "openminds.controlledterms.PreparationType",
                "openminds.controlledterms.ProductAccessibility",
                "openminds.controlledterms.ProgrammingLanguage",
                "openminds.controlledterms.QualitativeOverlap",
                "openminds.controlledterms.SemanticDataType",
                "openminds.controlledterms.Service",
                "openminds.controlledterms.SetupType",
                "openminds.controlledterms.SoftwareApplicationCategory",
                "openminds.controlledterms.SoftwareFeature",
                "openminds.controlledterms.Species",
                "openminds.controlledterms.StimulationApproach",
                "openminds.controlledterms.StimulationTechnique",
                "openminds.controlledterms.SubcellularEntity",
                "openminds.controlledterms.SubjectAttribute",
                "openminds.controlledterms.TactileStimulusType",
                "openminds.controlledterms.Technique",
                "openminds.controlledterms.TermSuggestion",
                "openminds.controlledterms.Terminology",
                "openminds.controlledterms.TissueSampleAttribute",
                "openminds.controlledterms.TissueSampleType",
                "openminds.controlledterms.TypeOfUncertainty",
                "openminds.controlledterms.UBERONParcellation",
                "openminds.controlledterms.UnitOfMeasurement",
                "openminds.controlledterms.VisualStimulusType",
            ],
            "vocab:keyword",
            multiple=True,
            doc="Significant word or concept that are representative of the validation test version.",
        ),
        Field(
            "licenses",
            "openminds.core.License",
            "vocab:license",
            multiple=True,
            doc="Grant by a party to another party as an element of an agreement between those parties that permits to do, use, or own something.",
        ),
        Field(
            "other_contributions",
            "openminds.core.Contribution",
            "vocab:otherContribution",
            multiple=True,
            doc="Giving or supplying of something (such as money or time) as a part or share other than what is covered elsewhere.",
        ),
        Field(
            "reference_data",
            ["openminds.core.DOI", "openminds.core.File", "openminds.core.FileBundle", "openminds.core.WebResource"],
            "vocab:referenceData",
            multiple=True,
            doc="no description available",
        ),
        Field(
            "related_publications",
            [
                "openminds.core.DOI",
                "openminds.core.HANDLE",
                "openminds.core.ISBN",
                "openminds.core.ISSN",
                "openminds.publications.Book",
                "openminds.publications.Chapter",
                "openminds.publications.ScholarlyArticle",
            ],
            "vocab:relatedPublication",
            multiple=True,
            doc="Reference to something that was made available for the general public to see or buy.",
        ),
        Field(
            "release_date",
            date,
            "vocab:releaseDate",
            required=True,
            doc="Fixed date on which a product is due to become or was made available for the general public to see or buy",
        ),
        Field(
            "repository",
            "openminds.core.FileRepository",
            "vocab:repository",
            doc="Place, room, or container where something is deposited or stored.",
        ),
        Field(
            "support_channels",
            str,
            "vocab:supportChannel",
            multiple=True,
            doc="Way of communication used to interact with users or customers.",
        ),
        Field(
            "version_identifier",
            str,
            "vocab:versionIdentifier",
            required=True,
            doc="Term or code used to identify the version of something.",
        ),
        Field(
            "version_innovation",
            str,
            "vocab:versionInnovation",
            required=True,
            doc="Documentation on what changed in comparison to a previously published form of something.",
        ),
    ]
    existence_query_fields = ("alias", "version_identifier")

    def __init__(
        self,
        name=None,
        alias=None,
        accessibility=None,
        configuration=None,
        copyright=None,
        custodians=None,
        description=None,
        developers=None,
        digital_identifier=None,
        entry_point=None,
        format=None,
        full_documentation=None,
        funding=None,
        homepage=None,
        how_to_cite=None,
        is_alternative_version_of=None,
        is_new_version_of=None,
        keywords=None,
        licenses=None,
        other_contributions=None,
        reference_data=None,
        related_publications=None,
        release_date=None,
        repository=None,
        support_channels=None,
        version_identifier=None,
        version_innovation=None,
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
            accessibility=accessibility,
            configuration=configuration,
            copyright=copyright,
            custodians=custodians,
            description=description,
            developers=developers,
            digital_identifier=digital_identifier,
            entry_point=entry_point,
            format=format,
            full_documentation=full_documentation,
            funding=funding,
            homepage=homepage,
            how_to_cite=how_to_cite,
            is_alternative_version_of=is_alternative_version_of,
            is_new_version_of=is_new_version_of,
            keywords=keywords,
            licenses=licenses,
            other_contributions=other_contributions,
            reference_data=reference_data,
            related_publications=related_publications,
            release_date=release_date,
            repository=repository,
            support_channels=support_channels,
            version_identifier=version_identifier,
            version_innovation=version_innovation,
        )

    def is_version_of(self, client):
        parents = ValidationTest.list(client, scope=self.scope, space=self.space, versions=self)
        if len(parents) == 0:
            raise ResolutionFailure("Unable to find parent")
        else:
            assert len(parents) == 1
            return parents[0]
