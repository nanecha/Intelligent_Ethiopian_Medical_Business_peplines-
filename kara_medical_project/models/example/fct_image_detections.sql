{{ config(materialized='table', schema='analytics') }}

SELECT
    d.message_id,
    d.detected_object_class,
    d.confidence_score,
    m.sender_id,
    m.posted_at
FROM raw.image_detections d
LEFT JOIN analytics.fact_messages m
    ON d.message_id = m.message_id
