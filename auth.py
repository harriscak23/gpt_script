from pathlib import Path

from config import SESSION_DIR


def get_session_path(account):
    return Path(SESSION_DIR) / f"{account}.json"

def get_accounts():
    return sorted(
        path.stem
        for path in Path(SESSION_DIR).glob("*.json")
)