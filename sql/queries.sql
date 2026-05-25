-- Top-selling products
SELECT
    p.product_name,
    SUM(s.revenue) AS total_revenue,
    SUM(s.quantity) AS units_sold
FROM sales s
JOIN products p ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Monthly sales trends
SELECT
    sale_month,
    SUM(net_revenue) AS monthly_revenue
FROM sales
GROUP BY sale_month
ORDER BY sale_month;

-- Regional performance
SELECT
    r.region_name,
    SUM(s.net_revenue) AS regional_revenue,
    SUM(s.profit) AS regional_profit,
    ROUND(SUM(s.profit) / NULLIF(SUM(s.net_revenue), 0), 4) AS profit_margin
FROM sales s
JOIN regions r ON s.region_id = r.region_id
GROUP BY r.region_name
ORDER BY regional_revenue DESC;

-- Customer segmentation
SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    SUM(s.net_revenue) AS revenue
FROM customers c
JOIN sales s ON c.customer_id = s.customer_id
GROUP BY c.segment
ORDER BY revenue DESC;

-- Inventory analytics
SELECT
    p.product_name,
    i.stock_on_hand,
    i.reorder_level,
    COALESCE(SUM(s.quantity), 0) AS units_sold,
    ROUND(COALESCE(SUM(s.quantity), 0) / NULLIF(i.stock_on_hand, 0), 2) AS inventory_turnover
FROM inventory i
JOIN products p ON i.product_id = p.product_id
LEFT JOIN sales s ON i.product_id = s.product_id
GROUP BY p.product_name, i.stock_on_hand, i.reorder_level
ORDER BY inventory_turnover DESC;

-- Revenue insights
SELECT
    DATE_TRUNC('month', sale_date) AS revenue_month,
    SUM(net_revenue) AS revenue,
    SUM(profit) AS profit
FROM sales
GROUP BY DATE_TRUNC('month', sale_date)
ORDER BY revenue_month;
