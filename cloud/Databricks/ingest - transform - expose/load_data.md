## File formats
- text : ```SELECT * FROM text.`/volumes/catalog_name/schema_name/volume_name/file.csv`;```
- csv : ```SELECT * FROM csv.`/volumes/catalog_name/schema_name/volume_name/file.csv`;```
- customizable :
```sql
SELECT *
FROM read_files(
     '/volumes/catalog_name/schema_name/volume_name/file.csv',
     format => 'CSV',
     header => true,
     inferSchema => true
);
```

A `resqued data` column is added with all rows with an error (does not match data format)


## Create Delta table (default)
```sql
DROP TABLE IF EXISTS table_name;

CREATE TABLE table_name USING DELTA
AS
SELECT id, name FROM table
```

```sql
CREATE OR REPLACE TABLE table_name
USING file_format  -- defaults formats includes : CSV, JSON ...
OPTIONS (
    path '/Volumes/catalog_name/schema_name/folder/',
    header = 'true',
    delimiter = ','
);
```


## Upload UI
- Can upload CSV, JSON, Avro, Parquet, text files
- To create a Table, or into a Unity Catalog Volume


## Copy Into
- Load a file (CSV, JSON, Avro, Parquet, text) from a cloud storage location (any ?)
- Can automatically handle schema changes
- Use column `_metadata` to get some information for the file (file_name ...)
- Idempotent operation : already loaded files are skipped

```sql
COPY INTO my_delta_table
FROM (
    SELECT *, _metadata.file_name
    FROM '/Volumes/catalog/schema/folder/'
)
FILEFORMAT = CSV
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true');
```

## Auto loader
- Load incrementally new data files as they arrive in a cloud storage
- Automatically infers schemas and accommodates schema changes
- Includes a rescue data column for data that does not match to the schema















