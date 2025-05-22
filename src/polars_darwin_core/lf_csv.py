from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

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

    def __init__(self, inner: pl.LazyFrame):
        self._inner = inner

    # ---------------------------------------------------------------------
    # Public helpers
    # ---------------------------------------------------------------------
    def collect(self, **kwargs: Any) -> pl.DataFrame:  # noqa: D401
        """Eagerly evaluate the query plan and return a *polars* DataFrame."""

        return self._inner.collect(**kwargs)

    # More domain-specific helpers can be added here over time.

    # ---------------------------------------------------------------------
    # Dunder delegation
    # ---------------------------------------------------------------------
    def __getattr__(self, item: str):  # noqa: D401
        return getattr(self._inner, item)

    def __iter__(self) -> Iterable[Any]:  # pragma: no cover
        return iter(self._inner)

    def __repr__(self) -> str:  # pragma: no cover
        return f"DarwinCoreCsvLazyFrame({self._inner!r})"


# -------------------------------------------------------------------------
# Convenience functions
# -------------------------------------------------------------------------

def read_darwin_core_csv(path: str | Path, **scan_csv_kwargs: Any) -> DarwinCoreCsvLazyFrame:  # noqa: D401
    """Scan a Darwin Core CSV lazily.

    This is a very light wrapper around :pyfunc:`polars.scan_csv` that returns a
    domain-specific :class:`DarwinCoreCsvLazyFrame` instead of a plain
    :class:`polars.LazyFrame`.
    """

    inner = pl.scan_csv(path, **scan_csv_kwargs)
    return DarwinCoreCsvLazyFrame(inner) 