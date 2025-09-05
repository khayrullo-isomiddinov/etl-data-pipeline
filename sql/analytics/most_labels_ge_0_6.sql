WITH counts AS (
  SELECT
    l.record_file_name,
    l."timestamp",
    COUNT(*) AS cnt_ge_06
  FROM labels AS l
  WHERE l.label_size >= 0.6
  GROUP BY l.record_file_name, l."timestamp"
),
maxcnt AS (
  SELECT MAX(cnt_ge_06) AS mx FROM counts
)
SELECT c.record_file_name,
       c."timestamp",
       c.cnt_ge_06 AS labels_ge_0_6
FROM counts AS c
JOIN maxcnt AS m ON c.cnt_ge_06 = m.mx
ORDER BY c.record_file_name, c."timestamp";
