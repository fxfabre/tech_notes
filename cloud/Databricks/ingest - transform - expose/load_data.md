# Load data

## Read files or folder
- text : ```SELECT * FROM text.`/volumes/catalog_name/schema_name/volume_name/file.csv`;```
- csv : ```SELECT * FROM csv.`/volumes/catalog_name/schema_name/volume_name/file.csv`;```
- folder : ```SELECT * FROM parquet.`dataset/folder/raw`;```
- customizable :
```sql
SELECT *
FROM read_files(
     '/volumes/catalog_name/schema_name/volume_name/file.csv',
     format => 'CSV',  -- or "csv"
     sep => "|",
     header => true,
     inferSchema => true,
     mode => "FAILFAST"
);
```

A `rescued data` column is added with all rows with an error (does not match data format)


## Create Delta table (default)
```sql
DROP TABLE IF EXISTS table_name;

CREATE TABLE table_name USING DELTA
AS
SELECT id, name FROM table
```

```sql
CREATE OR REPLACE TABLE table_name
USING csv
OPTIONS (
    path '/Volumes/catalog_name/schema_name/folder/',
    header = 'true',
    delimiter = ','
)
LOCATION "s3://...";
```


## Upload UI
- Can upload CSV, JSON, Avro, Parquet, text files
- To create a Table, or into a Unity Catalog Volume


## Copy / clone / overwrite / merge
Copy Into :
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
FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true')
COPY_OPTIONS ('mergeSchema' = 'true');
```

Deep clone will copy the data + metadata :
```sql
CREATE TABLE tble_name
DEEP CLONE tble_source;
```

Shallow clone will only copy the metadata -> only a ref to the table version :
```sql
CREATE TABLE tble_name
SHALLOW CLONE tble_source;
```

Insert overwrite to replace table, but keep history :
```sql
INSERT OVERWRITE tble_name
SELECT * FROM source;
```

Merge, can do insert, update or delete, add custom logic :
```sql
MERGE INTO tble_name a
USING table_source b
    ON a.user_id = b.user_id
WHEN MATCHED AND b.email IS NOT NULL
    UPDATE SET email = b.email, updated_at = b.updated_at
WHEN NOT MATCHED THEN
    INSERT (user_id, email, updated_at)
    VALUES (b.user_id, b.email, b.updated_at)
```




## Auto loader
- Load incrementally new data files as they arrive in a cloud storage
- Automatically infers schemas and accommodates schema changes
- Includes a rescue data column for data that does not match to the schema















