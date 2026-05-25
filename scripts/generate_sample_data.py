from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from config import load_settings
from utils import ensure_directory, write_dataframe


FIRST_NAMES = [
    "Aarav",
    "Aditya",
    "Aisha",
    "Ananya",
    "Arjun",
    "Diya",
    "Ishaan",
    "Kabir",
    "Kavya",
    "Meera",
    "Maya",
    "Neha",
    "Nikhil",
    "Priya",
    "Rohan",
    "Sana",
    "Sara",
    "Vihaan",
]

LAST_NAMES = [
    "Bansal",
    "Chatterjee",
    "Das",
    "Gupta",
    "Iyer",
    "Kapoor",
    "Khan",
    "Kulkarni",
    "Mishra",
    "Nair",
    "Patel",
    "Rao",
    "Sharma",
    "Singh",
    "Verma",
]

PRODUCT_CATALOG = [
    ("P1001", "Wireless Mouse", "Accessories", 11.50, 24.99),
    ("P1002", "Mechanical Keyboard", "Accessories", 29.80, 59.99),
    ("P1003", "USB-C Hub", "Accessories", 14.20, 31.99),
    ("P1004", "Laptop Stand", "Accessories", 18.40, 39.99),
    ("P1005", "Webcam 1080p", "Electronics", 22.00, 49.99),
    ("P1006", "Noise Cancelling Headset", "Electronics", 41.20, 89.99),
    ("P1007", "16GB USB Drive", "Accessories", 4.90, 12.99),
    ("P1008", "Portable SSD 1TB", "Electronics", 68.50, 119.99),
    ("P1009", "Office Chair", "Furniture", 84.00, 159.99),
    ("P1010", "Standing Desk", "Furniture", 162.00, 279.99),
    ("P1011", "Desk Lamp", "Furniture", 13.30, 29.99),
    ("P1012", "File Organizer", "Office", 6.10, 14.99),
    ("P1013", "Notebook Pack", "Office", 3.20, 9.99),
    ("P1014", "Ballpoint Pen Set", "Office", 2.40, 7.99),
    ("P1015", "Sticky Notes Pack", "Office", 1.80, 5.99),
    ("P1016", "Printer Paper Ream", "Office", 4.10, 10.99),
    ("P1017", "Monitor 24 inch", "Electronics", 76.50, 149.99),
    ("P1018", "Monitor 27 inch", "Electronics", 109.00, 199.99),
    ("P1019", "HDMI Cable", "Accessories", 3.10, 8.99),
    ("P1020", "Wireless Charger", "Electronics", 12.70, 27.99),
    ("P1021", "Bluetooth Speaker", "Electronics", 19.90, 44.99),
    ("P1022", "Smart Plug", "Electronics", 8.80, 21.99),
    ("P1023", "Desk Mat", "Accessories", 5.40, 13.99),
    ("P1024", "Storage Box", "Home", 7.10, 16.99),
    ("P1025", "Water Bottle", "Home", 4.30, 11.99),
    ("P1026", "Coffee Mug", "Home", 3.60, 9.49),
    ("P1027", "Laptop Backpack", "Bags", 21.40, 49.99),
    ("P1028", "Travel Adapter", "Accessories", 9.10, 19.99),
    ("P1029", "Ring Light", "Electronics", 15.80, 34.99),
    ("P1030", "Webcam Stand", "Accessories", 5.20, 12.99),
    ("P1031", "Desk Drawer Unit", "Furniture", 32.00, 69.99),
    ("P1032", "Planner Notebook", "Office", 3.80, 8.99),
    ("P1033", "Marker Set", "Office", 2.20, 6.99),
    ("P1034", "Whiteboard", "Office", 12.50, 29.99),
    ("P1035", "Tablet Stand", "Accessories", 8.70, 18.99),
    ("P1036", "Laptop Sleeve", "Bags", 10.90, 24.99),
    ("P1037", "Cable Organizer", "Accessories", 2.90, 7.49),
    ("P1038", "Surge Protector", "Electronics", 7.40, 17.99),
    ("P1039", "Desk Fan", "Home", 9.80, 22.99),
    ("P1040", "Receipt Scanner", "Electronics", 58.00, 99.99),
]


def _build_customer_name(rng: np.random.Generator) -> str:
    return f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"


def _build_email(full_name: str) -> str:
    slug = full_name.lower().replace(" ", ".")
    return f"{slug}@mail.com"


def _sale_date_strings(rng: np.random.Generator, count: int) -> list[str]:
    month_weights = np.array([1.0, 0.9, 1.0, 1.05, 1.05, 1.1, 1.15, 1.15, 1.2, 1.25, 1.35, 1.6, 1.05, 0.95, 1.0, 1.1])
    month_weights = month_weights / month_weights.sum()
    months = rng.choice(np.arange(1, 17), size=count, p=month_weights)

    sale_dates: list[str] = []
    for month_index in months:
        year = 2024 + (month_index - 1) // 12
        month = ((month_index - 1) % 12) + 1
        day = int(rng.integers(1, 28))
        date_value = datetime(year, month, day)
        if rng.random() < 0.7:
            sale_dates.append(date_value.strftime("%Y-%m-%d"))
        else:
            sale_dates.append(date_value.strftime("%m/%d/%Y"))
    return sale_dates


