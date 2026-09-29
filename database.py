from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("applications.db")

def initialize(db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            location TEXT,
            job_url TEXT,
            notes TEXT
        )
        """)

def add_application(company: str, role: str, status: str, date_applied: str,
                    location: str = "", job_url: str = "", notes: str = "",
                    db_path: Path = DB_PATH) -> None:
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """INSERT INTO applications(company, role, status, date_applied, location, job_url, notes)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (company, role, status, date_applied, location, job_url, notes),
        )

def get_applications(db_path: Path = DB_PATH) -> pd.DataFrame:
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        frame = pd.read_sql_query(
            "SELECT * FROM applications ORDER BY date_applied DESC, id DESC", conn
        )
    if not frame.empty:
        frame["date_applied"] = pd.to_datetime(frame["date_applied"])
    return frame

def update_status(application_id: int, status: str, db_path: Path = DB_PATH) -> None:
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("UPDATE applications SET status=? WHERE id=?", (status, application_id))

def delete_application(application_id: int, db_path: Path = DB_PATH) -> None:
    initialize(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM applications WHERE id=?", (application_id,))
