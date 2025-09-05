from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parents[1] / "databases" / "db_labels.db"

def test_tables_exist():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    tables = {r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table';")}
    assert "images" in tables
    assert "labels" in tables

def test_images_have_data():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    (cnt,) = cur.execute("SELECT COUNT(*) FROM images;").fetchone()
    assert cnt > 0 

def test_labels_have_data():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    (cnt,) = cur.execute("SELECT COUNT(*) FROM labels;").fetchone()
    assert cnt > 0  
