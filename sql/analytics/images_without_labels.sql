SELECT i.record_file_name,
       i."timestamp",
       i.image_path,
       i.country
FROM images AS i
LEFT JOIN labels AS l
  ON l.record_file_name = i.record_file_name
 AND l."timestamp"      = i."timestamp"
WHERE l.record_file_name IS NULL
ORDER BY i.record_file_name, i."timestamp";
