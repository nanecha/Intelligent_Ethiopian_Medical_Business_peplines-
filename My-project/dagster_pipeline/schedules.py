from dagster import schedule
from .jobs import ethiopian_medical_pipeline

@schedule(cron_schedule="0 2 * * *", job=ethiopian_medical_pipeline, execution_timezone="UTC")
def daily_pipeline_schedule(_context):
    return {}
