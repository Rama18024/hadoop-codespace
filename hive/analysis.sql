USE smart_canteen;

-- 1. Overall canteen statistics
SELECT
    SUM(prepared_quantity) AS total_prepared,
    SUM(sold_quantity) AS total_sold,
    SUM(leftover_quantity) AS total_leftover,
    ROUND(100.0 * SUM(leftover_quantity) / SUM(prepared_quantity), 2)
        AS overall_waste_percentage
FROM food_waste;

-- 2. Food-wise waste analysis
SELECT
    food_item,
    SUM(prepared_quantity) AS total_prepared,
    SUM(sold_quantity) AS total_sold,
    SUM(leftover_quantity) AS total_leftover,
    ROUND(
        100.0 * SUM(leftover_quantity) / SUM(prepared_quantity), 2
    ) AS waste_percentage
FROM food_waste
GROUP BY food_item
ORDER BY waste_percentage DESC;
