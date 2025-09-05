from pathlib import Path
import sqlite3
import subprocess, sys

BASE = Path(__file__).resolve().parents[1]
DB = BASE / "databases" / "db_labels.db"
DEDUP = BASE / "scripts" / "dedup_labels.py"

def _q(sql, params=()):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    rows = cur.execute(sql, params).fetchall()
    con.close()
    return rows


def test_dedup_keeps_only_highest_version(tmp_path=None):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    
    cur.execute('DELETE FROM labels WHERE record_file_name=? AND "timestamp"=?;', ("demo.jpg", 1111))
    cur.execute('DELETE FROM images WHERE record_file_name=? AND "timestamp"=?;', ("demo.jpg", 1111))

    
    cur.execute("""
        INSERT INTO images (record_file_name, "timestamp", image_format, image_path, country)
        VALUES (?, ?, ?, ?, ?);
    """, ("demo.jpg", 1111, "jpg", "/tmp/demo.jpg", "HU"))
    cur.execute("""INSERT INTO labels VALUES (?, ?, ?, ?, ?, ?);""",
                ("demo.jpg", 1111, "car", 0.5, "10,10,20,20", 1))
    cur.execute("""INSERT INTO labels VALUES (?, ?, ?, ?, ?, ?);""",
                ("demo.jpg", 1111, "person", 0.9, "12,12,22,22", 2))
    cur.execute("""INSERT INTO labels VALUES (?, ?, ?, ?, ?, ?);""",
                ("demo.jpg", 1111, "tree", 0.7, "8,8,18,18", 2))
    con.commit()
    con.close()

    subprocess.check_call([sys.executable, str(DEDUP)])

    rows = _q("""SELECT DISTINCT "version" FROM labels
                 WHERE record_file_name=? AND "timestamp"=? ORDER BY "version";""",
              ("demo.jpg", 1111))
    assert [r[0] for r in rows] == [2]

    rows2 = _q("""SELECT label_type FROM labels
                  WHERE record_file_name=? AND "timestamp"=? AND "version"=2
                  ORDER BY label_type;""",
               ("demo.jpg", 1111))
    assert [r[0] for r in rows2] == ["person", "tree"]



def test_dedup_is_idempotent():
    
    before = _q("SELECT COUNT(*) FROM labels;")[0][0]
    subprocess.check_call([sys.executable, str(DEDUP)])
    after = _q("SELECT COUNT(*) FROM labels;")[0][0]
    assert after == before
