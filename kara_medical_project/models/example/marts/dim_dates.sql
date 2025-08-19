{{ config(schema='marts') }}

SELECT DISTINCT
    posted_at::date AS date_key,
    EXTRACT(year FROM posted_at) AS year,
    EXTRACT(month FROM posted_at) AS month,
    EXTRACT(day FROM posted_at) AS day,
    EXTRACT(week FROM posted_at) AS week,
    EXTRACT(dow FROM posted_at) AS day_of_week
FROM {{ ref('stg_telegram_messages') }};
