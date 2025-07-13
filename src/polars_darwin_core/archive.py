from __future__ import annotations

"""Helpers for reading unpacked Darwin Core Archives (DwC-A)."""

from pathlib import Path
from typing import Any, List
import xml.etree.ElementTree as ET

import polars as pl

from .lf_csv import DarwinCoreCsvLazyFrame

__all__ = ["scan_archive"]


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


def scan_archive(path: str | Path, **scan_csv_kwargs: Any) -> DarwinCoreCsvLazyFrame:  # noqa: D401
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
    DarwinCoreCsvLazyFrame
    """

    base_dir = Path(path)
    meta_path = base_dir / "meta.xml"
    if not meta_path.exists():
        raise FileNotFoundError("meta.xml not found in archive directory")

    core_file_rel, has_header, separator, columns = _parse_meta(meta_path)
    data_path = base_dir / core_file_rel

    inner = pl.scan_csv(
        data_path,
        separator=separator,
        has_header=has_header,
        new_columns=columns if has_header is False else None,
        **scan_csv_kwargs,
    )

    return DarwinCoreCsvLazyFrame(inner)