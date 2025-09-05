from pathlib import Path
import sqlite3

BASE = Path(__file__).resolve().parents[1]
DB_PATH = BASE / "databases" / "db_labels.db"

SQL_DEDUP = """
-- Keep only the highest version per (record_file_name, timestamp)
DELETE FROM labels AS l
WHERE EXISTS (
  SELECT 1
  FROM labels AS s
  WHERE s.record_file_name = l.record_file_name
    AND s."timestamp"      = l."timestamp"
    AND COALESCE(s."version", 1) > COALESCE(l."version", 1)
);
"""

def main():
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found at {DB_PATH}. Run scripts/create_db.py first.")

    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")
    cur = con.cursor()

    cur.execute("BEGIN;")
    cur.executescript(SQL_DEDUP)
    con.commit()
    con.close()
    print("Dedup complete: older label versions removed.")
    
if __name__ == "__main__":
    main()
