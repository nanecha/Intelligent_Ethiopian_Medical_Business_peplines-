import json
import os
import psycopg2
from psycopg2.extras import Json

# Database connection parameters
db_params = {
    'dbname': 'kara_medical_db',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '5432'
}

# Data lake directory
data_lake_path = 'F:\\Change-point-analysis-and-statistical-modelling-of-time-series-data\\data_lake'

def create_raw_table():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;
            DROP TABLE IF EXISTS raw.telegram_messages CASCADE;
            CREATE TABLE raw.telegram_messages (
                id SERIAL PRIMARY KEY,
                json_data JSONB NOT NULL,
                file_name VARCHAR(255),
                channel_name VARCHAR(255),
                loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("Raw table created successfully.")
    except Exception as e:
        print(f"Error creating raw table: {e}")
    finally:
        cur.close()
        conn.close()

def load_json_files():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        json_files = [f for f in os.listdir(data_lake_path) if f.endswith('.json')]
        if len(json_files) != 3:
            print(f"Warning: Found {len(json_files)} JSON files, expected 3: {json_files}")
        for file in json_files:
            file_path = os.path.join(data_lake_path, file)
            # Derive channel_name from file name (e.g., 'channel1' from 'channel1.json')
            channel_name = os.path.splitext(file)[0]
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    json_data = json.load(f)
                    # Handle list of messages
                    if isinstance(json_data, list):
                        for item in json_data:
                            cur.execute(
                                "INSERT INTO raw.telegram_messages (json_data, file_name, channel_name) VALUES (%s, %s, %s)",
                                (Json(item), file, channel_name)
                            )
                    else:
                        cur.execute(
                            "INSERT INTO raw.telegram_messages (json_data, file_name, channel_name) VALUES (%s, %s, %s)",
                            (Json(json_data), file, channel_name)
                        )
                except json.JSONDecodeError as je:
                    print(f"Error decoding JSON in {file_path}: {je}")
        conn.commit()
        print("JSON data loaded successfully.")
    except Exception as e:
        print(f"Error loading JSON data: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    create_raw_table()
    load_json_files()