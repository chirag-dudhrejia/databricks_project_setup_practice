import uuid
from datetime import datetime, timezone
import time
import random

def make_fetch_id():
    return str(uuid.uuid4())

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def timestamp_for_key():
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

def sleep_backoff(attempt, base=1.0):
    jitter = random.random() * 0.5
    time.sleep(base * (2 ** attempt) + jitter)