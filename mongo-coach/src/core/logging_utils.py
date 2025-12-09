import datetime as _dt

def log(msg: str) -> None:
    ts = _dt.datetime.utcnow().isoformat()
    print(f"[{ts}] {msg}")
