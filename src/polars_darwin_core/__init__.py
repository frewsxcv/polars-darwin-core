__version__ = "1.0.0"

"""Top-level package for polars_darwin_core.

This library provides helpers for working with Darwin Core (DwC) data in
polars DataFrames and LazyFrames.
"""

from .darwin_core import Kingdom, kingdom_data_type, TAXONOMIC_RANKS
from .lf_csv import (
    DarwinCoreCsvLazyFrame,
    read_darwin_core_csv,
)
from .archive import scan_archive

__all__ = [
    "__version__",
    "Kingdom",
    "kingdom_data_type",
    "TAXONOMIC_RANKS",
    "DarwinCoreCsvLazyFrame",
    "read_darwin_core_csv",
    "scan_archive",
]
