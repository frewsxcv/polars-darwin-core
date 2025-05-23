# polars-darwin-core

Helpers for working with [Darwin Core](https://dwc.tdwg.org/) CSV data using [polars](https://pola.rs/).

```shell
pip install polars-darwin-core
```

## Usage

### Reading a single Darwin Core CSV file

```python
from polars_darwin_core import read_darwin_core_csv

lf = read_darwin_core_csv("occurrence.csv")
print(lf.collect())
```

### Working with Darwin Core Archives (DwC-A)

```python
import polars as pl
from polars_darwin_core import scan_archive

# Path to an unpacked Darwin Core Archive directory (containing meta.xml)
archive_path = "path/to/dwc/archive"

# Load the core file from the archive
lf = scan_archive(archive_path)

# Work with the data
df = lf.filter(pl.col("kingdom") == "Animalia").collect()
print(df)
```

## Development

```shell
# Create a virtualenv however you prefer, then:
pip install -e .[dev]

# Run the test-suite
python -m unittest
```

The project follows the standard [PEP 517](https://peps.python.org/pep-0517/) build flow via [Hatch](https://hatch.pypa.io/):

```shell
python -m build    # create sdist and wheel in ./dist/
```
