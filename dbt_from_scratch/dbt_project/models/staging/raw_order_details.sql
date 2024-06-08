{{
  config(
    materialized='view'
  )
}}

SELECT
  *
FROM
  {{ source('raw', 'order_details') }}