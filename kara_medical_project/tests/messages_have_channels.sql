SELECT *
FROM {{ ref('fct_messages') }}
WHERE channel_key IS NULL;
