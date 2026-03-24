def analyze_question(question: str) -> dict:
    q = (question or "").lower().strip()

    TOP_SELLING_KEYWORDS = [
        "top selling",
        "top sell",
        "best selling",
        "most sold",
        "highest selling",
    ]

    REVENUE_KEYWORDS = [
        "total revenue",
        "revenue",
        "total sales",
        "sales amount",
    ]

    NO_RESTOCK_KEYWORDS = [
        "not restock",
        "do not restock",
        "should i not restock",
        "what should i not restock",
        "what not to buy",
    ]

    RESTOCK_KEYWORDS = [
        "restock",
        "reorder",
        "what should i buy",
        "what to order",
        "what should i restock",
    ]

    LOW_STOCK_KEYWORDS = [
        "low stock",
        "out of stock",
        "stock low",
        "remaining stock",
    ]

    if not q:
        return {"intent": "empty", "raw_question": question}

    if any(k in q for k in TOP_SELLING_KEYWORDS):
        return {"intent": "top_selling", "raw_question": question}

    if any(k in q for k in REVENUE_KEYWORDS):
        return {"intent": "revenue", "raw_question": question}

    if any(k in q for k in NO_RESTOCK_KEYWORDS):
        return {"intent": "no_restock", "raw_question": question}

    if any(k in q for k in RESTOCK_KEYWORDS):
        return {"intent": "restock", "raw_question": question}

    if any(k in q for k in LOW_STOCK_KEYWORDS):
        return {"intent": "low_stock", "raw_question": question}

    return {"intent": "general", "raw_question": question}