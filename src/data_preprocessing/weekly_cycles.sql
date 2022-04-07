WITH distinct_orders AS (
    SELECT DISTINCT batch,
    DATE (date) AS DATE
FROM df
    )

SELECT
    DATE(date, '1 DAYS', 'WEEKDAY 0', '-7 DAYS') as week,
    COUNT (*) as num_cycles

FROM distinct_orders
GROUP BY 1
ORDER BY 1

--https://www.youtube.com/watch?v=Wsfz3i1AXzY