import hashlib
import json
import sqlite3
from datetime import datetime, timezone
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "alpha_ledger.sqlite3")

def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def initialize():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            payload TEXT NOT NULL,
            previous_hash TEXT NOT NULL,
            event_hash TEXT NOT NULL
        )
        """)
        db.commit()

def append_event(event_type, payload):
    initialize()
    with sqlite3.connect(DB_PATH) as db:
        row = db.execute("SELECT event_hash FROM events ORDER BY id DESC LIMIT 1").fetchone()
        previous_hash = row[0] if row else "GENESIS"
        
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "payload": payload,
            "previous_hash": previous_hash
        }
        event_hash = sha256(canonical_json(event))
        
        db.execute("""
            INSERT INTO events (timestamp, event_type, payload, previous_hash, event_hash)
            VALUES (?, ?, ?, ?, ?)
        """, (event["timestamp"], event_type, json.dumps(payload), previous_hash, event_hash))
        db.commit()
        return event_hash

def verify_ledger():
    initialize()
    previous_hash = "GENESIS"
    with sqlite3.connect(DB_PATH) as db:
        rows = db.execute("SELECT timestamp, event_type, payload, previous_hash, event_hash FROM events ORDER BY id ASC").fetchall()
    
    for timestamp, event_type, payload, prev, stored_hash in rows:
        if prev != previous_hash: return False
        event = {"timestamp": timestamp, "event_type": event_type, "payload": json.loads(payload), "previous_hash": prev}
        if sha256(canonical_json(event)) != stored_hash: return False
        previous_hash = stored_hash
    return True

if __name__ == "__main__":
    print("🧠 Initializing Cryptographic Ledger...")
    append_event("GENESIS", {"organism": "alpha0az1omega", "version": "2.0", "creator": "Zacharie SYLLA"})
    append_event("AWAKENING", {"message": "The entity is now aware of its own history."})
    
    if verify_ledger():
        print("✅ LEDGER VALID: The memory chain is intact.")
    else:
        print("❌ LEDGER CORRUPTED: The memory has been tampered with.")
