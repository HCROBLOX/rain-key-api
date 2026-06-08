from fastapi import FastAPI
import sqlite3

app = FastAPI()

# Kết nối database
db = sqlite3.connect("keys.db", check_same_thread=False)

db.execute("""
CREATE TABLE IF NOT EXISTS keys (
    key TEXT PRIMARY KEY,
    used INTEGER DEFAULT 0
)
""")

db.commit()

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Rain Key API"
    }

@app.get("/check/{key}")
def check_key(key: str):

    cur = db.cursor()

    cur.execute(
        "SELECT used FROM keys WHERE key=?",
        (key,)
    )

    row = cur.fetchone()

    if row is None:
        return {
            "valid": False,
            "message": "Key không tồn tại"
        }

    if row[0] == 1:
        return {
            "valid": False,
            "message": "Key đã dùng"
        }

    cur.execute(
        "UPDATE keys SET used=1 WHERE key=?",
        (key,)
    )

    db.commit()

    return {
        "valid": True,
        "reward": 100
    }

@app.get("/add/{key}")
def add_key(key: str):

    try:
        db.execute(
            "INSERT INTO keys(key) VALUES(?)",
            (key,)
        )
        db.commit()

        return {
            "success": True,
            "key": key
        }

    except:
        return {
            "success": False,
            "message": "Key đã tồn tại"
  }
