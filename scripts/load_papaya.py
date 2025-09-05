from pathlib import Path
import sqlite3
from csv_utils import read_csv_smart
from delta_utils import fetch_existing_image_keys, fetch_existing_label_keys
from mapping import to_country_code

BASE = Path(__file__).resolve().parents[1]
DB_PATH = BASE / "databases" / "db_labels.db"
PAPAYA_IMAGES = BASE / "raw_data" / "papaya_output_images.csv"
PAPAYA_LABELS = BASE / "raw_data" / "papaya_output_labels.csv"

def to_float(x):
    if x is None or x == "":
        return None
    return float(str(x).replace(",", "."))

def table_exists(con, name):
    (cnt,) = con.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name=?;", (name,)
    ).fetchone()
    return cnt == 1

def main():
    if not DB_PATH.exists():
        raise SystemExit(f"Database not found at {DB_PATH}. Run scripts/create_db.py first.")
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")
    if not (table_exists(con, "images") and table_exists(con, "labels")):
        raise SystemExit("Schema missing (images/labels). Run: python scripts/create_db.py")

    cur = con.cursor()

    existing_img = fetch_existing_image_keys(cur)
    existing_lbl = fetch_existing_label_keys(cur)

    new_imgs, new_lbls = [], []

    # ---- IMAGES ----
    _, img_rows = read_csv_smart(str(PAPAYA_IMAGES))
    for r in img_rows:
        rec = r["record_file_name"]
        ts = int(r["timestamp"])
        fmt = r.get("image_format")
        path = r.get("image_path")
        country = to_country_code(r.get("country"))

        ikey = (rec, ts)
        if ikey not in existing_img:
            new_imgs.append((rec, ts, fmt, path, country))
            existing_img.add(ikey)

    _, lbl_rows = read_csv_smart(str(PAPAYA_LABELS))
    for r in lbl_rows:
        rec = r["record_file_name"]
        ts = int(r["timestamp"])
        ltype = r["label_type"]
        lsize = to_float(r.get("label_size"))
        lcoords = r.get("label_coordinates")
        ver = int(r.get("version", 1))

        lkey = (rec, ts, ltype or "", ver, lcoords or "")
        if lkey not in existing_lbl:
            new_lbls.append((rec, ts, ltype, lsize, lcoords, ver))
            existing_lbl.add(lkey)

    if new_imgs:
        cur.executemany("""
            INSERT INTO images (record_file_name, "timestamp", image_format, image_path, country)
            VALUES (?, ?, ?, ?, ?);
        """, new_imgs)

    if new_lbls:
        cur.executemany("""
            INSERT INTO labels (record_file_name, "timestamp", label_type, label_size, label_coordinates, "version")
            VALUES (?, ?, ?, ?, ?, ?);
        """, new_lbls)

    con.commit()
    con.close()
    print(f"Papaya delta-load complete. +{len(new_imgs)} images, +{len(new_lbls)} labels inserted.")

if __name__ == "__main__":
    main()
