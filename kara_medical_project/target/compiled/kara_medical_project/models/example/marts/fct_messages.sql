

SELECT
    m.message_id,
    c.channel_key,
    d.date_key,
    m.message_length,
    m.has_media,
    m.media_type,
    m.media_url
FROM "kara_medical_db"."public_staging"."stg_telegram_messages" m
LEFT JOIN "kara_medical_db"."public_marts"."dim_channels" c
    ON m.channel_id = c.channel_key
LEFT JOIN "kara_medical_db"."public_marts"."dim_dates" d
    ON m.posted_at::date = d.date_key;