"""
Retail Sales & Inventory Intelligence System

Professional Python data engineering workflow for cleaning the raw retail CSV
files and preparing Power BI-ready analytics tables.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, Iterable

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw_data"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed_data"
POWERBI_DATASET_DIR = PROJECT_ROOT / "powerbi" / "dataset"
REPORTS_DIR = PROJECT_ROOT / "reports"

TABLE_FILES = {
    "brands": "brands.csv",
    "categories": "categories.csv",
    "customers": "customers.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "products": "products.csv",
    "staffs": "staffs.csv",
    "stocks": "stocks.csv",
    "stores": "stores.csv",
}

DTYPE_CONFIG = {
    "customers": {"phone": "string", "email": "string", "zip_code": "string"},
    "staffs": {"phone": "string", "email": "string"},
    "stores": {"phone": "string", "email": "string", "zip_code": "string"},
}

ORDER_STATUS_MAP = {
    1: "Pending",
    2: "Processing",
    3: "Rejected",
    4: "Completed",
}

LOW_STOCK_THRESHOLD = 5


def ensure_directories() -> None:
    """Create output folders used by the pipeline."""
    for folder in [PROCESSED_DATA_DIR, POWERBI_DATASET_DIR, REPORTS_DIR]:
        folder.mkdir(parents=True, exist_ok=True)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names to snake_case."""
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df


def trim_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim leading/trailing spaces in text columns."""
    df = df.copy()
    text_cols = df.select_dtypes(include=["object", "string"]).columns
    for column in text_cols:
        df[column] = df[column].astype("string").str.strip()
        df[column] = df[column].replace({"": pd.NA})
    return df


def normalize_phone(value: object) -> object:
    """Format 10-digit phone values consistently while preserving missing values."""
    if pd.isna(value):
        return pd.NA
    value_str = str(value).strip()
    digits = re.sub(r"\D", "", value_str)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return value_str if value_str else pd.NA


def normalize_zip(value: object) -> object:
    """Keep ZIP codes as text so leading zeros are not lost."""
    if pd.isna(value):
        return pd.NA
    value_str = str(value).strip().replace(".0", "")
    digits = re.sub(r"\D", "", value_str)
    return digits.zfill(5) if digits else pd.NA


def load_raw_data(raw_dir: Path = RAW_DATA_DIR) -> Dict[str, pd.DataFrame]:
    """Load all raw CSV files into a dictionary of DataFrames."""
    tables: Dict[str, pd.DataFrame] = {}
    for table_name, file_name in TABLE_FILES.items():
        path = raw_dir / file_name
        if not path.exists():
            raise FileNotFoundError(f"Missing required source file: {path}")
        dtype = DTYPE_CONFIG.get(table_name)
        tables[table_name] = standardize_column_names(pd.read_csv(path, dtype=dtype))
    return tables


def audit_tables(tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Create a compact data quality audit for all tables."""
    records = []
    for table_name, df in tables.items():
        null_counts = df.isna().sum()
        duplicate_rows = int(df.duplicated().sum())
        records.append(
            {
                "table_name": table_name,
                "rows": int(len(df)),
                "columns": int(df.shape[1]),
                "duplicate_rows": duplicate_rows,
                "columns_with_nulls": int((null_counts > 0).sum()),
                "total_null_values": int(null_counts.sum()),
                "null_detail": "; ".join(
                    f"{column}: {int(count)}"
                    for column, count in null_counts.items()
                    if count > 0
                )
                or "None",
                "data_types": "; ".join(f"{col}: {dtype}" for col, dtype in df.dtypes.items()),
            }
        )
    return pd.DataFrame(records)


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = trim_text_columns(df)
    df["first_name"] = df["first_name"].str.title()
    df["last_name"] = df["last_name"].str.title()
    df["customer_name"] = df["first_name"] + " " + df["last_name"]
    df["email"] = df["email"].str.lower()
    df["phone"] = df["phone"].apply(normalize_phone).astype("string")
    df["phone_available"] = df["phone"].notna()
    df["street"] = df["street"].str.title()
    df["city"] = df["city"].str.title()
    df["state"] = df["state"].str.upper()
    df["zip_code"] = df["zip_code"].apply(normalize_zip).astype("string")
    return df


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = trim_text_columns(df)
    for column in ["order_date", "required_date", "shipped_date"]:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    df["order_status_label"] = df["order_status"].map(ORDER_STATUS_MAP).fillna("Unknown")
    df["is_completed"] = df["order_status"].eq(4)
    df["is_shipped"] = df["shipped_date"].notna()
    df["required_lead_days"] = (df["required_date"] - df["order_date"]).dt.days
    df["shipping_days"] = (df["shipped_date"] - df["order_date"]).dt.days
    df["is_late"] = np.where(
        df["shipped_date"].notna(),
        df["shipped_date"] > df["required_date"],
        False,
    )
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["order_month_name"] = df["order_date"].dt.strftime("%b")
    df["order_month_start"] = df["order_date"].values.astype("datetime64[M]")
    return df


