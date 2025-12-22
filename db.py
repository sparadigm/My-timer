import sqlite3, time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "my_timer.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS session(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_ts INTEGER NOT NULL,
            end_ts INTEGER NOT NULL,
            mode TEXT NOT NULL CHECK (mode IN ("work", "break")),
            note TEXT
        )""")
    return conn

#INFO: CREATE TABLE IF NOT EXISTS session
#テーブルがなければ作る、あるなら何もしない
#INFO: AUTOINCREMENT
#自動で割り当てを行う際、これまで使われたidの最大値+1を使用する。過去に使われたidを使用しない
#NOTE: 柔軟性を考え、セッションごとに管理

def insert_session(start_ts, end_ts, mode, note = None):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO session (start_ts, end_ts, mode, note) VALUES (?, ?, ?, ?)",
            (int(start_ts), int(end_ts), mode, note)
        )
# 