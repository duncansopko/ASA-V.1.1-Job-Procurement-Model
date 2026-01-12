import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "asa.db"

def run():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS application_customization (
            application_id INTEGER PRIMARY KEY,
            resume_customized INTEGER NOT NULL DEFAULT 0,
            cover_letter_customized INTEGER NOT NULL DEFAULT 0,
            timestamp TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (application_id) REFERENCES applications(application_id)
        );
    """)

    conn.commit()
    conn.close()
    print("application_customization table ready.")

if __name__ == "__main__":
    run()

