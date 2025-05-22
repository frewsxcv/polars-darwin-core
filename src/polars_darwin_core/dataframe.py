from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import polars as pl

__all__ = ["DarwinCoreDataFrame", "read_darwin_core_dataframe"]


def read_darwin_core_dataframe(path: str | Path, **read_csv_kwargs: Any) -> "DarwinCoreDataFrame":
    """Read a Darwin Core CSV eagerly into a *polars* DataFrame.

    Parameters
    ----------
    path:
        File path to a Darwin Core‐compatible CSV file.
    **read_csv_kwargs:
        Additional keyword arguments forwarded to :pyfunc:`polars.read_csv`.

    Returns
    -------
    DarwinCoreDataFrame
    """

    return DarwinCoreDataFrame(pl.read_csv(path, **read_csv_kwargs))


class DarwinCoreDataFrame(pl.DataFrame):
    """A *polars* DataFrame specialised for Darwin Core data.

    This subclass does not currently add new behaviour; it exists mainly for
    type clarity and to provide a future-proof extension point.
    """

    # NOTE: Sub-classing ``polars.DataFrame`` is *not* officially supported, but
    # in practice works fine for simple wrapper use-cases.  We keep the class
    # intentionally thin to avoid surprises.

    # Make DataFrame constructor inherits base.

    # You can extend with domain-specific helpers later, for example:
    #
    #     def filter_by_kingdom(self, kingdom: Kingdom) -> "DarwinCoreDataFrame":
    #         return self.filter(pl.col("kingdom") == str(kingdom)).cast(DarwinCoreDataFrame)

    # Typing trick: return "Self" once Python 3.11+ only

    def __init__(self, data: pl.DataFrame | Sequence[Mapping[str, Any]] | None = None, **kwargs: Any) -> None:  # type: ignore[override]
        super().__init__(data, **kwargs) 