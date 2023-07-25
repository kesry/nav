import os
import logging

confirm = os.getenv("CONFIRM")
if confirm is None:
    confirm = "kesry"

host = os.getenv("HOST")
if host is None:
    host = "0.0.0.0"

level = os.getenv("LOG_LEVEL")
if level is None:
    level = logging.ERROR
elif level.strip().lower() == "debug":
    level = logging.DEBUG
elif level.strip().lower() == "info":
    level = logging.INFO
elif level.strip().lower() == "warn":
    level = logging.WARNING
elif level.strip().lower() == "error":
    level = logging.ERROR
elif level.strip().lower() == "critical":
    level = logging.CRITICAL

print(level)

config = {
    "db": {
        "sqlite3": {
            "path": os.path.join(os.getcwd(), "db/nav.db"),
            "poolsize": 5
        }
    },
    "server": {
        "port": "8080",
        "host": host,
        "log": {
            "path": os.path.join(os.getcwd(), "logs/nav.log"),
            "level": level
            # "level": logging.DEBUG
            # "level": logging.INFO
            # "level": logging.WARNING
            # "level": logging.ERROR
            # "level": logging.CRITICAL
        }
    },
    "confirm": confirm
}

