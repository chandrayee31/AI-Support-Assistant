from app.llm_client import ask_llm
from app.sales_analyzer import (
    get_total_revenue,
    get_top_selling_products,
    get_low_stock_items,
    recommend_restock,
    recommend_no_restock,
)
from app.question_analyzer import analyze_question


def process_question(question: str) -> str:
    analysis = analyze_question(question)
    intent = analysis["intent"]

    if intent == "empty":
        return "Please enter a question."

    if intent == "top_selling":
        return get_top_selling_products()

    if intent == "revenue":
        return get_total_revenue()

    if intent == "no_restock":
        return recommend_no_restock()

    if intent == "restock":
        return recommend_restock()

    if intent == "low_stock":
        return get_low_stock_items()

    return ask_llm(question)    # git test
