import pandas as pd
from app.sales_data_loader import load_sales_data, normalize_column_names
from app.prompt_generator import format_bullet_response, format_plain_response
from app.prompt_generator import format_bullet_response, format_plain_response

def load_clean_data(filename=None):
    """
    Load and normalize sales data.
    If filename is provided, load that specific uploaded file.
    """
    df, error = load_sales_data(filename)

    if error:
        return None, error

    df = normalize_column_names(df)
    return df, None

# -------------------------------------------------
# 1️⃣ TOTAL REVENUE
# -------------------------------------------------
def get_total_revenue():
    df, error = load_clean_data()
    if error:
        return format_plain_response("Total Revenue", error)

    if "sales" in df.columns:
        total = df["sales"].sum()
        return format_plain_response("Total Revenue", str(round(total, 2)))

    if "revenue" in df.columns:
        total = df["revenue"].sum()
        return format_plain_response("Total Revenue", str(round(total, 2)))

    return format_plain_response("Total Revenue", "No revenue column found.")


# -------------------------------------------------
# 2️⃣ TOP SELLING PRODUCTS
# -------------------------------------------------
def get_top_selling_products(limit=5):
    df, error = load_clean_data()
    if error:
        return format_plain_response("Top Selling Products", error)

    product_col = None
    for col in ["product_name", "sub_category", "product", "item"]:
        if col in df.columns:
            product_col = col
            break

    if not product_col:
        return format_plain_response("Top Selling Products", "No product column found.")

    sales_col = None
    for col in ["units_sold", "quantity", "sales"]:
        if col in df.columns:
            sales_col = col
            break

    if not sales_col:
        return format_plain_response("Top Selling Products", "No sales/quantity column found.")

    grouped = (
        df.groupby(product_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )

    items = [
        f"{i}. {product} — {int(value)} units"
        for i, (product, value) in enumerate(grouped.items(), 1)
    ]

    return format_bullet_response("Top Selling Products", items)


# -------------------------------------------------
# 3️⃣ LOW STOCK / SLOW ITEMS
# -------------------------------------------------
def get_low_stock_items(threshold=10):
    df, error = load_clean_data()
    if error:
        return format_plain_response("Low Stock Items", error)

    stock_col = None
    for col in ["stock_left", "inventory", "remaining"]:
        if col in df.columns:
            stock_col = col
            break

    product_col = None
    for col in ["product_name", "sub_category", "product", "item"]:
        if col in df.columns:
            product_col = col
            break

    date_col = None
    for col in ["date", "order_date"]:
        if col in df.columns:
            date_col = col
            break

    if not stock_col or not product_col:
        return format_plain_response("Low Stock Items", "Required columns not found for stock analysis.")

    latest_df = df.copy()

    if date_col and date_col in latest_df.columns:
        latest_df[date_col] = pd.to_datetime(latest_df[date_col], errors="coerce")
        latest_df = latest_df.sort_values(date_col).groupby(product_col, as_index=False).tail(1)
    else:
        latest_df = latest_df.groupby(product_col, as_index=False).tail(1)

    low_stock = latest_df[latest_df[stock_col] <= threshold]

    if low_stock.empty:
        return format_plain_response("Low Stock Items", "No low stock items.")

    items = [
        f"{row[product_col]} ({int(row[stock_col])} left)"
        for _, row in low_stock.iterrows()
    ]

    return format_bullet_response("Low Stock Items", items)

def recommend_restock(days=1):
    """
    Recommend items to restock based on:
    - recent sales trend (last few days)
    - current stock
    """
    df, error = load_clean_data()
    if error:
        return format_plain_response("Restock Recommendations", error)

    product_col = None
    for col in ["product_name", "product", "item"]:
        if col in df.columns:
            product_col = col
            break

    date_col = None
    for col in ["date", "order_date"]:
        if col in df.columns:
            date_col = col
            break

    sales_col = None
    for col in ["units_sold", "quantity", "sales"]:
        if col in df.columns:
            sales_col = col
            break

    stock_col = None
    for col in ["stock_left", "inventory", "remaining"]:
        if col in df.columns:
            stock_col = col
            break

    if not all([product_col, date_col, sales_col, stock_col]):
        return format_plain_response(
            "Restock Recommendations",
            "Required columns missing for restock prediction."
        )

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    recent_df = df.sort_values(date_col).groupby(product_col).tail(3)

    items = []

    for product in recent_df[product_col].unique():
        product_data = recent_df[recent_df[product_col] == product]

        avg_daily_sales = product_data[sales_col].mean()
        current_stock = product_data.iloc[-1][stock_col]
        expected_need = avg_daily_sales * days

        if current_stock < expected_need:
            reorder_qty = int(expected_need - current_stock + 5)
            items.append(f"{product}: restock ~{reorder_qty} units")

    if not items:
        return format_plain_response("Restock Recommendations", "Stock levels look sufficient.")

    return format_bullet_response("Restock Recommendations", items)


def recommend_no_restock(days=1):
    """
    Recommend items that do NOT need restocking based on:
    - recent sales trend (last few days)
    - current stock
    """
    df, error = load_clean_data()
    if error:
        return format_plain_response("Do Not Restock Tomorrow", error)

    product_col = None
    for col in ["product_name", "product", "item"]:
        if col in df.columns:
            product_col = col
            break

    date_col = None
    for col in ["date", "order_date"]:
        if col in df.columns:
            date_col = col
            break

    sales_col = None
    for col in ["units_sold", "quantity", "sales"]:
        if col in df.columns:
            sales_col = col
            break

    stock_col = None
    for col in ["stock_left", "inventory", "remaining"]:
        if col in df.columns:
            stock_col = col
            break

    if not all([product_col, date_col, sales_col, stock_col]):
        return format_plain_response(
            "Do Not Restock Tomorrow",
            "Required columns missing for no-restock prediction."
        )

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    recent_df = df.sort_values(date_col).groupby(product_col).tail(3)

    items = []

    for product in recent_df[product_col].unique():
        product_data = recent_df[recent_df[product_col] == product]

        avg_daily_sales = product_data[sales_col].mean()
        current_stock = product_data.iloc[-1][stock_col]
        expected_need = avg_daily_sales * days

        if current_stock >= expected_need:
            items.append(
                f"{product}: current stock ({int(current_stock)}) is enough for expected demand (~{int(round(expected_need))})"
            )

    if not items:
        return format_plain_response(
            "Do Not Restock Tomorrow",
            "All items may need restocking soon."
        )

    return format_bullet_response("Do Not Restock Tomorrow", items)