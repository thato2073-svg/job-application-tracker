from __future__ import annotations
import sqlite3
from pathlib import Path

DB_PATH = Path("applications.db")

def connect(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize(db_path=DB_PATH):
    with connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            location TEXT DEFAULT '',
            job_url TEXT DEFAULT '',
            notes TEXT DEFAULT ''
        )""")

def add_application(company, role, status, date_applied, location="", job_url="", notes="", db_path=DB_PATH):
    initialize(db_path)
    with connect(db_path) as conn:
        conn.execute("""INSERT INTO applications(company,role,status,date_applied,location,job_url,notes)
                        VALUES(?,?,?,?,?,?,?)""",
                     (company, role, status, date_applied, location, job_url, notes))

def get_applications(search="", status="", db_path=DB_PATH):
    initialize(db_path)
    query = "SELECT * FROM applications WHERE 1=1"
    params = []
    if search:
        query += " AND (LOWER(company) LIKE ? OR LOWER(role) LIKE ?)"
        term = f"%{search.lower()}%"
        params += [term, term]
    if status:
        query += " AND status=?"
        params.append(status)
    query += " ORDER BY date_applied DESC, id DESC"
    with connect(db_path) as conn:
        return conn.execute(query, params).fetchall()

def get_application(application_id, db_path=DB_PATH):
    initialize(db_path)
    with connect(db_path) as conn:
        return conn.execute("SELECT * FROM applications WHERE id=?", (application_id,)).fetchone()

def update_application(application_id, company, role, status, date_applied, location="", job_url="", notes="", db_path=DB_PATH):
    with connect(db_path) as conn:
        conn.execute("""UPDATE applications SET company=?,role=?,status=?,date_applied=?,
                        location=?,job_url=?,notes=? WHERE id=?""",
                     (company, role, status, date_applied, location, job_url, notes, application_id))

def delete_application(application_id, db_path=DB_PATH):
    with connect(db_path) as conn:
        conn.execute("DELETE FROM applications WHERE id=?", (application_id,))

def stats(db_path=DB_PATH):
    initialize(db_path)
    with connect(db_path) as conn:
        total = conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
        interviews = conn.execute("SELECT COUNT(*) FROM applications WHERE status='Interview'").fetchone()[0]
        offers = conn.execute("SELECT COUNT(*) FROM applications WHERE status='Offer'").fetchone()[0]
        responses = conn.execute("SELECT COUNT(*) FROM applications WHERE status IN ('Interview','Offer','Rejected')").fetchone()[0]
    return {"total": total, "interviews": interviews, "offers": offers,
            "response_rate": (responses / total * 100) if total else 0}
