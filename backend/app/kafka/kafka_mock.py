def get_kafka_lag(topic_name: str):
    mock_lag = {
        "order-events": 42,
        "payment-events": 8,
        "inventory-events": 0
    }
    return mock_lag.get(topic_name, "unknown topic")
