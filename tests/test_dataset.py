from pathlib import Path
import unittest
import tempfile
import shutil
import os

import polars as pl
from polars_darwin_core import read_darwin_core_csv, DarwinCoreCsvLazyFrame
from polars_darwin_core.archive import scan_archive


class TestDarwinCore(unittest.TestCase):
    def test_sample_dataset_occurrence(self) -> None:
        """Ensure we can lazily scan the sample Darwin Core occurrence file."""

        data_dir = Path(__file__).parents[1] / "sample-dataset"
        file_path = data_dir / "occurrence.txt"

        lf = read_darwin_core_csv(file_path, separator="\t")
        self.assertIsInstance(lf, DarwinCoreCsvLazyFrame)

        # Collect a small portion to verify schema and some basic stats
        # Polars will lazily evaluate; we collect first 100 rows for speed.
        df: pl.DataFrame = lf.head(1).collect()
        self.assertEqual(df.shape, (1, df.width))
        expected_row = {
            'gbifID': 984586740,
            'accessRights': None,
            'bibliographicCitation': None,
            'language': None,
            'license': 'CC_BY_4_0',
            'modified': None,
            'publisher': None,
            'references': None,
            'rightsHolder': None,
            'type': None,
            'institutionID': None,
            'collectionID': None,
            'datasetID': None,
            'institutionCode': 'CLO',
            'collectionCode': 'EBIRD',
            'datasetName': None,
            'ownerInstitutionCode': None,
            'basisOfRecord': 'HUMAN_OBSERVATION',
            'informationWithheld': None,
            'dataGeneralizations': None,
            'dynamicProperties': None,
            'occurrenceID': 'URN:catalog:CLO:EBIRD:OBS96797545',
            'catalogNumber': 'OBS96797545',
            'recordNumber': None,
            'recordedBy': 'obsr134796',
            'recordedByID': None,
            'individualCount': 1,
            'organismQuantity': None,
            'organismQuantityType': None,
            'sex': None,
            'lifeStage': None,
            'reproductiveCondition': None,
            'caste': None,
            'behavior': None,
            'vitality': None,
            'establishmentMeans': None,
            'degreeOfEstablishment': None,
            'pathway': None,
            'georeferenceVerificationStatus': None,
            'occurrenceStatus': 'PRESENT',
            'preparations': None,
            'disposition': None,
            'associatedOccurrences': None,
            'associatedReferences': None,
            'associatedSequences': None,
            'associatedTaxa': None,
            'otherCatalogNumbers': None,
            'occurrenceRemarks': None,
            'organismID': None,
            'organismName': None,
            'organismScope': None,
            'associatedOrganisms': None,
            'previousIdentifications': None,
            'organismRemarks': None,
            'materialEntityID': None,
            'materialEntityRemarks': None,
            'verbatimLabel': None,
            'materialSampleID': None,
            'eventID': None,
            'parentEventID': None,
            'eventType': None,
            'fieldNumber': None,
            'eventDate': '1977-02-26',
            'eventTime': None,
            'startDayOfYear': 57,
            'endDayOfYear': 57,
            'year': 1977,
            'month': 2,
            'day': 26,
            'verbatimEventDate': None,
            'habitat': None,
            'samplingProtocol': None,
            'sampleSizeValue': None,
            'sampleSizeUnit': None,
            'samplingEffort': None,
            'fieldNotes': None,
            'eventRemarks': None,
            'locationID': None,
            'higherGeographyID': None,
            'higherGeography': None,
            'continent': 'EUROPE',
            'waterBody': None,
            'islandGroup': None,
            'island': None,
            'countryCode': 'MC',
            'stateProvince': 'Monaco',
            'county': None,
            'municipality': None,
            'locality': 'Monte-Carlo Monaco',
            'verbatimLocality': None,
            'verbatimElevation': None,
            'verticalDatum': None,
            'verbatimDepth': None,
            'minimumDistanceAboveSurfaceInMeters': None,
            'maximumDistanceAboveSurfaceInMeters': None,
            'locationAccordingTo': None,
            'locationRemarks': None,
            'decimalLatitude': 43.732407,
            'decimalLongitude': 7.422724,
            'coordinateUncertaintyInMeters': None,
            'coordinatePrecision': None,
            'pointRadiusSpatialFit': None,
            'verbatimCoordinateSystem': None,
            'verbatimSRS': None,
            'footprintWKT': None,
            'footprintSRS': None,
            'footprintSpatialFit': None,
            'georeferencedBy': None,
            'georeferencedDate': None,
            'georeferenceProtocol': None,
            'georeferenceSources': None,
            'georeferenceRemarks': None,
            'geologicalContextID': None,
            'earliestEonOrLowestEonothem': None,
            'latestEonOrHighestEonothem': None,
            'earliestEraOrLowestErathem': None,
            'latestEraOrHighestErathem': None,
            'earliestPeriodOrLowestSystem': None,
            'latestPeriodOrHighestSystem': None,
            'earliestEpochOrLowestSeries': None,
            'latestEpochOrHighestSeries': None,
            'earliestAgeOrLowestStage': None,
            'latestAgeOrHighestStage': None,
            'lowestBiostratigraphicZone': None,
            'highestBiostratigraphicZone': None,
            'lithostratigraphicTerms': None,
            'group': None,
            'formation': None,
            'member': None,
            'bed': None,
            'identificationID': None,
            'verbatimIdentification': None,
            'identificationQualifier': None,
            'typeStatus': None,
            'identifiedBy': None,
            'identifiedByID': None,
            'dateIdentified': None,
            'identificationReferences': None,
            'identificationVerificationStatus': None,
            'identificationRemarks': None,
            'taxonID': None,
            'scientificNameID': None,
            'acceptedNameUsageID': None,
            'parentNameUsageID': None,
            'originalNameUsageID': None,
            'nameAccordingToID': None,
            'namePublishedInID': None,
            'taxonConceptID': 'avibase-E5531933',
            'scientificName': 'Lophophanes cristatus (Linnaeus, 1758)',
            'acceptedNameUsage': None,
            'parentNameUsage': None,
            'originalNameUsage': None,
            'nameAccordingTo': None,
            'namePublishedIn': None,
            'namePublishedInYear': None,
            'higherClassification': None,
            'kingdom': 'Animalia',
            'phylum': 'Chordata',
            'class': 'Aves',
            'order': 'Passeriformes',
            'superfamily': None,
            'family': 'Paridae',
            'subfamily': None,
            'tribe': None,
            'subtribe': None,
            'genus': 'Lophophanes',
            'genericName': 'Lophophanes',
            'subgenus': None,
            'infragenericEpithet': None,
            'specificEpithet': 'cristatus',
            'infraspecificEpithet': None,
            'cultivarEpithet': None,
            'taxonRank': 'SPECIES',
            'verbatimTaxonRank': None,
            'vernacularName': 'Crested Tit',
            'nomenclaturalCode': None,
            'taxonomicStatus': 'ACCEPTED',
            'nomenclaturalStatus': None,
            'taxonRemarks': None,
            'datasetKey': '4fa7b334-ce0d-4e88-aaae-2e0c138d049e',
            'publishingCountry': 'MC',
            'lastInterpreted': '2025-02-05T00:21:14.527Z',
            'elevation': None,
            'elevationAccuracy': None,
            'depth': None,
            'depthAccuracy': None,
            'distanceFromCentroidInMeters': 245.34532311724828,
            'issue': 'CONTINENT_DERIVED_FROM_COORDINATES;TAXON_MATCH_TAXON_CONCEPT_ID_IGNORED',
            'mediaType': None,
            'hasCoordinate': True,
            'hasGeospatialIssues': False,
            'taxonKey': 2487883,
            'acceptedTaxonKey': 2487883,
            'kingdomKey': 1,
            'phylumKey': 44,
            'classKey': 212,
            'orderKey': 729,
            'familyKey': 9327,
            'genusKey': 2487881,
            'subgenusKey': None,
            'speciesKey': 2487883,
            'species': 'Lophophanes cristatus',
            'acceptedScientificName': 'Lophophanes cristatus (Linnaeus, 1758)',
            'verbatimScientificName': 'Lophophanes cristatus',
            'typifiedName': None,
            'protocol': 'DWC_ARCHIVE',
            'lastParsed': '2025-02-05T00:21:14.527Z',
            'lastCrawled': '2024-09-27T13:35:39.907Z',
            'repatriated': False,
            'relativeOrganismQuantity': None,
            'projectId': None,
            'isSequenced': False,
            'gbifRegion': 'EUROPE',
            'publishedByGbifRegion': 'EUROPE',
            'level0Gid': 'MCO',
            'level0Name': 'Monaco',
            'level1Gid': None,
            'level1Name': None,
            'level2Gid': None,
            'level2Name': None,
            'level3Gid': None,
            'level3Name': None,
            'iucnRedListCategory': 'LC',
        }

        self.assertEqual(df.to_dicts()[0], expected_row)

    def test_scan_archive_core(self) -> None:
        """Test the scan_archive function using the existing sample dataset."""
        # Use the sample dataset directory from the repository
        data_dir = Path(__file__).parents[1] / "sample-dataset"

        # Call scan_archive with the sample dataset
        lf = scan_archive(data_dir)

        # Validate the result is a DarwinCoreCsvLazyFrame
        self.assertIsInstance(lf, DarwinCoreCsvLazyFrame)

        # Collect a small portion to verify we can access the data
        df = lf.head(2).collect()

        # Verify we have the right schema - occurrence.txt has many columns
        self.assertTrue(df.width > 10)

        # Check for some expected columns from Darwin Core
        expected_columns = ["scientificName", "kingdom", "decimalLatitude", "decimalLongitude"]
        for col in expected_columns:
            self.assertIn(col, df.columns)

        # Verify we can access a specific value from the first row
        # The first record should be for "Lophophanes cristatus" based on our earlier test
        self.assertEqual(df["scientificName"][0], "Lophophanes cristatus (Linnaeus, 1758)")
