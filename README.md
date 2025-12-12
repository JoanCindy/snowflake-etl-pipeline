# E-commerce Data Pipeline

Simple ETL pipeline that scrapes book data, transforms it and loads it to Snowflake.

## 🚀 Quick Start

### Option 1: Run with Airflow (Recommended)
```bash
# Start Airflow services
docker compose up -d

# Access web UI at http://localhost:8080
# Username: airflow, Password: airflow

# Trigger the ETL pipeline from the web interface
```

### Option 2: Run Manually
```bash
pip install requests beautifulsoup4 pandas openpyxl snowflake-connector-python python-dotenv lxml
python scripts/main.py
```

## 📁 Project Structure

### Core Scripts
- [`scripts/main.py`](scripts/main.py) - Manual pipeline orchestration
- [`scripts/extract.py`](scripts/extract.py) - Data extraction from books.toscrape.com
- [`scripts/transform.py`](scripts/transform.py) - Data cleaning and transformation
- [`scripts/load.py`](scripts/load.py) - Data loading to Snowflake

### Airflow Integration
- [`dags/ecommerce_etl_dag.py`](dags/ecommerce_etl_dag.py) - Airflow DAG definition
- [`docker-compose.yaml`](docker-compose.yaml) - Airflow services configuration
- [`assets/etl_pipeline_diagram.svg`](assets/etl_pipeline_diagram.svg) - Pipeline diagram

## 🔧 Setup

### Environment Variables
Create `scripts/.env` with your Snowflake credentials:

```env
user="your_snowflake_user"
password="your_snowflake_password"
account="your_account.region"
warehouse="YOUR_WAREHOUSE"
database="YOUR_DATABASE"
schema="YOUR_SCHEMA"

output_path_ext="data/raw/books_raw.csv"
output_path_trans="data/processed/books_final.xlsx"
```

### Airflow Setup
```bash
# Ensure Docker is running
docker compose up -d

# Wait for services to be healthy
docker compose ps

# Access Airflow UI at http://localhost:8080
```

## 📊 ETL Pipeline Details

### Extract Phase
- **Source**: BooksToScrape.com (5 pages, ~100 books)
- **Data Collected**: Title, Price, Availability, Rating, Link
- **Output**: CSV file with raw book data

### Transform Phase
- **Input**: Raw CSV data
- **Operations**:
  - Price parsing and cleaning
  - Availability → Boolean conversion
  - Rating text → Numeric mapping (1-5)
  - Missing data handling
- **Output**: Cleaned Excel file

### Load Phase
- **Input**: Processed Excel data
- **Target**: Snowflake table `BOOK_FINAL`
- **Columns**: title, price, link, in_stock, rating_number

## 🌪️ Airflow DAG Features

### DAG Configuration
- **Name**: `ecommerce_etl_pipeline`
- **Schedule**: `@daily` (runs once per day)
- **Tasks**: Extract → Transform → Load (sequential)
- **Retries**: 1 retry with 5-minute delay
- **Catchup**: Disabled (no backfilling)

### Task Details

#### Extract Task
```python
# Scrapes book data from website
# Saves to: /opt/airflow/data/raw/books_raw.csv
# Returns: File path for next task
```

#### Transform Task
```python
# Cleans and transforms raw data
# Input: Raw CSV from extract task
# Output: /opt/airflow/data/processed/books_final.xlsx
# Returns: File path for load task
```

#### Load Task
```python
# Loads processed data to Snowflake
# Input: Excel file from transform task
# Target: BOOK_FINAL table
# Logs: Statistics and confirmation
```

### Monitoring & Logs
- **Web UI**: http://localhost:8080
- **Logs**: Available in Airflow UI per task
- **XCom**: Task communication via file paths
- **Health Checks**: Built-in service monitoring

### Manual Execution
1. Access Airflow UI
2. Navigate to DAGs page
3. Find `ecommerce_etl_pipeline`
4. Click ▶️ to trigger manually
5. Monitor progress in Graph/Tree views

## 📋 Requirements

### Manual Execution
- Python 3.9+
- Libraries: requests, beautifulsoup4, pandas, openpyxl, snowflake-connector-python, python-dotenv, lxml

### Airflow Execution
- Docker & Docker Compose
- 4GB+ RAM recommended
- Ports 8080, 5432, 6379 available

## 🔍 Troubleshooting

### Common Issues

**Airflow UI not accessible**:
```bash
docker compose ps  # Check service status
docker compose logs airflow-apiserver  # Check logs
```

**DAG import errors**:
- Ensure all required packages are installed
- Check file paths in container vs local
- Verify environment variables

**Snowflake connection issues**:
- Verify credentials in `scripts/.env`
- Check Snowflake account permissions
- Ensure BOOK_FINAL table exists with correct schema

### Useful Commands
```bash
# Restart Airflow services
docker compose restart

# View logs
docker compose logs -f airflow-scheduler
docker compose logs -f airflow-apiserver

# Stop services
docker compose down
```

## 📈 Data Flow

```
BooksToScrape.com → Extract → CSV → Transform → Excel → Load → Snowflake
       ↑              ↓              ↓              ↓              ↓
    Website      Raw Data      Cleaning      Processed      Database
   Scraping      Storage       Logic         Data          Storage
```

## 🎯 Key Functions

### Manual Execution
- [`extract.get_book_data`](scripts/extract.py) - Web scraping
- [`extract.save_raw_data`](scripts/extract.py) - CSV export
- [`transform.transform_data`](scripts/transform.py) - Data cleaning
- [`transform.save_processed_data`](scripts/transform.py) - Excel export
- [`load.load_data_to_snowflake`](scripts/load.py) - Database loading
- [`main.run_pipeline`](scripts/main.py) - Pipeline orchestration

### Airflow Tasks
- `extract_task()` - Orchestrated extraction
- `transform_task()` - Orchestrated transformation
- `load_task()` - Orchestrated loading

## 📝 Notes

- The project writes processed output as Excel by default. Update `output_path_trans` in `scripts/.env` for CSV format
- The Snowflake table targeted is `BOOK_FINAL`. Ensure the table schema matches: `title`, `price`, `link`, `in_stock`, `rating_number`
- Data cleaning logic handles price parsing, availability conversion, and rating mapping
- Airflow provides scheduling, monitoring, and error handling for production use
- Manual execution is suitable for development and testing


