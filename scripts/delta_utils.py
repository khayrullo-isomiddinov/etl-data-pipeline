from typing import Set, Tuple

def fetch_existing_image_keys(cur) -> Set[Tuple[str, int]]:
    
    rows = cur.execute('SELECT record_file_name, "timestamp" FROM images;').fetchall()
    return {(r[0], int(r[1])) for r in rows}

def fetch_existing_label_keys(cur) -> Set[Tuple[str, int, str, int, str]]:
    rows = cur.execute(
        'SELECT record_file_name, "timestamp", COALESCE(label_type,""), '
        'COALESCE("version",1), COALESCE(label_coordinates,"") FROM labels;'
    ).fetchall()
    return {(r[0], int(r[1]), str(r[2]), int(r[3]), str(r[4])) for r in rows}
