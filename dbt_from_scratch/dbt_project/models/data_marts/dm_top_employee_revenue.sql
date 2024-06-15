WITH employee_revenue AS (
  SELECT
    e.FIRSTNAME || ' ' || e.LASTNAME AS employee_name,
    TO_CHAR(DATE_TRUNC('month', o.ORDERDATE), 'YYYY-MM') AS month_order,
    SUM((od.UNITPRICE - (od.UNITPRICE * od.DISCOUNT)) * od.QUANTITY) AS gross_revenue
  FROM
    {{ ref('raw_order_details') }} od
    JOIN {{ ref('raw_orders') }} o ON od.ORDERID = o.ORDERID
    JOIN {{ ref('raw_employees') }} e ON o.EMPLOYEEID = e.EMPLOYEEID
  GROUP BY
    employee_name, month_order
),
ranked_employees AS (
  SELECT
    employee_name,
    month_order,
    gross_revenue,
    ROW_NUMBER() OVER (PARTITION BY month_order ORDER BY gross_revenue DESC) AS rank
  FROM
    employee_revenue
)
SELECT
  employee_name,
  month_order,
  gross_revenue
FROM
  ranked_employees
WHERE
  rank = 1