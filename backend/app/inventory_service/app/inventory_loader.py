import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../data"))

BEGINNING_FILE = os.path.join(DATA_DIR, "beginning_of_week.xlsx")
SALES_FILE = os.path.join(DATA_DIR, "sales_daily.xlsx")

def load_data():
    if not os.path.exists(BEGINNING_FILE):
        raise FileNotFoundError(f"Missing file: {BEGINNING_FILE}")
    if not os.path.exists(SALES_FILE):
        raise FileNotFoundError(f"Missing file: {SALES_FILE}")

    beginning_df = pd.read_excel(BEGINNING_FILE)
    sales_df = pd.read_excel(SALES_FILE)

    beginning_df["item"] = beginning_df["item"].astype(str).str.strip().str.lower()
    sales_df["item"] = sales_df["item"].astype(str).str.strip().str.lower()

    return beginning_df, sales_df


def get_remaining_inventory(item: str):
    item = item.strip().lower()
    beginning_df, sales_df = load_data()

    ordered = beginning_df.loc[
        beginning_df["item"] == item, "quantity"
    ].sum()

    sold = sales_df.loc[
        sales_df["item"] == item, "quantity"
    ].sum()

    return {
        "item": item,
        "ordered": int(ordered),
        "sold": int(sold),
        "remaining": int(ordered - sold),
    }
def get_inventory_health(threshold: float = 0.3):
    beginning_df, sales_df = load_data()

    summary = []
    for item in beginning_df["item"].unique():
        ordered = beginning_df.loc[beginning_df["item"] == item, "quantity"].sum()
        sold = sales_df.loc[sales_df["item"] == item, "quantity"].sum()
        remaining = ordered - sold

        status = "LOW" if remaining / ordered < threshold else "HEALTHY"

        summary.append({
            "item": item,
            "ordered": int(ordered),
            "sold": int(sold),
            "remaining": int(remaining),
            "status": status
        })

    return summary

def get_inventory_health(threshold: float = 0.3):
    beginning_df, sales_df = load_data()

    health = []
    for item in beginning_df["item"].unique():
        ordered = beginning_df.loc[beginning_df["item"] == item, "quantity"].sum()
        sold = sales_df.loc[sales_df["item"] == item, "quantity"].sum()
        remaining = ordered - sold

        status = "LOW" if remaining / ordered < threshold else "HEALTHY"

        health.append({
            "item": item,
            "ordered": int(ordered),
            "sold": int(sold),
            "remaining": int(remaining),
            "status": status
        })

    return health

