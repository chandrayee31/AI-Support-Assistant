import json
from pathlib import Path

def load_fake_logs():
    log_file = Path(__file__).parent.parent.parent / "connectors" / "mock_logs" / "fake_logs.json"
    
    with open(log_file, "r") as f:
        logs = json.load(f)

    return logs
