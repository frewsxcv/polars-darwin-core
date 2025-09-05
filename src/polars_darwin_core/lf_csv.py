from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Type
import xml.etree.ElementTree as ET

import polars as pl

from polars_darwin_core.darwin_core import kingdom_data_type

__all__ = [
    "DarwinCoreLazyFrame",
]


class DarwinCoreLazyFrame:
    """A thin wrapper around :pyclass:`polars.LazyFrame` for Darwin Core CSVs.

    The class intentionally exposes (and delegates to) the full *polars* lazy
    API while giving the object a domain-specific identity that tools like
    linters and type-checkers can understand.
    """

    # Columns that need a type override.
    # Polars can infer most types, but dates, datetimes, and booleans stored as
    # strings need to be specified.
    SCHEMA_OVERRIDES: Dict[str, Type[pl.DataType] | pl.DataType] = {
        "kingdom": kingdom_data_type,
        # Dates and datetimes
        # "modified": pl.Datetime,
        # "eventDate": pl.Datetime,
        # "dateIdentified": pl.Date,
        # "georeferencedDate": pl.Date,
        # "lastInterpreted": pl.Datetime,
        # "lastParsed": pl.Datetime,
        # "lastCrawled": pl.Datetime,
        # Booleans
        "hasCoordinate": pl.Boolean,
        "hasGeospatialIssues": pl.Boolean,
        "repatriated": pl.Boolean,
    }

    def __init__(self, inner: pl.LazyFrame):
        """Initialize the Darwin Core LazyFrame wrapper.

        Parameters
        ----------
        inner : pl.LazyFrame
            The inner LazyFrame to wrap
        """
        self._inner = inner

    @classmethod
    def from_csv(
        cls,
        path: str | Path,
    ) -> DarwinCoreLazyFrame:
        """Scan a Darwin Core CSV lazily.
        This is a very light wrapper around :pyfunc:`polars.scan_csv` that returns a
        domain-specific :class:`DarwinCoreLazyFrame` instead of a plain
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
            schema_overrides=DarwinCoreLazyFrame.SCHEMA_OVERRIDES,
            quote_char=None,
            separator="\t",
        )
        return DarwinCoreLazyFrame(inner)

    @classmethod
    def from_parquet(
        cls,
        path: str | Path,
    ) -> DarwinCoreLazyFrame:
        """Scan a Darwin Core Parquet file lazily.
        This is a very light wrapper around :pyfunc:`polars.scan_parquet` that returns a
        domain-specific :class:`DarwinCoreLazyFrame` instead of a plain
        :class:`polars.LazyFrame`.
        Parameters
        ----------
        path : str | Path
            Path to the Parquet file
        """

        inner = pl.scan_parquet(
            path,
        )
        return DarwinCoreLazyFrame(inner)

    @staticmethod
    def _parse_meta(meta_path: Path) -> tuple[str, bool, str, List[str]]:
        """Return information (core_file, has_header, separator, column_names)."""

        tree = ET.parse(meta_path)
        root = tree.getroot()

        # Handle XML namespace if present
        ns = {"dwc": "http://rs.tdwg.org/dwc/text/"}

        # Try with namespace first, then without
        core_elem = root.find("dwc:core", ns)
        if core_elem is None:
            core_elem = root.find(".//core")
        if core_elem is None:
            raise ValueError("meta.xml does not contain <core> element")

        # file location – in <files><location>relative/path</location></files>
        files_elem = core_elem.find(".//files")
        if files_elem is None:
            files_elem = core_elem.find("dwc:files", ns)
        if files_elem is None:
            raise ValueError("<core> missing <files>")

        location_elem = files_elem.find(".//location")
        if location_elem is None:
            location_elem = files_elem.find("dwc:location", ns)
        if location_elem is None or not location_elem.text:
            raise ValueError("<files> missing <location>")
        core_file = location_elem.text.strip()

        # delimiter & header
        separator = core_elem.get("fieldsTerminatedBy", "\t")
        # XML may encode tab as "\t" literal or as actual tab char
        if separator == "\t":
            separator = "\t"
        elif separator == "\\t":
            separator = "\t"

        ignore_header = int(core_elem.get("ignoreHeaderLines", "0"))
        has_header = ignore_header >= 1

        # column order
        fields: List[str] = []
        field_elems = core_elem.findall(".//field")
        if not field_elems:
            field_elems = core_elem.findall("dwc:field", ns)

        for field_elem in field_elems:
            index_str = field_elem.get("index")
            term_uri = field_elem.get("term")
            if index_str is None or term_uri is None:
                continue
            try:
                idx = int(index_str)
            except ValueError:
                continue
            # extract local term name from URI
            term = term_uri.rsplit("/", 1)[-1].rsplit("#", 1)[-1]
            if len(fields) <= idx:
                fields.extend([""] * (idx - len(fields) + 1))
            fields[idx] = term

        # some meta.xml include <id index="0" /> that represents the record id
        id_elem = core_elem.find(".//id")
        if id_elem is None:
            id_elem = core_elem.find("dwc:id", ns)
        assert id_elem is not None
        idx2 = id_elem.get("index")
        if idx2 is not None:
            idx = int(idx2)
            if len(fields) <= idx:
                fields.extend([""] * (idx - len(fields) + 1))
            # id doesn't have a term; choose "id"
            if not fields[idx]:
                fields[idx] = "id"

        # fill any empty column names with fallback names
        fields = [name if name else f"col_{i}" for i, name in enumerate(fields)]

        return core_file, has_header, separator, fields

    @classmethod
    def from_archive(
        cls, path: str | Path, **scan_csv_kwargs: Any
    ) -> DarwinCoreLazyFrame:  # noqa: D401
        """Scan an *unpacked* Darwin Core Archive directory lazily.
        Parameters
        ----------
        path:
            Path to a directory that contains at least ``meta.xml`` and the core
            data file referenced from it.
        **scan_csv_kwargs:
            Extra keyword arguments forwarded to :pyfunc:`polars.scan_csv` (e.g.
            ``infer_schema_length``).
        Returns
        -------
        DarwinCoreLazyFrame
        """

        base_dir = Path(path)
        meta_path = base_dir / "meta.xml"
        if not meta_path.exists():
            raise FileNotFoundError("meta.xml not found in archive directory")

        core_file_rel, has_header, separator, columns = cls._parse_meta(meta_path)
        data_path = base_dir / core_file_rel

        schema_from_meta = {
            col: cls.SCHEMA_OVERRIDES[col]
            for col in columns
            if col in cls.SCHEMA_OVERRIDES
        }
        scan_csv_kwargs.setdefault("schema_overrides", {}).update(schema_from_meta)

        inner = pl.scan_csv(
            data_path,
            separator=separator,
            has_header=has_header,
            new_columns=columns if not has_header else None,
            **scan_csv_kwargs,
        )

        return DarwinCoreLazyFrame(inner)
