{{ config(schema='staging') }}

WITH base AS (
    SELECT
        message_id,
        channel_id,
        channel_name,
        message_text,
        posted_at::timestamp AS posted_at,
        media_type,
        media_url,
        length(message_text) AS message_length,
        CASE WHEN media_type IS NOT NULL THEN 1 ELSE 0 END AS has_media
    FROM raw.telegram_messages
)

SELECT * FROM base;
