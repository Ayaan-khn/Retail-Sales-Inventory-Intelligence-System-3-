# Power BI Dashboard Blueprint

## Report Title

Retail Sales & Inventory Intelligence System

## Theme Direction

Use a corporate retail analytics look:

- Background: `#F7F8FA`
- Primary text: `#1F2937`
- Primary accent: `#2563EB`
- Secondary accent: `#0F766E`
- Alert accent: `#DC2626`
- Warning accent: `#D97706`
- Success accent: `#16A34A`

Design rules:

- Use a clean light background.
- Keep KPI cards aligned across the top.
- Avoid too many colors in one visual.
- Use red/orange only for delay and low-stock alerts.
- Use slicers consistently on each page.

## Page 1: Executive Summary

Purpose: Give management a quick view of overall sales performance and business health.

### Top KPI Cards

Place five cards across the top:

1. `Total Sales`
2. `Total Orders`
3. `Total Customers`
4. `Average Order Value`
5. `Units Sold`

### Main Visuals

| Visual | Fields / Measures | Placement |
|---|---|---|
| Line chart | `dim_date[month_year]`, `Total Sales` | Center-left, largest visual |
| Clustered bar chart | `dim_stores[store_name]`, `Total Sales` | Top-right |
| Bar chart | `dim_products[category_name]`, `Total Sales` | Bottom-left |
| Bar chart | `dim_products[brand_name]`, `Total Sales` | Bottom-center |
| Donut chart | `fact_sales[order_status_label]`, `Total Orders` | Bottom-right |

### Slicers

- `dim_date[year]`
- `dim_stores[state]`
- `dim_stores[store_name]`
- `dim_products[category_name]`
- `dim_products[brand_name]`

### Drill-Down

Enable drill-down from category to product using:

1. `dim_products[category_name]`
2. `dim_products[brand_name]`
3. `dim_products[product_name]`

## Page 2: Product & Inventory Analysis

Purpose: Help inventory and category managers identify product performance, inventory risks, and stock value.

### Top KPI Cards

1. `Inventory Quantity`
2. `Inventory Value`
3. `Low Stock Rows`
4. `Out of Stock Rows`
5. `Low Stock %`

### Main Visuals

| Visual | Fields / Measures | Placement |
|---|---|---|
| Matrix | `dim_stores[store_name]`, `dim_products[category_name]`, `Inventory Quantity`, `Inventory Value` | Left side |
| Bar chart | `dim_products[brand_name]`, `Total Sales` | Top-right |
| Bar chart | `dim_products[category_name]`, `Units Sold` | Middle-right |
| Table | `dim_products[product_name]`, `dim_stores[store_name]`, `fact_inventory[quantity]`, `fact_inventory[stock_status]` | Bottom |
| Donut chart | `fact_inventory[stock_status]`, `Inventory Quantity` | Right side |

### Conditional Formatting

Apply color rules to `fact_inventory[quantity]`:

- `0`: red
- `1-5`: orange
- `6-19`: neutral gray/blue
- `20+`: green

### Filters

- Stock status
- Store
- Brand
- Category

## Page 3: Customer & Staff Analysis

Purpose: Show customer concentration, staff contribution, and fulfillment quality.

### Top KPI Cards

1. `Total Customers`
2. `Orders Per Customer`
3. `Revenue Per Customer`
4. `Completed Orders`
5. `Delay Rate`

### Main Visuals

| Visual | Fields / Measures | Placement |
|---|---|---|
| Bar chart | `dim_staffs[staff_name]`, `Total Sales` | Left side |
| Bar chart | `dim_staffs[staff_name]`, `Total Orders` | Right side |
| Table | `dim_customers[customer_name]`, `Total Orders`, `Total Sales`, `Units Sold` | Bottom-left |
| Map visual | `dim_customers[state]`, `Total Sales` | Top-center, if map permissions are available |
| Bar chart | `fact_sales[order_status_label]`, `Total Orders` | Bottom-right |
| KPI or gauge | `On Time Shipment Rate` | Near shipment visuals |

### Slicers

- Year
- Store
- Staff
- Customer state
- Order status

## Suggested Report Interactions

- Selecting a brand should filter sales trend, category performance, and inventory.
- Selecting a store should filter staff, customers, sales, and inventory.
- Selecting a year/month should filter all revenue, order, and shipment visuals.
- Use tooltip pages for product-level detail if time allows.

## Tooltip Suggestions

For product visuals, show:

- Product name
- Brand
- Category
- Total Sales
- Units Sold
- Inventory Quantity
- Low Stock %

For staff visuals, show:

- Staff name
- Store
- Total Sales
- Total Orders
- Average Order Value
- Delay Rate

## Evaluation Talking Points

- The dashboard separates executive, inventory, and operational analysis.
- Measures are DAX-based, so KPIs respond dynamically to slicers.
- The model uses a star-schema approach for clean relationships and reliable aggregation.
- Inventory and shipment pages support action, not only reporting.
