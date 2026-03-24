def format_bullet_response(title: str, items: list[str]) -> str:
    if not items:
        return f"{title}\n- No data available."

    result = f"{title}\n"
    for item in items:
        result += f"- {item}\n"
    return result


def format_key_value_response(title: str, data: dict) -> str:
    if not data:
        return f"{title}\n- No data available."

    result = f"{title}\n"
    for key, value in data.items():
        result += f"- {key}: {value}\n"
    return result


def format_plain_response(title: str, message: str) -> str:
    return f"{title}\n- {message}"