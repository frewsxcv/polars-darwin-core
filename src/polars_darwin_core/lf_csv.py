from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Type

import polars as pl

from polars_darwin_core.darwin_core import kingdom_data_type

__all__ = [
    "DarwinCoreCsvLazyFrame",
    "read_darwin_core_csv",
]


class DarwinCoreCsvLazyFrame:  # pylint: disable=too-few-public-methods
    """A thin wrapper around :pyclass:`polars.LazyFrame` for Darwin Core CSVs.

    The class intentionally exposes (and delegates to) the full *polars* lazy
    API while giving the object a domain-specific identity that tools like
    linters and type-checkers can understand.
    """

    # Common required fields in Darwin Core datasets
    EXPECTED_SCHEMA: Dict[str, Type[pl.DataType] | pl.DataType] = {
        # Required core fields
        "scientificName": pl.Utf8,
        "kingdom": kingdom_data_type,
        # Optional but common fields
        "phylum": pl.Utf8,
        "class": pl.Utf8,
        "order": pl.Utf8,
        "family": pl.Utf8,
        "genus": pl.Utf8,
        "species": pl.Utf8,
        # Geolocation fields
        "decimalLatitude": pl.Float64,
        "decimalLongitude": pl.Float64,
        "continent": pl.Utf8,
        "country": pl.Utf8,
        "countryCode": pl.Utf8,
        "stateProvince": pl.Utf8,
        "county": pl.Utf8,
        "municipality": pl.Utf8,
        "locality": pl.Utf8,
        "verbatimLocality": pl.Utf8,
        "minimumElevationInMeters": pl.Float64,
        "maximumElevationInMeters": pl.Float64,
        "verbatimElevation": pl.Utf8,
        "minimumDepthInMeters": pl.Float64,
        "maximumDepthInMeters": pl.Float64,
        "verbatimDepth": pl.Utf8,
        "geodeticDatum": pl.Utf8,
        "coordinateUncertaintyInMeters": pl.Float64,
        "georeferenceProtocol": pl.Utf8,
        "georeferenceSources": pl.Utf8,
        "georeferenceVerificationStatus": pl.Utf8,
        # Occurrence fields
        "basisOfRecord": pl.Utf8,
        "occurrenceID": pl.Utf8,
        "eventDate": pl.Utf8,
        "catalogNumber": pl.Utf8,
        "recordNumber": pl.Utf8,
        "recordedBy": pl.Utf8,
        "individualCount": pl.Int64,
        "sex": pl.Utf8,
        "lifeStage": pl.Utf8,
        "reproductiveCondition": pl.Utf8,
        "occurrenceStatus": pl.Utf8,
        "occurrenceRemarks": pl.Utf8,
        # Record-level fields
        "type": pl.Utf8,
        "modified": pl.Utf8,
        "language": pl.Utf8,
        "license": pl.Utf8,
        "rightsHolder": pl.Utf8,
        "accessRights": pl.Utf8,
        "bibliographicCitation": pl.Utf8,
        "references": pl.Utf8,
        "institutionID": pl.Utf8,
        "collectionID": pl.Utf8,
        "datasetID": pl.Utf8,
        "institutionCode": pl.Utf8,
        "collectionCode": pl.Utf8,
        "datasetName": pl.Utf8,
        "ownerInstitutionCode": pl.Utf8,
        "informationWithheld": pl.Utf8,
        "dataGeneralizations": pl.Utf8,
        "dynamicProperties": pl.Utf8,
    }

    # SCHEMA_OVERRIDES = {
    #     "decimalLatitude": pl.Float64(),
    #     "decimalLongitude": pl.Float64(),
    #     "taxonKey": pl.UInt64(),
    #     "verbatimScientificName": pl.String(),
    #     "order": pl.String(),
    #     "recordedBy": pl.String(),
    #     "kingdom": kingdom_enum,
    # }

    def __init__(self, inner: pl.LazyFrame):
        """Initialize the Darwin Core LazyFrame wrapper.

        Parameters
        ----------
        inner : pl.LazyFrame
            The inner LazyFrame to wrap
        """
        self._inner = inner


# -------------------------------------------------------------------------
# Convenience functions
# -------------------------------------------------------------------------


def read_darwin_core_csv(
    path: str | Path, **scan_csv_kwargs: Any
) -> DarwinCoreCsvLazyFrame:
    """Scan a Darwin Core CSV lazily.

    This is a very light wrapper around :pyfunc:`polars.scan_csv` that returns a
    domain-specific :class:`DarwinCoreCsvLazyFrame` instead of a plain
    :class:`polars.LazyFrame`.

    Parameters
    ----------
    path : str | Path
        Path to the CSV file
    **scan_csv_kwargs
        Additional keyword arguments passed to pl.scan_csv
    """

    inner = pl.scan_csv(
        path,
        schema_overrides=DarwinCoreCsvLazyFrame.EXPECTED_SCHEMA,
        quote_char=None,
        **scan_csv_kwargs,
    )
    return DarwinCoreCsvLazyFrame(inner)
