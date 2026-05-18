# Power BI DAX Measures

Create a dedicated table called `Measures` in Power BI and add these measures there.

## Sales KPIs

```DAX
Total Sales = SUM(fact_sales[net_sales])
```

```DAX
Gross Sales = SUM(fact_sales[gross_sales])
```

```DAX
Discount Amount = SUM(fact_sales[discount_amount])
```

```DAX
Discount Rate = DIVIDE([Discount Amount], [Gross Sales])
```

```DAX
Total Orders = DISTINCTCOUNT(fact_sales[order_id])
```

```DAX
Total Customers = DISTINCTCOUNT(fact_sales[customer_id])
```

```DAX
Units Sold = SUM(fact_sales[quantity])
```

```DAX
Average Order Value = DIVIDE([Total Sales], [Total Orders])
```

```DAX
Average Selling Price = DIVIDE([Total Sales], [Units Sold])
```

## Time Intelligence

```DAX
Sales YTD =
TOTALYTD(
    [Total Sales],
    dim_date[date]
)
```

```DAX
Orders YTD =
TOTALYTD(
    [Total Orders],
    dim_date[date]
)
```

```DAX
Sales Previous Month =
CALCULATE(
    [Total Sales],
    DATEADD(dim_date[date], -1, MONTH)
)
```

```DAX
Monthly Sales Growth % =
DIVIDE(
    [Total Sales] - [Sales Previous Month],
    [Sales Previous Month]
)
```

## Product and Category Performance

```DAX
Sales Contribution % =
DIVIDE(
    [Total Sales],
    CALCULATE([Total Sales], ALL(dim_products))
)
```

```DAX
Average Units Per Order =
DIVIDE([Units Sold], [Total Orders])
```

```DAX
Products Sold = DISTINCTCOUNT(fact_sales[product_id])
```

## Inventory Measures

```DAX
Inventory Quantity = SUM(fact_inventory[quantity])
```

```DAX
Inventory Value = SUM(fact_inventory[inventory_value])
```

```DAX
Low Stock Rows =
CALCULATE(
    COUNTROWS(fact_inventory),
    fact_inventory[quantity] <= 5
)
```

```DAX
Out of Stock Rows =
CALCULATE(
    COUNTROWS(fact_inventory),
    fact_inventory[quantity] = 0
)
```

```DAX
Low Stock % =
DIVIDE(
    [Low Stock Rows],
    COUNTROWS(fact_inventory)
)
```

```DAX
Average Stock Quantity = AVERAGE(fact_inventory[quantity])
```

## Staff and Customer Measures

```DAX
Orders Per Customer =
DIVIDE([Total Orders], [Total Customers])
```

```DAX
Revenue Per Customer =
DIVIDE([Total Sales], [Total Customers])
```

```DAX
Staff Count = DISTINCTCOUNT(dim_staffs[staff_id])
```

```DAX
Sales Per Staff =
DIVIDE([Total Sales], [Staff Count])
```

## Shipment and Fulfillment Measures

```DAX
Completed Orders =
CALCULATE(
    DISTINCTCOUNT(fact_sales[order_id]),
    fact_sales[order_status_label] = "Completed"
)
```

```DAX
Pending Orders =
CALCULATE(
    DISTINCTCOUNT(fact_sales[order_id]),
    fact_sales[order_status_label] = "Pending"
)
```

```DAX
Processing Orders =
CALCULATE(
    DISTINCTCOUNT(fact_sales[order_id]),
    fact_sales[order_status_label] = "Processing"
)
```

```DAX
Rejected Orders =
CALCULATE(
    DISTINCTCOUNT(fact_sales[order_id]),
    fact_sales[order_status_label] = "Rejected"
)
```

```DAX
Delayed Orders =
CALCULATE(
    DISTINCTCOUNT(fact_sales[order_id]),
    fact_sales[is_late] = TRUE()
)
```

```DAX
Delay Rate =
DIVIDE([Delayed Orders], [Completed Orders])
```

```DAX
Average Shipping Days =
AVERAGEX(
    VALUES(fact_sales[order_id]),
    CALCULATE(MAX(fact_sales[shipping_days]))
)
```

```DAX
On Time Orders =
[Completed Orders] - [Delayed Orders]
```

```DAX
On Time Shipment Rate =
DIVIDE([On Time Orders], [Completed Orders])
```

## Formatting Recommendations

Format these as currency:

- `Total Sales`
- `Gross Sales`
- `Discount Amount`
- `Average Order Value`
- `Average Selling Price`
- `Inventory Value`
- `Revenue Per Customer`
- `Sales Per Staff`

Format these as percentages:

- `Discount Rate`
- `Monthly Sales Growth %`
- `Sales Contribution %`
- `Low Stock %`
- `Delay Rate`
- `On Time Shipment Rate`
