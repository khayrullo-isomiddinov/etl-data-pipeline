import csv, io

def read_csv_smart(path: str):
    
    with open(path, "r", encoding="utf-8") as f:
        first = f.readline()
        if first.startswith("\ufeff"):
            first = first.lstrip("\ufeff")
        delimiter = ";" if ";" in first and "," not in first else ","
        rest = f.read()
        data = first + rest
    rdr = csv.DictReader(io.StringIO(data), delimiter=delimiter)
    rows = [{k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()} for r in rdr]
    return rdr.fieldnames, rows
