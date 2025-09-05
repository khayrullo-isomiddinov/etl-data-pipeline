from pathlib import Path
import sqlite3
import re

BASE = Path(__file__).resolve().parents[1]
DB_PATH = BASE / "databases" / "db_labels.db"
IMAGES_SQL = BASE / "sql" / "images.sql"
LABELS_SQL = BASE / "sql" / "labels.sql"

def load_sql_sqlite_compat(text: str) -> str:
    return re.sub(r"VARCHAR\s*\(\s*max\s*\)", "TEXT", text, flags=re.IGNORECASE)

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS labels;")
    cur.execute("DROP TABLE IF EXISTS images;")

    images_sql = load_sql_sqlite_compat(IMAGES_SQL.read_text(encoding="utf-8"))
    labels_sql = load_sql_sqlite_compat(LABELS_SQL.read_text(encoding="utf-8"))
    con.executescript(images_sql)
    con.executescript(labels_sql)
    con.commit()
    con.close()
    print(f"Database created with success ==>> {DB_PATH}")

if __name__ == "__main__":
    main()
