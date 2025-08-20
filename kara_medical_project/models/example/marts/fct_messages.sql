{{ config(schema='marts') }}

SELECT
    m.message_id,
    c.channel_key,
    d.date_key,
    m.message_length,
    m.has_media,
    m.media_type,
    m.media_url
FROM {{ ref('stg_telegram_messages') }} m
LEFT JOIN {{ ref('dim_channels') }} c
    ON m.channel_id = c.channel_key
LEFT JOIN {{ ref('dim_dates') }} d
    ON m.posted_at::date = d.date_key;
