# Power BI Data Model Guide

## Recommended Model Type

Use a star-schema style model with two fact tables and supporting dimensions.

## Fact Tables

### `fact_sales`

Grain: one row per order line item.

Primary analytical fields:

- `order_line_key`
- `order_id`
- `item_id`
- `product_id`
- `customer_id`
- `store_id`
- `staff_id`
- `order_date`
- `required_date`
- `shipped_date`
- `quantity`
- `list_price`
- `discount`
- `gross_sales`
- `discount_amount`
- `net_sales`
- `order_status_label`
- `is_late`
- `shipping_days`

### `fact_inventory`

Grain: one row per store-product stock record.

Primary analytical fields:

- `store_id`
- `product_id`
- `quantity`
- `stock_status`
- `is_low_stock`
- `inventory_value`

## Dimension Tables

### `dim_customers`

Primary key: `customer_id`

Use for customer name, city, state, ZIP, contact availability, and customer-level slicing.

### `dim_products`

Primary key: `product_id`

Use for product name, brand, category, model year, and product price analysis.

### `dim_stores`

Primary key: `store_id`

Use for store name, city, state, and regional/store-level filtering.

### `dim_staffs`

Primary key: `staff_id`

Use for sales staff performance and manager hierarchy.

### `dim_date`

Primary key: `date_key`

Use as the official date table for trends, month/quarter/year slicing, and time intelligence.

## Relationships To Create

Create these relationships in Power BI Model View.

| From Table | From Column | To Table | To Column | Cardinality | Filter Direction |
|---|---|---|---|---|---|
| `fact_sales` | `customer_id` | `dim_customers` | `customer_id` | Many-to-one | Single |
| `fact_sales` | `product_id` | `dim_products` | `product_id` | Many-to-one | Single |
| `fact_sales` | `store_id` | `dim_stores` | `store_id` | Many-to-one | Single |
| `fact_sales` | `staff_id` | `dim_staffs` | `staff_id` | Many-to-one | Single |
| `fact_sales` | `order_date_key` | `dim_date` | `date_key` | Many-to-one | Single |
| `fact_inventory` | `product_id` | `dim_products` | `product_id` | Many-to-one | Single |
| `fact_inventory` | `store_id` | `dim_stores` | `store_id` | Many-to-one | Single |

## Optional Inactive Date Relationships

You can optionally create inactive relationships for fulfillment analysis:

| From Table | From Column | To Table | To Column | Purpose |
|---|---|---|---|---|
| `fact_sales` | `required_date_key` | `dim_date` | `date_key` | Required delivery trend |
| `fact_sales` | `shipped_date_key` | `dim_date` | `date_key` | Shipment trend |

Use `USERELATIONSHIP()` in advanced DAX if you need visuals by shipped date or required date.

## Modeling Rules

- Mark `dim_date[date]` as the official date table.
- Keep cross-filter direction as single unless a visual truly requires otherwise.
- Hide technical keys in report view after relationships are built.
- Use measures for KPIs instead of dragging raw numeric columns into cards.
- Use `fact_sales` for revenue and order metrics.
- Use `fact_inventory` for stock and inventory metrics.
