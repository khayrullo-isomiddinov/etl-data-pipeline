from pathlib import Path
import sqlite3
import subprocess, sys

BASE = Path(__file__).resolve().parents[1]
DB = BASE / "databases" / "db_labels.db"
KUMQUAT_LOADER = BASE / "scripts" / "load_kumquat.py"

def counts():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    (i,) = cur.execute("SELECT COUNT(*) FROM images;").fetchone()
    (l,) = cur.execute("SELECT COUNT(*) FROM labels;").fetchone()
    con.close()
    return i, l

def test_delta_no_growth_on_second_run():
    subprocess.check_call([sys.executable, str(KUMQUAT_LOADER)])
    i1, l1 = counts()

    subprocess.check_call([sys.executable, str(KUMQUAT_LOADER)])
    i2, l2 = counts()

    assert i2 == i1
    assert l2 == l1
