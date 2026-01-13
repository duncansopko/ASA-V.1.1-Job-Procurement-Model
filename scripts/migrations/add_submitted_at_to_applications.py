import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "asa.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Add column if it doesn't exist (SQLite has no IF NOT EXISTS for ADD COLUMN)
    cur.execute("PRAGMA table_info(applications);")
    cols = {row[1] for row in cur.fetchall()}

    if "submitted_at" not in cols:
        cur.execute("ALTER TABLE applications ADD COLUMN submitted_at TEXT;")
        conn.commit()
        print("submitted_at column added to applications.")
    else:
        print("submitted_at column already exists.")

    conn.close()

if __name__ == "__main__":
    main()

