import sqlite3
from pathlib import Path

DB_PATH = Path("runs.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            runs INTEGER NOT NULL,
            avg_latency_ms REAL,
            p95_latency_ms REAL,
            error_rate REAL NOT NULL,
            availability REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_run(result: dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO runs (
            runs,
            avg_latency_ms,
            p95_latency_ms,
            error_rate,
            availability
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        result["runs"],
        result["avg_latency_ms"],
        result["p95_latency_ms"],
        result["error_rate"],
        result["availability"],
    ))

    conn.commit()
    conn.close()


def list_runs(limit: int = 20):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, created_at, runs, avg_latency_ms, p95_latency_ms, error_rate, availability
        FROM runs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows
