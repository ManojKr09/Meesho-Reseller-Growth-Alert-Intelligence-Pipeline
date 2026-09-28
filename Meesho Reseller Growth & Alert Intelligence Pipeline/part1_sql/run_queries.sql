.headers on
.mode csv
.once part1_sql/output/monthly_category_revenue.csv
SELECT month, category, ROUND(SUM(quantity * unit_price), 2) AS revenue, COUNT(*) AS n_orders FROM orders GROUP BY month, category ORDER BY CASE month WHEN 'April' THEN 1 WHEN 'May' THEN 2 WHEN 'June' THEN 3 END, category;
.once part1_sql/output/region_revenue_orders.csv
SELECT r.region, ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue, COUNT(*) AS n_orders FROM orders o JOIN resellers r ON o.reseller_id=r.reseller_id GROUP BY r.region ORDER BY r.region;
.once part1_sql/output/top_resellers.csv
SELECT r.reseller_id, r.reseller_name, ROUND(SUM(o.quantity*o.unit_price),2) AS total_spend FROM orders o JOIN resellers r ON o.reseller_id=r.reseller_id GROUP BY r.reseller_id,r.reseller_name HAVING total_spend>50000 ORDER BY total_spend DESC LIMIT 5;
.once part1_sql/output/zero_order_resellers.csv
SELECT r.reseller_id,r.reseller_name FROM resellers r LEFT JOIN orders o ON r.reseller_id=o.reseller_id WHERE o.order_id IS NULL;
.once part1_sql/output/zero_order_count_demo.csv
SELECT r.reseller_id,COUNT(*) AS count_star,COUNT(o.order_id) AS count_order_id FROM resellers r LEFT JOIN orders o ON r.reseller_id=o.reseller_id WHERE r.reseller_id='RS024' GROUP BY r.reseller_id;
.once part1_sql/output/june_delivered_aov.csv
SELECT ROUND(SUM(quantity*unit_price)/COUNT(*),2) AS aov FROM orders WHERE month='June' AND status='Delivered';
