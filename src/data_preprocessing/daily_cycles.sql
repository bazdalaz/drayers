WITH distinct_orders AS (
    SELECT DISTINCT phase,
    DATE (date) AS DATE
FROM df
WHERE phase='PREPARE'
    )

SELECT
    date,
    COUNT (*) as num_cycles

FROM distinct_orders
GROUP BY 1
ORDER BY 1

--https://www.youtube.com/watch?v=Wsfz3i1AXzY