# Power BI Build Instructions

## Files To Import

Import these CSV files from `powerbi/dataset`:

- `fact_sales.csv`
- `fact_inventory.csv`
- `dim_customers.csv`
- `dim_products.csv`
- `dim_stores.csv`
- `dim_staffs.csv`
- `dim_date.csv`

The `insight_*.csv` files are supporting validation tables. You can import them if you want quick reference tables, but the main dashboard should use the fact and dimension tables above.

## Build Steps

1. Open Power BI Desktop.
2. Select **Get Data > Text/CSV**.
3. Import the seven main model tables.
4. Open **Model View** and create relationships from `docs/model_relationships.md`.
5. Mark `dim_date[date]` as the date table.
6. Create a dedicated `Measures` table.
7. Add the DAX measures from `docs/dax_measures.md`.
8. Import `retail_corporate_theme.json` from **View > Themes > Browse for themes**.
9. Build the three dashboard pages using `docs/dashboard_blueprint.md`.

## Recommended Pages

- Executive Summary
- Product & Inventory Analysis
- Customer & Staff Analysis

## Important Notes

- Use `fact_sales` for sales, order, customer, staff, and shipment KPIs.
- Use `fact_inventory` for stock, inventory value, and low-stock KPIs.
- Use dimension fields for slicers and chart categories.
- Do not sum `order_id`; use the `Total Orders` measure.
- Do not sum boolean delay flags from `fact_sales` directly because order lines can duplicate order-level information. Use the provided `Delayed Orders` measure.
