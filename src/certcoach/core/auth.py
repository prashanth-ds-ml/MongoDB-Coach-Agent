import json
import os
from datetime import datetime, timezone

from certcoach.core import database


SESSION_FILE = os.path.join(database.GLOBAL_CONFIG_DIR, "session.json")


def normalize_email(email: str) -> str:
    return email.strip().lower()


def load_session() -> dict | None:
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("user_id"):
            return data
    except Exception:
        return None
    return None


def save_session(user: dict) -> None:
    os.makedirs(database.GLOBAL_CONFIG_DIR, exist_ok=True)
    data = {
        "user_id": user["_id"],
        "email": user.get("email", ""),
        "display_name": user.get("display_name", ""),
        "saved_at": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
    }
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def clear_session() -> None:
    try:
        os.remove(SESSION_FILE)
    except FileNotFoundError:
        pass


def get_session_user_id(default_user_id: str = "local_user_1") -> str:
    session = load_session()
    if session and session.get("user_id"):
        return session["user_id"]
    return default_user_id


def create_account(email: str, password: str, display_name: str = "") -> tuple[bool, str, dict | None]:
    email = normalize_email(email)
    if not email or "@" not in email:
        return False, "Enter a valid email address.", None
    if len(password) < 8:
        return False, "Password must be at least 8 characters.", None

    ok, result = database.create_user(email, password, display_name or email.split("@")[0])
    if not ok:
        return False, result, None
    save_session(result)
    database.get_user_profile(result["_id"])
    return True, "Account created and signed in.", result


def login(email: str, password: str) -> tuple[bool, str, dict | None]:
    ok, result = database.authenticate_user(normalize_email(email), password)
    if not ok:
        return False, result, None
    save_session(result)
    database.get_user_profile(result["_id"])
    return True, "Signed in.", result
