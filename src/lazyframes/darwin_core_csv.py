"""Compatibility shim for projects that previously imported from
``src.lazyframes.darwin_core_csv``.

The real implementation now lives in :pymod:`polars_darwin_core.lf_csv`.
This file *must* remain extremely small so that keeping the duplication
in-tree does not become a maintenance burden.
"""

from polars_darwin_core.lf_csv import DarwinCoreCsvLazyFrame, read_darwin_core_csv

__all__ = [
    "DarwinCoreCsvLazyFrame",
    "read_darwin_core_csv",
]