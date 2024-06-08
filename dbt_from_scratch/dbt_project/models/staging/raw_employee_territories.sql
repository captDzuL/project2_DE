{{
  config(
    materialized='view'
  )
}}

SELECT
  *
FROM
  {{ source('raw', 'employee_territories') }}