# SQL instructions

## Hierarchie des objets
- Catalog : `USE CATALOG catalog_name`, `SELECT current_catalog()`, `DESCRIBE CATALOG name`
- Schema : `USE SCHEMA schema_name`, `SELECT current_schema()`, `DESCRIBE SCHEMA EXTENDED schema_name`
- Tables : aggrégation / gouvernance sur les données tabulaires. `SHOW TABLES;`, `DESCRIBE [EXTENDED] table_name`
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

## Create table
```sql
CREATE TABLE tble_name (
    id STRING,
    operation_ts FLOAT,
    date DATE GENERATED ALWAYS AS (
        cast(cast(operation_ts / 1e6 AS TIMESTAMP) AS DATE)
    ) COMMENT "Generated based on 'operation_ts' column"
);
```

```sql
ALTER TABLE tble_name
ADD CONSTRAINT cstrt_name CHECK ( column_date > '2020-01-01' );
```

## Json
Add schema to json data :
```sql
SELECT schema_of_json('{"key": "value", ...}') as data_with_schema;
```

Create a table from json data :
```sql
CREATE TABLE tble_name AS
SELECT json.* from (
    SELECT from_json(value, schema_of_json('json data ...')) as json
)
```

## Arrays
Convert list of dict to a table structure :
```sql
CREATE TABLE name AS
SELECT *, explode(items) as item
from source;
```
- Array len : `size(array)`
- `flatten`
- `collect_set(col)` -> gen a set : distinct values
