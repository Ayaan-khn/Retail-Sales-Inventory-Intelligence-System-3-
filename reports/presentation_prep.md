# Presentation Preparation

## Short Professional Project Summary

Retail Sales & Inventory Intelligence System is a Python and Power BI analytics project that converts raw retail CSV data into cleaned datasets, a star-schema reporting model, KPI measures, and an interactive dashboard plan. The project analyzes sales, orders, customers, staff, products, stores, inventory, and shipment delays to support data-driven retail decision-making.

## Resume-Ready Project Description

Built a Retail Sales & Inventory Intelligence System using Python, Pandas, NumPy, and Power BI. Cleaned and validated 9 relational CSV datasets, engineered sales, inventory, and shipment KPIs, created Power BI-ready fact and dimension tables, and designed an executive dashboard covering revenue trends, product/category performance, staff performance, customer frequency, stock levels, and shipment delays.

## HR / Interviewer Explanation

This project simulates a real retail analytics use case where management needs visibility into sales, inventory, staff, customers, and fulfillment. I used Python for data cleaning, quality checks, feature engineering, and export of dashboard-ready tables. Then I designed a Power BI model using fact and dimension tables, wrote DAX measures for business KPIs, and planned a three-page dashboard for executive, product/inventory, and customer/staff analysis.

The main business value is that the company can quickly identify top-selling brands and categories, monitor store and staff performance, find low-stock products, and detect delayed shipments.

## 5-Minute Presentation Script

### Opening

Good morning. My project is titled Retail Sales & Inventory Intelligence System. The objective of this project is to build a professional analytics solution that helps a retail business monitor sales, inventory, customers, staff performance, and shipment delays using Python and Power BI.

### Problem Statement

Retail businesses generate data from orders, products, stores, customers, staff, and inventory. Without a structured analytics system, it becomes difficult to identify revenue drivers, monitor stock risk, track delayed shipments, and evaluate staff performance. This project solves that problem by converting raw CSV data into clean, dashboard-ready insights.

### Dataset

The dataset contains nine CSV files: customers, orders, order items, products, brands, categories, staffs, stores, and stocks. These tables represent both the sales side and the inventory side of the business.

### Python Workflow

I used Python with Pandas and NumPy for the complete data preparation process. First, I loaded all CSV files and performed data auditing. I checked null values, duplicates, datatypes, date formats, and relationship validity between tables. Then I cleaned the datasets by standardizing text fields, converting dates, normalizing emails and phone numbers, and creating useful analytical fields.

For example, I created gross sales, discount amount, net sales, shipment delay flags, shipping days, stock status, and inventory value. After cleaning, I exported all cleaned datasets and separate Power BI-ready fact and dimension tables.

### Data Model

For Power BI, I designed a star-schema model. The two fact tables are fact sales and fact inventory. The dimension tables are customers, products, stores, staffs, and date. This makes the dashboard easier to maintain and ensures KPI calculations are accurate.

### KPIs and Insights

The key KPIs include total sales, total orders, total customers, average order value, units sold, inventory value, low-stock products, and delayed orders. The project found total net sales of approximately 7.69 million across 1,615 orders. Trek was the top brand, Mountain Bikes was the top category, and Baldwin Bikes was the highest-performing store. The analysis also found 458 delayed completed orders and 190 low-stock inventory records.

### Dashboard

The Power BI dashboard is planned with three pages. The Executive Summary page shows overall KPIs, monthly sales trend, sales by store, brand, and category. The Product and Inventory page focuses on stock status, inventory value, low-stock products, and category performance. The Customer and Staff page shows staff performance, customer order frequency, and shipment delay analysis.

### Conclusion

Overall, this project demonstrates an end-to-end analytics workflow from raw data to business insights. It supports management decisions in sales strategy, inventory planning, staff evaluation, and fulfillment improvement.

## Likely Viva / Interview Questions and Answers

### 1. Why did you use Python before Power BI?

Python gives more control over data cleaning, validation, and feature engineering. I used it to standardize the raw data and create clean, reliable tables before loading them into Power BI.

### 2. What are the main KPIs in this project?

The main KPIs are total sales, gross sales, discount amount, total orders, total customers, average order value, units sold, inventory value, low-stock products, delayed orders, and delay rate.

### 3. What is the difference between gross sales and net sales?

Gross sales is quantity multiplied by list price before discount. Net sales is the final sales value after subtracting discount amount.

### 4. How did you handle missing shipped dates?

I did not blindly fill them. Missing shipped dates belong to non-completed orders such as pending, processing, or rejected orders, so I kept them as missing and added shipment status fields for analysis.

### 5. Why did you create a star schema?

A star schema makes the Power BI model cleaner and more scalable. Fact tables store numeric business events, while dimension tables store descriptive attributes. This improves filtering, relationships, and DAX calculations.

### 6. What are the fact tables in your model?

The fact tables are `fact_sales` and `fact_inventory`. `fact_sales` stores order-line sales metrics, while `fact_inventory` stores store-product stock metrics.

### 7. What are the dimension tables?

The dimension tables are `dim_customers`, `dim_products`, `dim_stores`, `dim_staffs`, and `dim_date`.

### 8. How do you identify low-stock products?

I classify stock records with quantity less than or equal to 5 as low stock. These products should be reviewed for replenishment.

### 9. How do you identify delayed orders?

An order is delayed if the shipped date is later than the required delivery date.

### 10. What business decision can be made from this dashboard?

Management can identify top-performing products and stores, reward high-performing staff, reduce shipment delays, and prioritize replenishment for low-stock products.

### 11. What was the biggest data quality issue?

The biggest missing-value issue was customer phone number availability. However, it did not affect sales analysis, so the records were retained.

### 12. How would you improve this project further?

I would add forecasting for product demand, customer segmentation, profitability analysis if cost data is available, and automated refresh in Power BI Service.
