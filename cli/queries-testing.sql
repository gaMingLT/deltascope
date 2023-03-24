

-- New files
-- If path & hash are not in the base image but in the next image
-- SQLite
SELECT *
FROM scn_1_change_files -- Next Image
WHERE name not like '%(deleted%' 
and name NOT IN (SELECT name FROM scn_1_base_files) -- Base Image
AND name like '/etc%'
ORDER BY mtime desc, atime desc

-- Modified Files
-- if path & hash are not in base image
-- if path in base image but hash doesn't macht
SELECT *
FROM scn_1_change_files next
WHERE name not like '%(deleted%'
AND name in (SELECT md5 FROM scn_1_base_files base where base.md5 != next.md5)
AND name like '/etc%'
ORDER BY mtime desc, atime desc

-- AND 'd' = (SELECT substr(mode_as_string, 1, 1) as fileType FROM scn_1_change_files next2 WHERE next2.md5 = next.md5)

-- Moved files
-- if path is different
-- hash is the same
SELECT *
FROM scn_1_change_files next
WHERE name not like '%(deleted%'
AND md5 in (SELECT md5 FROM scn_1_base_files base where base.name != next.name)
AND name like '/etc%'
ORDER BY mtime desc, atime desc


-- Deleted files
-- if path & hash in base image but not in next image
SELECT *
FROM scn_1_base_files base
WHERE name not in (SELECT name FROM scn_1_change_files)
