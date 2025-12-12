from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Add the scripts directory to Python path
sys.path.append('/opt/airflow/scripts')

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(days=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'ecommerce_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for e-commerce book data',
    schedule="@daily",  # Run daily
    catchup=False,
)

def extract_task():
    """Extract book data from the website"""
    print("🚀 Starting extraction phase...")

    # Import here to avoid top-level imports
    from extract import get_book_data, save_raw_data

    # Use container paths
    output_path = '/opt/airflow/data/raw/books_raw.csv'

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Override environment variable for container
    os.environ['output_path_ext'] = output_path

    df_raw = get_book_data()
    save_raw_data(df_raw, output_path)

    print(f"✅ Extraction completed. Data saved to {output_path}")
    return output_path

def transform_task(**context):
    """Transform the extracted data"""
    print("🔄 Starting transformation phase...")

    # Import here to avoid top-level imports
    from transform import transform_data, save_processed_data

    # Get the output path from the previous task
    input_path = context['ti'].xcom_pull(task_ids='extract')

    # Use container paths
    output_path = '/opt/airflow/data/processed/books_final.xlsx'

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Override environment variables for container
    os.environ['output_path_ext'] = input_path
    os.environ['output_path_trans'] = output_path

    df_cleaned = transform_data(input_path)
    save_processed_data(df_cleaned, output_path)

    print(f"✅ Transformation completed. Data saved to {output_path}")
    return output_path

def load_task(**context):
    """Load transformed data to Snowflake"""
    print("📤 Starting loading phase...")

    # Import here to avoid top-level imports
    from load import load_data_to_snowflake

    # Get the output path from the previous task
    input_path = context['ti'].xcom_pull(task_ids='transform')

    # Override environment variable for container
    os.environ['output_path_trans'] = input_path

    load_data_to_snowflake(input_path)

    print("✅ Loading completed. Data loaded to Snowflake")

# Define the tasks
extract = PythonOperator(
    task_id='extract',
    python_callable=extract_task,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform',
    python_callable=transform_task,
    dag=dag,
)

load = PythonOperator(
    task_id='load',
    python_callable=load_task,
    dag=dag,
)

# Set task dependencies
extract >> transform >> load