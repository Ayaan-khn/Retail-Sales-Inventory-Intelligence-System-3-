"""Generate the presentation-ready Jupyter notebook for the project."""

from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks" / "retail_sales_inventory_powerbi_workflow.ipynb"


def markdown(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.strip().splitlines(keepends=True),
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.strip().splitlines(keepends=True),
    }


cells = [
    markdown(
        """
        # Retail Sales & Inventory Intelligence System

        **Objective:** Build a professional Python + Power BI analytics workflow for retail sales, fulfillment, customer, staff, product, and inventory performance.

        **Tools Used:** Python, Pandas, NumPy, CSV exports, Power BI.

        **Scope:** SQL is intentionally skipped. Python handles data cleaning, audit checks, feature engineering, and export of Power BI-ready tables.
        """
    ),
    markdown(
        """
        ## Business Context

        The business needs an end-to-end retail intelligence solution that helps management monitor:

        - Sales performance across stores, brands, categories, products, and staff.
        - Order fulfillment and shipment delays.
        - Customer order frequency and revenue contribution.
        - Inventory levels, low-stock products, and stock value.

        **Dataset note:** The provided files contain retail product, brand, category, order, customer, staff, store, and stock data. The analytics model is domain-agnostic and can represent mobile phones/laptops or any SKU-based retail catalog. The current source labels are preserved exactly for auditability.
        """
    ),
    markdown(
        """
        ## 1. Setup

        Import libraries and the modular project pipeline from `src/retail_analytics_pipeline.py`.
        """
    ),
    code(
        """
        from pathlib import Path
        import sys

        import numpy as np
        import pandas as pd

        PROJECT_ROOT = Path.cwd()
        if PROJECT_ROOT.name == "notebooks":
            PROJECT_ROOT = PROJECT_ROOT.parent

        sys.path.append(str(PROJECT_ROOT / "src"))

        from retail_analytics_pipeline import (
            RAW_DATA_DIR,
            PROCESSED_DATA_DIR,
            POWERBI_DATASET_DIR,
            REPORTS_DIR,
            audit_tables,
            build_insight_tables,
            build_powerbi_tables,
            clean_all_tables,
            load_raw_data,
            run_pipeline,
            validate_relationships,
        )

        pd.set_option("display.max_columns", 100)
        pd.set_option("display.float_format", "{:,.2f}".format)
        """
    ),
    markdown(
        """
        ## 2. Load Raw Data

        Load all nine CSV files into Pandas DataFrames.
        """
    ),
    code(
        """
        raw_tables = load_raw_data(RAW_DATA_DIR)

        table_inventory = pd.DataFrame(
            [
                {"table_name": name, "rows": len(df), "columns": df.shape[1]}
                for name, df in raw_tables.items()
            ]
        ).sort_values("table_name")

        table_inventory
        """
    ),
    markdown(
        """
        ## 3. Data Audit

        The audit checks row counts, duplicate rows, null values, and datatypes for every table.
        """
    ),
    code(
        """
        raw_audit = audit_tables(raw_tables)
        raw_audit
        """
    ),
    code(
        """
        for table_name, df in raw_tables.items():
            print(f"\\n--- {table_name.upper()} ---")
            print(df.head(3))
        """
    ),
    markdown(
        """
        ## 4. Data Cleaning

        Cleaning rules applied:

        - Standardized column names.
        - Trimmed text fields.
        - Lowercased emails.
        - Standardized phone and ZIP formatting.
        - Converted date fields to datetime.
        - Added readable order status labels.
        - Added shipment, late-delivery, and sales-calculation features.
        - Kept missing customer phone values because they do not block analytics.
        - Kept missing shipped dates for pending, processing, and rejected orders because those orders are not completed.
        """
    ),
    code(
        """
        cleaned_tables = clean_all_tables(raw_tables)
        cleaned_audit = audit_tables(cleaned_tables)
        cleaned_audit
        """
    ),
    markdown(
        """
        ## 5. Relationship Validation

        Validate conceptual primary-key and foreign-key relationships before building the Power BI model.
        """
    ),
    code(
        """
        relationship_validation = validate_relationships(cleaned_tables)
        relationship_validation
        """
    ),
    markdown(
        """
        ## 6. Power BI Star Schema

        The Power BI layer uses:

        - `fact_sales`: order-line level sales and fulfillment facts.
        - `fact_inventory`: store-product stock facts.
        - `dim_customers`: customer attributes.
        - `dim_products`: product, brand, and category attributes.
        - `dim_stores`: store and regional attributes.
        - `dim_staffs`: staff and manager attributes.
        - `dim_date`: calendar table for time intelligence.
        """
    ),
    code(
        """
        powerbi_tables = build_powerbi_tables(cleaned_tables)

        pd.DataFrame(
            [
                {"table_name": name, "rows": len(df), "columns": df.shape[1]}
                for name, df in powerbi_tables.items()
            ]
        )
        """
    ),
    markdown(
        """
        ## 7. KPI Engineering and Business Insights

        Generate executive KPI tables and supporting insight tables for Power BI validation.
        """
    ),
    code(
        """
        insight_tables = build_insight_tables(powerbi_tables)
        insight_tables["insight_executive_summary"]
        """
    ),
    code(
        """
        insight_tables["insight_brand_sales"].head(10)
        """
    ),
    code(
        """
        insight_tables["insight_category_sales"].head(10)
        """
    ),
    code(
        """
        insight_tables["insight_store_sales"]
        """
    ),
    code(
        """
        insight_tables["insight_staff_performance"].head(10)
        """
    ),
    code(
        """
        insight_tables["insight_low_stock_products"].head(20)
        """
    ),
    code(
        """
        insight_tables["insight_shipment_delay"]
        """
    ),
    markdown(
        """
        ## 8. Export Cleaned and Power BI-Ready Data

        Run the complete pipeline to export:

        - Cleaned CSVs into `data/processed_data`.
        - Power BI fact/dimension CSVs into `powerbi/dataset`.
        - Data quality audit outputs into `reports`.
        """
    ),
    code(
        """
        run_pipeline()
        """
    ),
    markdown(
        """
        ## 9. Power BI Build Checklist

        Import the CSVs from `powerbi/dataset` into Power BI Desktop.

        Recommended pages:

        1. **Executive Summary**: KPI cards, monthly trend, sales by store, sales by category, sales by brand.
        2. **Product & Inventory Analysis**: stock status, low-stock table, inventory value, brand/category drill-downs.
        3. **Customer & Staff Analysis**: staff leaderboard, customer frequency, shipment delay, customer geography.

        Use the DAX measures and relationship guidance provided in the `powerbi` folder.
        """
    ),
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.11",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}


def main() -> None:
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=2), encoding="utf-8")
    print(f"Notebook generated: {NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
