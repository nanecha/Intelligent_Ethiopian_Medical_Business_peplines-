{{ config(schema='marts') }}

SELECT DISTINCT
    channel_id AS channel_key,
    channel_name
FROM {{ ref('stg_telegram_messages') }};
