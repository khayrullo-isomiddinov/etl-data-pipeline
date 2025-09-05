WITH ranked AS (
  SELECT
    l.record_file_name,
    l."timestamp",
    l.label_type,
    l.label_size,
    ROW_NUMBER() OVER (
      PARTITION BY l.record_file_name, l."timestamp"
      ORDER BY l.label_size DESC NULLS LAST
    ) AS rn
  FROM labels AS l
)
SELECT record_file_name,
       "timestamp",
       label_type,
       label_size
FROM ranked
WHERE rn <= 2
ORDER BY record_file_name, "timestamp", rn;
