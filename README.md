# polars-darwin-core

Helpers for working with [Darwin Core](https://dwc.tdwg.org/) CSV data using [polars](https://pola.rs/).

```shell
pip install polars-darwin-core
```

```python
from polars_darwin_core import read_darwin_core_csv

lf = read_darwin_core_csv("occurrence.csv")
print(lf.collect())
```

## Development

```shell
# Create a virtualenv however you prefer, then:
pip install -e .[dev]

# Run the test-suite
pytest -q
```

The project follows the standard [PEP 517](https://peps.python.org/pep-0517/) build flow via [Hatch](https://hatch.pypa.io/):

```shell
python -m build    # create sdist and wheel in ./dist/
```
