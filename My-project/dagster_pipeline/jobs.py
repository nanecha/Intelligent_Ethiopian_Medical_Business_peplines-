from dagster import job
from .ops import scrape_telegram_data, load_raw_to_postgres, run_dbt_transformations, run_yolo_enrichment

@job
def ethiopian_medical_pipeline():
    raw = scrape_telegram_data()
    load = load_raw_to_postgres(start_after=raw)
    transform = run_dbt_transformations(start_after=load)
    run_yolo_enrichment(start_after=transform)
