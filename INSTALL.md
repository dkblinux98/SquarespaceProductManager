# squarespace-manager

Refactor of the IntelliJ project into a standard Python package with a CLI.

## Install (editable)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp example.config.ini ~/.squarespacemanager/config.ini  # then edit values
```

## Usage
```bash
sqsp login
sqsp update --csv /path/to/products.csv
```