def build_sample_data(seed: int = 42, row_count: int = 900) -> dict[str, pd.DataFrame]:
    rng = np.random.default_rng(seed)

    regions = pd.DataFrame(
        {
            "Region ID": [1, 2, 3, 4],
            "Region Name": ["North", "South", "East", "West"],
            "Country": ["India", "India", "India", "India"],
        }
    )

    customer_rows = []
    for customer_id in range(1, 161):
        full_name = _build_customer_name(rng)
        customer_rows.append(
            {
                "Customer ID": f"C{customer_id:04d}",
                "Customer Name": full_name,
                "Email": _build_email(full_name) if rng.random() > 0.06 else None,
                "Segment": rng.choice(["Consumer", "Corporate", "Home Office"], p=[0.58, 0.24, 0.18]),
                "Region ID": int(rng.choice(regions["Region ID"])),
                "Signup Date": (datetime(2023, 1, 1) + timedelta(days=int(rng.integers(0, 520)))).strftime("%Y-%m-%d"),
            }
        )
    customers = pd.DataFrame(customer_rows)
    customers.loc[rng.choice(customers.index, size=5, replace=False), "Segment"] = None
    customers = pd.concat([customers, customers.sample(4, random_state=seed)], ignore_index=True)

    product_rows = []
    for product_id, product_name, category, unit_cost, unit_price in PRODUCT_CATALOG:
        product_rows.append(
            {
                "Product ID": product_id,
                "Product Name": product_name,
                "Category": category if rng.random() > 0.05 else None,
                "Unit Cost": round(unit_cost * rng.uniform(0.95, 1.05), 2),
                "Unit Price": round(unit_price * rng.uniform(0.95, 1.08), 2),
            }
        )
    products = pd.DataFrame(product_rows)
    products = pd.concat([products, products.sample(3, random_state=seed + 1)], ignore_index=True)

    inventory_rows = []
    for row_index, product in products.drop_duplicates(subset=["Product ID"]).iterrows():
        inventory_rows.append(
            {
                "Inventory ID": f"I{row_index + 1:04d}",
                "Product ID": product["Product ID"],
                "Warehouse Location": rng.choice(["North Hub", "South Hub", "West Hub"], p=[0.38, 0.34, 0.28]),
                "Stock On Hand": int(rng.integers(20, 520)),
                "Reorder Level": int(rng.integers(10, 80)) if rng.random() > 0.03 else None,
                "Last Restock Date": (datetime(2024, 1, 1) + timedelta(days=int(rng.integers(0, 430)))).strftime("%d-%m-%Y"),
            }
        )
    inventory = pd.DataFrame(inventory_rows)

    sale_dates = _sale_date_strings(rng, row_count)
    product_lookup = products.drop_duplicates(subset=["Product ID"]).set_index("Product ID")
    sales_rows = []
    customer_pool = customers["Customer ID"].dropna().tolist()
    for sale_index in range(row_count):
        product_id = str(rng.choice(product_lookup.index))
        product = product_lookup.loc[product_id]
        quantity = int(rng.choice([1, 1, 1, 2, 2, 3, 4, 5, 6, 8], p=[0.18, 0.12, 0.12, 0.15, 0.1, 0.1, 0.09, 0.08, 0.04, 0.02]))
        discount_rate = round(float(rng.uniform(0.0, 0.22)), 2) if rng.random() > 0.04 else None
        sales_rows.append(
            {
                "Sale ID": f"S{sale_index + 1:06d}",
                "Sale Date": sale_dates[sale_index],
                "Customer ID": str(rng.choice(customer_pool)),
                "Product ID": product_id,
                "Region ID": int(rng.choice(regions["Region ID"])),
                "Quantity": quantity,
                "Unit Price": round(float(product["Unit Price"]) * rng.uniform(0.98, 1.02), 2),
                "Unit Cost": round(float(product["Unit Cost"]) * rng.uniform(0.98, 1.02), 2),
                "Discount Rate": discount_rate,
            }
        )

    sales = pd.DataFrame(sales_rows)
    sales = pd.concat([sales, sales.sample(12, random_state=seed + 2)], ignore_index=True)

    return {
        "customers": customers,
        "products": products,
        "sales": sales,
        "inventory": inventory,
        "regions": regions,
    }


def main() -> None:
    settings = load_settings()
    ensure_directory(settings.raw_data_dir)
    generated = build_sample_data()

    for table_name, frame in generated.items():
        write_dataframe(frame, settings.raw_data_dir / f"{table_name}.csv")

    print(f"Generated sample data in {settings.raw_data_dir}")


if __name__ == "__main__":
    main()
