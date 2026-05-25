# Power BI Dashboard Guide

## Dashboard Focus

The report focuses on three business areas:

- sales trends
- customer insights
- inventory analytics

## Suggested Visuals

### Sales Trends

- KPI cards for revenue and orders
- monthly line chart for revenue trend
- top products bar chart

### Customer Insights

- customer segmentation chart
- customer lifetime value table
- repeat customer summary

### Inventory Analytics

- inventory turnover chart
- low stock alert table
- stock on hand summary by product

## Suggested Measures

- Total Revenue = SUM(sales[revenue])
- Total Profit = SUM(sales[profit])
- Profit Margin = DIVIDE([Total Profit], [Total Revenue])
- Orders = COUNTROWS(sales)
- Customer Lifetime Value = CALCULATE([Total Revenue], ALLEXCEPT(customers, customers[customer_id]))
