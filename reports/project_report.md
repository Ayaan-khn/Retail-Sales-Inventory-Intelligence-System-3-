# Retail Sales & Inventory Intelligence System

## 1. Project Summary

This project delivers a Python and Power BI based retail analytics solution for monitoring sales, inventory, customers, staff performance, and order fulfillment. The solution follows a professional analytics workflow: raw data ingestion, data quality auditing, cleaning, feature engineering, star-schema modeling, KPI creation, and dashboard planning.

SQL is intentionally excluded from this implementation. Python handles the complete data preparation layer, and Power BI handles interactive business reporting.

## 2. Problem Statement

A retail company needs a centralized intelligence system to understand business performance across products, stores, customers, staff, and inventory. Management wants to identify revenue drivers, monitor stock risk, track delayed shipments, evaluate staff contribution, and support better commercial decisions.

## 3. Business Objectives

- Track total sales, order volume, customer count, and average order value.
- Identify top-performing brands, categories, products, stores, and staff.
- Monitor monthly sales trends and seasonal movement.
- Detect low-stock and out-of-stock inventory.
- Analyze customer order frequency and concentration.
- Measure shipment delays against required delivery dates.
- Prepare clean datasets for Power BI dashboarding.

## 4. Dataset Explanation

The dataset contains 9 relational CSV files:

| Table | Business Meaning |
|---|---|
| `customers` | Customer profile and location details |
| `orders` | Order header, date, status, customer, store, and staff details |
| `order_items` | Product-level order line items, quantity, price, and discount |
| `products` | Product catalog with brand, category, model year, and price |
| `brands` | Brand lookup table |
| `categories` | Product category lookup table |
| `staffs` | Staff profile, active status, store, and manager details |
| `stores` | Store location and contact details |
| `stocks` | Store-product inventory quantity |

Dataset note: The business framing is SKU-based retail analytics. The actual source product labels are preserved for accuracy and auditability; the same model applies to mobile phones, laptops, accessories, or any retail product catalog.

## 5. Data Cleaning Process

Python was used to load, audit, clean, validate, and export the data.

### Audit Checks Performed

- Row and column count validation.
- Null-value detection.
- Duplicate-row detection.
- Datatype checks.
- Primary-key uniqueness checks.
- Foreign-key style relationship checks.
- Date consistency checks.
- Numeric range checks for quantity, price, and discount.

### Key Cleaning Decisions

- Customer phone numbers were standardized where available.
- Missing customer phone values were retained because they do not affect sales analytics.
- Email fields were lowercased.
- Text fields were trimmed and standardized.
- ZIP codes were stored as text to preserve formatting.
- `order_date`, `required_date`, and `shipped_date` were converted to date format.
- Missing `shipped_date` values were retained for non-completed orders.
- Order status codes were mapped to readable labels: Pending, Processing, Rejected, Completed.
- Sales fields were engineered at order-line level:
  - `gross_sales`
  - `discount_amount`
  - `net_sales`
  - `unit_net_price`
- Shipment fields were engineered:
  - `is_shipped`
  - `shipping_days`
  - `is_late`
  - `required_lead_days`
- Inventory fields were engineered:
  - `stock_status`
  - `is_low_stock`
  - `inventory_value`

## 6. Data Modeling Methodology

The Power BI model follows a star-schema style design.

### Fact Tables

- `fact_sales`: order-line level sales, discount, order, customer, product, store, staff, and shipment metrics.
- `fact_inventory`: store-product inventory quantity, stock status, and inventory value.

### Dimension Tables

- `dim_customers`
- `dim_products`
- `dim_stores`
- `dim_staffs`
- `dim_date`

This structure improves reporting performance, reduces relationship complexity, and keeps KPI calculations reliable.

## 7. KPI Definitions

| KPI | Definition |
|---|---|
| Total Sales | Sum of net sales after discount |
| Gross Sales | Quantity multiplied by list price before discount |
| Discount Amount | Gross sales minus net sales |
| Total Orders | Distinct order count |
| Total Customers | Distinct customer count |
| Average Order Value | Total sales divided by total orders |
| Units Sold | Sum of item quantities |
| Inventory Value | Stock quantity multiplied by product price |
| Low Stock Rows | Store-product stock records with quantity less than or equal to 5 |
| Delayed Orders | Completed orders where shipped date is after required date |
| Delay Rate | Delayed orders divided by completed orders |

## 8. Analytical Results

### Executive KPIs

| Metric | Value |
|---|---:|
| Total Sales | 7,689,116.56 |
| Gross Sales | 8,578,988.88 |
| Discount Amount | 889,872.32 |
| Total Orders | 1,615 |
| Total Customers | 1,445 |
| Average Order Value | 4,761.06 |
| Units Sold | 7,078 |
| Late Shipments | 458 |
| Low Stock Rows | 190 |
| Inventory Value | 19,819,584.85 |

### Top Brands by Sales

| Brand | Total Sales |
|---|---:|
| Trek | 4,602,754.35 |
| Electra | 1,205,320.82 |
| Surly | 949,507.06 |
| Sun Bicycles | 341,994.93 |
| Haro | 185,384.55 |

### Top Categories by Sales

| Category | Total Sales |
|---|---:|
| Mountain Bikes | 2,715,079.53 |
| Road Bikes | 1,665,098.49 |
| Cruisers Bicycles | 995,032.62 |
| Electric Bikes | 916,684.78 |
| Cyclocross Bicycles | 711,011.84 |

### Top Stores by Sales

| Store | State | Total Sales |
|---|---|---:|
| Baldwin Bikes | NY | 5,215,751.28 |
| Santa Cruz Bikes | CA | 1,605,823.04 |
| Rowlett Bikes | TX | 867,542.24 |

### Top Staff by Sales

| Staff | Total Sales | Orders |
|---|---:|---:|
| Marcelene Boyer | 2,624,120.65 | 553 |
| Venita Daniel | 2,591,630.62 | 540 |
| Genna Serrano | 853,287.36 | 184 |
| Mireya Copeland | 752,535.68 | 164 |
| Kali Vargas | 463,918.30 | 88 |

## 9. Dashboard Explanation

The Power BI dashboard is designed with three pages.

### Page 1: Executive Summary

This page gives leadership a quick business overview with KPI cards, monthly sales trend, sales by brand, sales by category, sales by store, and order status distribution.

### Page 2: Product & Inventory Analysis

This page focuses on product movement and inventory risk. It includes inventory quantity, inventory value, stock status, low-stock products, sales by brand/category, and store-level stock comparison.

### Page 3: Customer & Staff Analysis

This page highlights customer order behavior, top customers, staff sales performance, staff order contribution, and shipment delay metrics.

## 10. Final Insights

- Total net sales reached 7.69M across 1,615 orders.
- Baldwin Bikes is the strongest store, contributing the highest sales volume.
- Trek is the dominant brand by revenue.
- Mountain Bikes is the highest-performing category.
- Staff performance is concentrated among top employees, especially Marcelene Boyer and Venita Daniel.
- 458 completed orders were shipped after the required date, making shipment delay analysis important.
- 190 store-product inventory records are low stock, creating a clear replenishment opportunity.
- The business should prioritize inventory planning for high-selling categories and improve fulfillment processes to reduce delivery delays.

## 11. Conclusion

This project converts raw retail CSV files into a clean, structured, and dashboard-ready analytics solution. Python ensures reliable data cleaning and feature engineering, while Power BI provides interactive KPI monitoring for decision-makers. The final solution supports executive reporting, product analysis, inventory control, customer analysis, staff evaluation, and shipment monitoring.
