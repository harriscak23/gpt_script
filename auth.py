from pathlib import Path

from config import SESSION_DIR


def get_session_path(account):
    return Path(SESSION_DIR) / f"{account}.json"