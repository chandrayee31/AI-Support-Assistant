# def analyze_with_llm(question: str, logs: dict) -> str:
    
#     if "order" in question.lower():
#         service_logs = logs.get("order-service", [])
#         error_count = len(service_logs)

#         return f"""
# Root Cause Analysis:
# The order service experienced {error_count} timeout-related errors today.

# Primary Cause:
# Payment gateway latency caused repeated request failures.

# Suggested Fix:
# - Scale the payment service
# - Restart the affected Kafka consumer
# - Add timeout retries
# """
    
#     return "No relevant service issues found."
from openai import OpenAI
import os

# Make sure OPENAI_API_KEY is in your environment!
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_with_llm(question: str, logs: dict) -> str:
    """
    This sends the logs + question to OpenAI's model for reasoning.
    """

    # Create a combined prompt with logs + question
    prompt = f"""
You are an SRE assistant. Analyze application logs and answer the user's question.

User Question:
{question}

Logs:
{logs}

Give a concise root-cause analysis and recommendations.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # good, fast, cheap
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error calling LLM: {e}"