def clean_order_items(df: pd.DataFrame) -> pd.DataFrame:
    df = trim_text_columns(df)
    df["gross_sales"] = df["quantity"] * df["list_price"]
    df["discount_amount"] = df["gross_sales"] * df["discount"]
    df["net_sales"] = df["gross_sales"] - df["discount_amount"]
    df["unit_net_price"] = df["list_price"] * (1 - df["discount"])
    df["order_line_key"] = df["order_id"].astype(str) + "-" + df["item_id"].astype(str)
    return df


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    df = trim_text_columns(df)
    df["product_name"] = df["product_name"].str.replace(r"\s+", " ", regex=True)
    df["product_name_clean"] = df["product_name"].str.title()
    return df


def clean_staffs(df: pd.DataFrame) -> pd.DataFrame:
    df = trim_text_columns(df)
    df["first_name"] = df["first_name"].str.title()
    df["last_name"] = df["last_name"].str.title()
    df["staff_name"] = df["first_name"] + " " + df["last_name"]
    df["email"] = df["email"].str.lower()
    df["phone"] = df["phone"].apply(normalize_phone).astype("string")
    df["active_flag"] = df["active"].eq(1)
    return df


def clean_stores(df: pd.DataFrame) -> pd.DataFrame:
    df = trim_text_columns(df)
    df["store_name"] = df["store_name"].str.title()
    df["email"] = df["email"].str.lower()
    df["phone"] = df["phone"].apply(normalize_phone).astype("string")
    df["street"] = df["street"].str.title()
    df["city"] = df["city"].str.title()
    df["state"] = df["state"].str.upper()
    df["zip_code"] = df["zip_code"].apply(normalize_zip).astype("string")
    return df


def clean_lookup_table(df: pd.DataFrame, text_columns: Iterable[str]) -> pd.DataFrame:
    df = trim_text_columns(df)
    for column in text_columns:
        df[column] = df[column].str.replace(r"\s+", " ", regex=True).str.title()
    return df


def clean_stocks(df: pd.DataFrame) -> pd.DataFrame:
    df = trim_text_columns(df)
    df["stock_status"] = np.select(
        [
            df["quantity"].eq(0),
            df["quantity"].between(1, LOW_STOCK_THRESHOLD, inclusive="both"),
            df["quantity"].ge(20),
        ],
        ["Out of Stock", "Low Stock", "Healthy Stock"],
        default="Moderate Stock",
    )
    df["is_low_stock"] = df["quantity"].le(LOW_STOCK_THRESHOLD)
    return df


