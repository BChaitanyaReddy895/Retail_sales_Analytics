from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import pandas as pd

from utils import (
    coerce_datetime,
    coerce_numeric,
    fill_numeric,
    fill_text,
    normalize_dataframe_columns,
    setup_logger,
    standardize_string_series,
    write_dataframe,
)


@dataclass(frozen=True)
class TransformResult:
    tables: Dict[str, pd.DataFrame]
    analytics: Dict[str, pd.DataFrame]


def _clean_customers(frame: pd.DataFrame) -> pd.DataFrame:
    frame = normalize_dataframe_columns(frame).drop_duplicates()
    frame = fill_text(frame, ["customer_name", "email", "segment"], "unknown")
    frame = coerce_datetime(frame, ["signup_date"])
    if "segment" in frame.columns:
        frame["segment"] = standardize_string_series(frame["segment"]).fillna("unknown")
    return frame


def _clean_products(frame: pd.DataFrame) -> pd.DataFrame:
    frame = normalize_dataframe_columns(frame).drop_duplicates()
    frame = fill_text(frame, ["product_name", "category"], "unknown")
    frame = coerce_numeric(frame, ["unit_cost", "unit_price"])
    frame = fill_numeric(frame, ["unit_cost", "unit_price"], 0.0)
    return frame


def _clean_inventory(frame: pd.DataFrame) -> pd.DataFrame:
    frame = normalize_dataframe_columns(frame).drop_duplicates()
    frame = coerce_datetime(frame, ["last_restock_date"])
    frame = coerce_numeric(frame, ["stock_on_hand", "reorder_level"])
    frame = fill_numeric(frame, ["stock_on_hand", "reorder_level"], 0)
    return frame


def _clean_regions(frame: pd.DataFrame) -> pd.DataFrame:
    frame = normalize_dataframe_columns(frame).drop_duplicates()
    frame = fill_text(frame, ["region_name", "country"], "unknown")
    return frame


def _clean_sales(frame: pd.DataFrame) -> pd.DataFrame:
    frame = normalize_dataframe_columns(frame).drop_duplicates()
    frame = coerce_datetime(frame, ["sale_date"])
    frame = coerce_numeric(frame, ["quantity", "unit_price", "unit_cost", "discount_rate", "revenue", "cost", "profit"])
    frame = fill_numeric(frame, ["quantity", "unit_price", "unit_cost", "discount_rate", "revenue", "cost", "profit"], 0.0)
    frame["discount_rate"] = frame["discount_rate"].clip(lower=0, upper=0.5)
    if "sale_date" in frame.columns:
        frame["sale_month"] = frame["sale_date"].dt.to_period("M").astype(str)
    frame["gross_revenue"] = (frame["quantity"] * frame["unit_price"]).round(2)
    frame["net_revenue"] = (frame["gross_revenue"] * (1 - frame["discount_rate"])).round(2)
    frame["revenue"] = frame["gross_revenue"]
    frame["cost"] = (frame["quantity"] * frame["unit_cost"]).round(2)
    frame["profit"] = (frame["net_revenue"] - frame["cost"]).round(2)
    frame["profit_margin"] = frame.apply(
        lambda row: round(row["profit"] / row["net_revenue"], 4) if row["net_revenue"] else 0.0,
        axis=1,
    )
    return frame


def transform_tables(raw_tables: Dict[str, pd.DataFrame], processed_dir: Path, logger=None) -> TransformResult:
    logger = logger or setup_logger("transform", processed_dir.parent / "logs")

    cleaned_tables: Dict[str, pd.DataFrame] = {}
    for table_name, frame in raw_tables.items():
        if table_name == "customers":
            cleaned_tables[table_name] = _clean_customers(frame)
        elif table_name == "products":
            cleaned_tables[table_name] = _clean_products(frame)
        elif table_name == "sales":
            cleaned_tables[table_name] = _clean_sales(frame)
        elif table_name == "inventory":
            cleaned_tables[table_name] = _clean_inventory(frame)
        elif table_name == "regions":
            cleaned_tables[table_name] = _clean_regions(frame)
        else:
            cleaned_tables[table_name] = normalize_dataframe_columns(frame).drop_duplicates()

        write_dataframe(cleaned_tables[table_name], processed_dir / f"{table_name}.csv")
        logger.info("Transformed %s with %s rows", table_name, len(cleaned_tables[table_name]))

    sales = cleaned_tables.get("sales", pd.DataFrame())
    customers = cleaned_tables.get("customers", pd.DataFrame())
    products = cleaned_tables.get("products", pd.DataFrame())
    inventory = cleaned_tables.get("inventory", pd.DataFrame())
    regions = cleaned_tables.get("regions", pd.DataFrame())

    analytics: Dict[str, pd.DataFrame] = {}
    if not sales.empty:
        analytics["monthly_revenue"] = (
            sales.groupby("sale_month", as_index=False)["net_revenue"].sum().rename(columns={"net_revenue": "monthly_revenue"})
        )
        if not products.empty:
            analytics["top_selling_products"] = (
                sales.groupby("product_id", as_index=False)
                .agg(total_revenue=("net_revenue", "sum"), units_sold=("quantity", "sum"))
                .merge(products[["product_id", "product_name", "category"]], on="product_id", how="left")
                .sort_values("total_revenue", ascending=False)
            )
            analytics["inventory_turnover"] = (
                inventory.merge(
                    sales.groupby("product_id", as_index=False)["quantity"].sum(),
                    on="product_id",
                    how="left",
                )
                .merge(products[["product_id", "product_name"]], on="product_id", how="left")
                .fillna({"quantity": 0})
            )
            analytics["inventory_turnover"]["inventory_turnover"] = analytics["inventory_turnover"].apply(
                lambda row: round(row["quantity"] / row["stock_on_hand"], 2) if row.get("stock_on_hand", 0) else 0.0,
                axis=1,
            )

        if not customers.empty:
            analytics["customer_lifetime_value"] = (
                sales.groupby("customer_id", as_index=False)["net_revenue"].sum().rename(columns={"net_revenue": "customer_lifetime_value"})
                .merge(customers[["customer_id", "customer_name", "segment", "region_id"]], on="customer_id", how="left")
            )

        if not regions.empty:
            analytics["regional_sales"] = (
                sales.groupby("region_id", as_index=False)
                .agg(regional_sales=("net_revenue", "sum"), profit=("profit", "sum"), orders=("sale_id", "count"))
                .merge(regions[["region_id", "region_name"]], on="region_id", how="left")
            )

    return TransformResult(tables=cleaned_tables, analytics=analytics)


def validate_transformed_tables(result: TransformResult) -> list[str]:
    issues: list[str] = []
    required_tables = ["customers", "products", "sales", "inventory", "regions"]
    for table_name in required_tables:
        if table_name not in result.tables:
            issues.append(f"Missing required table: {table_name}")
            continue
        if result.tables[table_name].empty:
            issues.append(f"Table is empty: {table_name}")

    sales = result.tables.get("sales")
    if sales is not None and not sales.empty:
        if (sales["quantity"] < 0).any():
            issues.append("Sales contains negative quantity values")
        if sales["sale_date"].isna().any():
            issues.append("Sales contains invalid sale_date values")

    return issues
