{{
  config(
    materialized='view'
  )
}}

SELECT
  *
FROM
  {{ source('raw', 'territories') }}