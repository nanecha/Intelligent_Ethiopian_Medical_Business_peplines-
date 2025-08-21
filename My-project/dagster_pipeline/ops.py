from dagster import op

@op
def scrape_telegram_data():
    print("✅ Scraping Telegram data...")
    # call your scraper script here

@op
def load_raw_to_postgres():
    print("✅ Loading raw data into Postgres...")
    # call your Postgres loader script here

@op
def run_dbt_transformations():
    print("✅ Running dbt models...")
    # e.g., os.system("dbt run")

@op
def run_yolo_enrichment():
    print("✅ Running YOLO object detection enrichment...")
    # call your YOLO pipeline function here
