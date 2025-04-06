# SQL instructions

## Hierarchie des objets
- Catalog : `USE CATALOG catalog_name`, `SELECT current_catalog()`
- Schema : `USE SCHEMA schema_name`, `SELECT current_schema()`, `DESCRIBE SCHEMA EXTENDED schema_name`
- Tables : aggrégation / gouvernance sur les données tabulaires. `SHOW TABLES;`
  - Managées ou externes
- Volumes : aggrégation / gouvernance sur les données non tabulaires. `SHOW VOLUMES;`
  - ie : dossier pour contenir données semi / non structurées + gestion access ...
  - identifier : /volumes/catalog_name/schema_name/volume_name
  - `LIST '/Volumes/catalog_name/schema_name/volume_name'`
  - Query : ```SELECT * FROM csv.`/volumes/catalog_name/schema_name/volume_name/file.csv`;```
  - Managées ou externes


## Table versions
- Display versions : `DESCRIBE HISTORY table_name;`
- Query a previous version (version number 2) : 
  - `SELECT * FROM table_name VERSION AS OF 2`
  - `SELECT * FROM table_name@v2` (alternative syntax)
- `RESTORE table_name TO VERSION AS OF 1`
- `RESTORE table_name TO TIMESTAMPS AS OF `
