# E-commerce Data Pipeline

Simple ETL pipeline that scrapes book data, transforms it and loads it to Snowflake.

Project files
- [dashboard/](dashboard/)
- [database/](database/)
- [scripts/.env](scripts/.env)
- [scripts/main.py](scripts/main.py)
- [scripts/extract.py](scripts/extract.py)
- [scripts/Extract.py](scripts/Extract.py)
- [scripts/transform.py](scripts/transform.py)
- [scripts/load.py](scripts/load.py)


Key functions
- [`extract.get_book_data`](scripts/extract.py)
- [`extract.save_raw_data`](scripts/extract.py)
- [`transform.transform_data`](scripts/transform.py)
- [`transform.save_processed_data`](scripts/transform.py)
- [`load.load_data_to_snowflake`](scripts/load.py)
- [`main.run_pipeline`](scripts/main.py)

Requirements
- Python 3.8+
- Libraries: requests, beautifulsoup4, pandas, openpyxl, snowflake-connector-python, python-dotenv, lxml

Install dependencies:
```sh
pip install requests beautifulsoup4 pandas openpyxl snowflake-connector-python python-dotenv lxml
```

Setup

- Create an environment variables in scripts/.env:

- Add Snowflake credentials (user, password, account, warehouse, database, schema)
- Add File paths: output_path_ext (raw CSV path) and output_path_trans (processed Excel path)

Confirm the expected input/output paths in:

scripts/extract.py (writes raw CSV)
scripts/transform.py (reads raw CSV, writes Excel)
scripts/load.py (reads Excel and uploads to Snowflake)
Usage

Run the pipeline:

```sh
python [main.py](http://_vscodecontentref_/0)
```

This executes:

extraction via extract.get_book_data and extract.save_raw_data,
transformation via transform.transform_data and transform.save_processed_data,
loading via load.load_data_to_snowflake.
Notes and caveats

The project currently writes processed output as Excel (see scripts/transform.py). Update output_path_trans in scripts/.env if you prefer CSV.
There are two extract modules (scripts/extract.py and scripts/Extract.py). Use the lowercase scripts/extract.py imported by scripts/main.py.
The Snowflake table targeted by the loader is BOOK_FINAL (see scripts/load.py). Ensure the table schema matches the columns: title, price, link, in_stock, rating_number.
Data cleaning logic is in transform.transform_data (price parsing, availability -> boolean, rating mapping)


