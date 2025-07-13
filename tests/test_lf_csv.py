from pathlib import Path
import unittest
import tempfile

import polars as pl
from polars_darwin_core.lf_csv import DarwinCoreCsvLazyFrame, read_darwin_core_csv


class TestLfCsv(unittest.TestCase):
    def test_read_darwin_core_csv(self) -> None:
        # Create a tiny Darwin Core‐like CSV in a temporary directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            csv_path = tmp_path / "dwc.csv"
            csv_path.write_text("id,kingdom\n1,Animalia\n2,Plantae\n")

            lf = read_darwin_core_csv(csv_path)
            self.assertIsInstance(lf, DarwinCoreCsvLazyFrame)

            df: pl.DataFrame = lf._inner.collect()
            self.assertEqual(df.shape, (2, 2))  # two rows, two columns
            self.assertEqual(df["kingdom"].to_list(), ["Animalia", "Plantae"])
