from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import polars as pl

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
    EXPECTED_SCHEMA: Dict[str, pl.DataType] = {
        # Required core fields
        "scientificName": pl.Utf8,
        "kingdom": pl.Utf8,
        
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
        
        # Occurrence fields
        "basisOfRecord": pl.Utf8,
        "occurrenceID": pl.Utf8,
        "eventDate": pl.Utf8,
    }

    def __init__(self, inner: pl.LazyFrame, validate_schema: bool = True, strict: bool = False):
        """Initialize the Darwin Core LazyFrame wrapper.
        
        Parameters
        ----------
        inner : pl.LazyFrame
            The inner LazyFrame to wrap
        validate_schema : bool, default True
            Whether to validate that the schema matches EXPECTED_SCHEMA
        strict : bool, default False
            If True, enforces that all expected fields are present.
            If False, only validates the types of fields that are present.
        """
        self._inner = inner
        
        if validate_schema:
            # Use collect_schema() to avoid PerformanceWarning
            schema = inner.collect_schema()
            for field, dtype in self.EXPECTED_SCHEMA.items():
                if field in schema:
                    actual_type = schema[field]
                    assert actual_type == dtype, f"Field '{field}' has unexpected type: got {actual_type}, expected {dtype}"
                elif strict:
                    raise ValueError(f"Missing required field '{field}' in schema")

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------
    def collect(self, **kwargs: Any) -> pl.DataFrame:
        """Eagerly evaluate the query plan and return a *polars* DataFrame."""

        return self._inner.collect(**kwargs)

    # More domain-specific helpers can be added here over time.

    # ---------------------------------------------------------------------
    # Dunder delegation
    # ---------------------------------------------------------------------
    def __getattr__(self, item: str):
        return getattr(self._inner, item)

    def __iter__(self) -> Iterable[Any]:
        return iter(self._inner)

    def __repr__(self) -> str:
        return f"DarwinCoreCsvLazyFrame({self._inner!r})"


# -------------------------------------------------------------------------
# Convenience functions
# -------------------------------------------------------------------------

def read_darwin_core_csv(path: str | Path, validate_schema: bool = True, strict: bool = False, 
                        **scan_csv_kwargs: Any) -> DarwinCoreCsvLazyFrame:
    """Scan a Darwin Core CSV lazily.

    This is a very light wrapper around :pyfunc:`polars.scan_csv` that returns a
    domain-specific :class:`DarwinCoreCsvLazyFrame` instead of a plain
    :class:`polars.LazyFrame`.
    
    Parameters
    ----------
    path : str | Path
        Path to the CSV file
    validate_schema : bool, default True
        Whether to validate that the schema matches the expected Darwin Core schema
    strict : bool, default False
        If True, enforces that all expected fields are present.
        If False, only validates the types of fields that are present.
    **scan_csv_kwargs
        Additional keyword arguments passed to pl.scan_csv
    """

    inner = pl.scan_csv(path, **scan_csv_kwargs)
    return DarwinCoreCsvLazyFrame(inner, validate_schema=validate_schema, strict=strict) 