def clean_all_tables(tables: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Apply table-specific cleaning rules."""
    cleaned = {
        "brands": clean_lookup_table(tables["brands"], ["brand_name"]),
        "categories": clean_lookup_table(tables["categories"], ["category_name"]),
        "customers": clean_customers(tables["customers"]),
        "orders": clean_orders(tables["orders"]),
        "order_items": clean_order_items(tables["order_items"]),
        "products": clean_products(tables["products"]),
        "staffs": clean_staffs(tables["staffs"]),
        "stocks": clean_stocks(tables["stocks"]),
        "stores": clean_stores(tables["stores"]),
    }
    return cleaned


def validate_relationships(tables: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Validate foreign-key style relationships for the analytics model."""
    checks = [
        ("products", "brand_id", "brands", "brand_id"),
        ("products", "category_id", "categories", "category_id"),
        ("orders", "customer_id", "customers", "customer_id"),
        ("orders", "store_id", "stores", "store_id"),
        ("orders", "staff_id", "staffs", "staff_id"),
        ("order_items", "order_id", "orders", "order_id"),
        ("order_items", "product_id", "products", "product_id"),
        ("stocks", "store_id", "stores", "store_id"),
        ("stocks", "product_id", "products", "product_id"),
        ("staffs", "store_id", "stores", "store_id"),
    ]

    records = []
    for child, child_key, parent, parent_key in checks:
        child_values = set(tables[child][child_key].dropna().astype(int))
        parent_values = set(tables[parent][parent_key].dropna().astype(int))
        missing_values = sorted(child_values - parent_values)
        records.append(
            {
                "child_table": child,
                "child_key": child_key,
                "parent_table": parent,
                "parent_key": parent_key,
                "missing_key_count": len(missing_values),
                "status": "Pass" if not missing_values else "Review",
                "missing_key_sample": ", ".join(map(str, missing_values[:10])) or "None",
            }
        )
    return pd.DataFrame(records)


def build_date_dimension(date_columns: Iterable[pd.Series]) -> pd.DataFrame:
    dates = pd.concat(date_columns).dropna()
    date_range = pd.date_range(dates.min().normalize(), dates.max().normalize(), freq="D")
    dim_date = pd.DataFrame({"date": date_range})
    dim_date["date_key"] = dim_date["date"].dt.strftime("%Y%m%d").astype(int)
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["quarter"] = "Q" + dim_date["date"].dt.quarter.astype(str)
    dim_date["month_number"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.strftime("%B")
    dim_date["month_year"] = dim_date["date"].dt.strftime("%b %Y")
    dim_date["week_number"] = dim_date["date"].dt.isocalendar().week.astype(int)
    dim_date["day_name"] = dim_date["date"].dt.strftime("%A")
    return dim_date


def build_powerbi_tables(cleaned: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    products = cleaned["products"].merge(cleaned["brands"], on="brand_id", how="left")
    products = products.merge(cleaned["categories"], on="category_id", how="left")

    staffs = cleaned["staffs"].copy()
    manager_lookup = staffs[["staff_id", "staff_name"]].rename(
        columns={"staff_id": "manager_id", "staff_name": "manager_name"}
    )
    staffs = staffs.merge(manager_lookup, on="manager_id", how="left")

    fact_sales = cleaned["order_items"].merge(cleaned["orders"], on="order_id", how="left")
    fact_sales["order_date_key"] = fact_sales["order_date"].dt.strftime("%Y%m%d").astype(int)
    fact_sales["required_date_key"] = fact_sales["required_date"].dt.strftime("%Y%m%d").astype(int)
    fact_sales["shipped_date_key"] = (
        fact_sales["shipped_date"].dt.strftime("%Y%m%d").replace("NaT", pd.NA)
    )
    fact_sales["shipped_date_key"] = pd.to_numeric(fact_sales["shipped_date_key"], errors="coerce")

    fact_inventory = cleaned["stocks"].merge(
        products[["product_id", "product_name", "brand_name", "category_name", "list_price"]],
        on="product_id",
        how="left",
    )
    fact_inventory["inventory_value"] = fact_inventory["quantity"] * fact_inventory["list_price"]

    dim_date = build_date_dimension(
        [
            cleaned["orders"]["order_date"],
            cleaned["orders"]["required_date"],
            cleaned["orders"]["shipped_date"],
        ]
    )

    return {
        "dim_customers": cleaned["customers"],
        "dim_products": products,
        "dim_stores": cleaned["stores"],
        "dim_staffs": staffs,
        "dim_date": dim_date,
        "fact_sales": fact_sales,
        "fact_inventory": fact_inventory,
    }


def build_insight_tables(powerbi_tables: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    fact_sales = powerbi_tables["fact_sales"]
    fact_inventory = powerbi_tables["fact_inventory"]
    dim_products = powerbi_tables["dim_products"]
    dim_stores = powerbi_tables["dim_stores"]
    dim_staffs = powerbi_tables["dim_staffs"]
    dim_customers = powerbi_tables["dim_customers"]

    sales_enriched = (
        fact_sales.merge(dim_products[["product_id", "brand_name", "category_name"]], on="product_id", how="left")
        .merge(dim_stores[["store_id", "store_name", "state"]], on="store_id", how="left")
        .merge(dim_staffs[["staff_id", "staff_name"]], on="staff_id", how="left")
    )

    monthly_sales = (
        sales_enriched.groupby("order_month_start", as_index=False)
        .agg(total_sales=("net_sales", "sum"), total_orders=("order_id", "nunique"), units_sold=("quantity", "sum"))
        .sort_values("order_month_start")
    )

    brand_sales = (
        sales_enriched.groupby("brand_name", as_index=False)
        .agg(total_sales=("net_sales", "sum"), total_orders=("order_id", "nunique"), units_sold=("quantity", "sum"))
        .sort_values("total_sales", ascending=False)
    )

    category_sales = (
        sales_enriched.groupby("category_name", as_index=False)
        .agg(total_sales=("net_sales", "sum"), total_orders=("order_id", "nunique"), units_sold=("quantity", "sum"))
        .sort_values("total_sales", ascending=False)
    )

    store_sales = (
        sales_enriched.groupby(["store_id", "store_name", "state"], as_index=False)
        .agg(total_sales=("net_sales", "sum"), total_orders=("order_id", "nunique"), units_sold=("quantity", "sum"))
        .sort_values("total_sales", ascending=False)
    )

    staff_performance = (
        sales_enriched.groupby(["staff_id", "staff_name"], as_index=False)
        .agg(total_sales=("net_sales", "sum"), total_orders=("order_id", "nunique"), units_sold=("quantity", "sum"))
        .sort_values("total_sales", ascending=False)
    )
    staff_performance["average_order_value"] = (
        staff_performance["total_sales"] / staff_performance["total_orders"]
    )

    customer_frequency = (
        fact_sales.groupby("customer_id", as_index=False)
        .agg(total_orders=("order_id", "nunique"), total_sales=("net_sales", "sum"), units_purchased=("quantity", "sum"))
        .merge(dim_customers[["customer_id", "customer_name", "city", "state"]], on="customer_id", how="left")
        .sort_values(["total_orders", "total_sales"], ascending=False)
    )

    low_stock_products = (
        fact_inventory[fact_inventory["quantity"].le(LOW_STOCK_THRESHOLD)]
        .merge(dim_stores[["store_id", "store_name", "state"]], on="store_id", how="left")
        .sort_values(["quantity", "inventory_value"], ascending=[True, False])
    )

    shipment_delay = (
        fact_sales.drop_duplicates("order_id")
        .groupby(["order_status_label"], as_index=False)
        .agg(
            total_orders=("order_id", "nunique"),
            shipped_orders=("is_shipped", "sum"),
            delayed_orders=("is_late", "sum"),
            avg_shipping_days=("shipping_days", "mean"),
        )
    )

    executive_summary = pd.DataFrame(
        [
            ("Total Sales", fact_sales["net_sales"].sum()),
            ("Gross Sales", fact_sales["gross_sales"].sum()),
            ("Discount Amount", fact_sales["discount_amount"].sum()),
            ("Total Orders", fact_sales["order_id"].nunique()),
            ("Total Customers", fact_sales["customer_id"].nunique()),
            ("Average Order Value", fact_sales["net_sales"].sum() / fact_sales["order_id"].nunique()),
            ("Units Sold", fact_sales["quantity"].sum()),
            ("Late Shipments", fact_sales.drop_duplicates("order_id")["is_late"].sum()),
            ("Low Stock Rows", int((fact_inventory["quantity"] <= LOW_STOCK_THRESHOLD).sum())),
            ("Inventory Value", fact_inventory["inventory_value"].sum()),
        ],
        columns=["metric", "value"],
    )

    return {
        "insight_executive_summary": executive_summary,
        "insight_monthly_sales": monthly_sales,
        "insight_brand_sales": brand_sales,
        "insight_category_sales": category_sales,
        "insight_store_sales": store_sales,
        "insight_staff_performance": staff_performance,
        "insight_customer_frequency": customer_frequency,
        "insight_low_stock_products": low_stock_products,
        "insight_shipment_delay": shipment_delay,
    }


def export_tables(tables: Dict[str, pd.DataFrame], output_dir: Path, suffix: str = "") -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for table_name, df in tables.items():
        file_name = f"{table_name}{suffix}.csv"
        df.to_csv(output_dir / file_name, index=False)


def export_audit_outputs(raw_tables: Dict[str, pd.DataFrame], cleaned_tables: Dict[str, pd.DataFrame]) -> None:
    raw_audit = audit_tables(raw_tables)
    cleaned_audit = audit_tables(cleaned_tables)
    relationship_validation = validate_relationships(cleaned_tables)

    raw_audit.to_csv(REPORTS_DIR / "raw_data_audit.csv", index=False)
    cleaned_audit.to_csv(REPORTS_DIR / "cleaned_data_audit.csv", index=False)
    relationship_validation.to_csv(REPORTS_DIR / "relationship_validation.csv", index=False)

    audit_summary = {
        "raw_tables": len(raw_tables),
        "cleaned_tables": len(cleaned_tables),
        "raw_total_rows": int(sum(len(df) for df in raw_tables.values())),
        "cleaned_total_rows": int(sum(len(df) for df in cleaned_tables.values())),
        "relationship_checks_failed": int((relationship_validation["status"] != "Pass").sum()),
    }
    (REPORTS_DIR / "pipeline_summary.json").write_text(json.dumps(audit_summary, indent=2))


def run_pipeline() -> None:
    ensure_directories()
    raw_tables = load_raw_data()
    cleaned_tables = clean_all_tables(raw_tables)
    powerbi_tables = build_powerbi_tables(cleaned_tables)
    insight_tables = build_insight_tables(powerbi_tables)

    export_tables(cleaned_tables, PROCESSED_DATA_DIR, suffix="_clean")
    export_tables(powerbi_tables, POWERBI_DATASET_DIR)
    export_tables(insight_tables, POWERBI_DATASET_DIR)
    export_audit_outputs(raw_tables, cleaned_tables)

    print("Retail analytics pipeline completed successfully.")
    print(f"Cleaned CSVs: {PROCESSED_DATA_DIR}")
    print(f"Power BI dataset CSVs: {POWERBI_DATASET_DIR}")
    print(f"Audit outputs: {REPORTS_DIR}")


if __name__ == "__main__":
    run_pipeline()
