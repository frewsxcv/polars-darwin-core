from pathlib import Path

import polars as pl
from polars_darwin_core.lf_csv import DarwinCoreCsvLazyFrame, read_darwin_core_csv


def test_read_darwin_core_csv(tmp_path: Path) -> None:
    # Create a tiny Darwin Core‐like CSV
    csv_path = tmp_path / "dwc.csv"
    csv_path.write_text("id,kingdom\n1,Animalia\n2,Plantae\n")

    lf = read_darwin_core_csv(csv_path)
    assert isinstance(lf, DarwinCoreCsvLazyFrame)

    df: pl.DataFrame = lf.collect()
    assert df.shape == (2, 2)  # two rows, two columns
    assert df["kingdom"].to_list() == ["Animalia", "Plantae"] 