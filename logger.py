import json
from datetime import datetime

def log_to_json(event, details, log_file="game_log.json"):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "details": details
    }

    try:
        with open(log_file, "r") as file:
            logs = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)

    with open(log_file, "w") as file:
        json.dump(logs, file, indent=4)
