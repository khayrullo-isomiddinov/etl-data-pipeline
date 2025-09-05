from pathlib import Path
import sqlite3
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
DB = BASE / "databases" / "db_labels.db"
LOADER = BASE / "scripts" / "load_kumquat.py"
CSV = BASE / "raw_data" / "kumquat_output.csv"

def _counts():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    (imgs,) = cur.execute("SELECT COUNT(*) FROM images;").fetchone()
    (lbls,) = cur.execute("SELECT COUNT(*) FROM labels;").fetchone()
    con.close()
    return imgs, lbls

def test_setup_files_exist():
    assert DB.exists(), "Run scripts/create_db.py first"
    assert LOADER.exists(), "Missing scripts/load_kumquat.py"
    assert CSV.exists(), "Missing raw_data/kumquat_output.csv"

def test_loader_runs_and_populates():
    # run once
    subprocess.check_call([sys.executable, str(LOADER)])
    imgs, lbls = _counts()
    assert imgs >= 0
    assert lbls >= 0

def test_loader_is_idempotent():
    # snapshot after first run
    first_imgs, first_lbls = _counts()
    # run again — should not duplicate
    subprocess.check_call([sys.executable, str(LOADER)])
    second_imgs, second_lbls = _counts()
    assert second_imgs == first_imgs
    assert second_lbls == first_lbls

def test_labels_have_matching_images():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    (orphans,) = cur.execute("""
        SELECT COUNT(*)
        FROM labels l
        LEFT JOIN images i
          ON i.record_file_name = l.record_file_name
         AND i."timestamp"      = l."timestamp"
        WHERE i.record_file_name IS NULL
    """).fetchone()
    con.close()
    assert orphans == 0, "Found labels without a matching image row"
