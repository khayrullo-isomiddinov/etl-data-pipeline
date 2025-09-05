from pathlib import Path
import sqlite3, csv, sys

BASE = Path(__file__).resolve().parents[1]
DB_PATH = BASE / "databases" / "db_labels.db"
SQL_DIR = BASE / "sql" / "analytics"
OUT_DIR = BASE / "reports"

def run_sql(con: sqlite3.Connection, sql_text: str):
    cur = con.cursor()
    cur.execute(sql_text)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description] if cur.description else []
    return cols, rows

def write_csv(path: Path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if cols: w.writerow(cols)
        w.writerows(rows)

def main(db_path: Path = DB_PATH):
    if not db_path.exists():
        raise SystemExit(f"DB not found: {db_path}. Run scripts/create_db.py and loaders first.")
    if not SQL_DIR.exists():
        raise SystemExit(f"SQL dir not found: {SQL_DIR}")
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA foreign_keys = ON;")

    sql_files = sorted(SQL_DIR.glob("*.sql"))
    if not sql_files:
        print(f"No .sql files in {SQL_DIR}")
        return

    for sql_file in sql_files:
        sql_text = sql_file.read_text(encoding="utf-8").strip().rstrip(";")
        cols, rows = run_sql(con, sql_text)
        out = OUT_DIR / (sql_file.stem + ".csv")
        write_csv(out, cols, rows)
        print(f"✓ {sql_file.name}: {len(rows)} row(s) -> {out}")

    con.close()

if __name__ == "__main__":
    
    db_arg = Path(sys.argv[1]) if len(sys.argv) > 1 else DB_PATH
    main(db_arg)
