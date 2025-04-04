# SQL native types & functions

## Native types
- Object : unordered set of name / value pair (= dict) `col_name['key']` or `col_name:"key"`
- Array : 0 or more pieces of data
- Variant : can store values of any other data type, including ARRAY & OBJECT

## Variant : Semi structured data
- no fixed schema, nested structure
- supported formats : JSON, XML, Parquet, ORC, Avro
- store NULL as string 'null'
- store non native strings (eg dates) as string
- Maximum length is 16MB uncompressed per row
- Query : `SELECT col_name:key.subkey[n]::VARCHAR` or `SELECT $1:key`

Implicit lateral flatten
```sql
SELECT
    table_name.column,
    value:string as flatten_value
FROM db.schema.table_name,
    TABLE(
        FLATTEN(input => col_name:key) alias
    )
```

Explicit lateral flatten
```sql
SELECT
    table_name.column,
    value:string as flatten_value
FROM db.schema.table_name,
    LATERAL FLATTEN(input => col_name:key) alias
```

## Unstructured data support
- Data that does not fit into pre-defined model
  - audio / video files, documents
- Access files throug URL
- Share file access URLs

3 types of URL available 
- scoped url : encoded snowflake URL with temporary access to a file.
  - Expires when the cache expires, currently after 24h
  - Generate with `BUILD_SCOPED_FILE_URL(@stage, 'relative_file_path.png')`
- File url : permanent access, does not expire
  - Generate with `BUILD_STAGE_FILE_URL(@stage, 'path.png')`
- Pre-signed url : HTTPS with token url to access file via web browser
  - No need to authenticate into Snowflake
  - Expiration time is configurable (in seconds). Default 3600
  - If use AWS IAM role, max = 3600, else : max = 604800 (7 days)
  - Generate with `GET_PRESIGNED_URL(@stage, 'path.png', expiration_time_secs)`


## Scalar functions
- Cast to VARIANT : `SELECT col_name::VARIANT FROM table_name`
- Cast to timestamp : `SELECT '2024-04-04 21:34:31.833 -0700'::TIMESTAMP_LTZ`
- current_timestamp() -> Local time zone, time zone included
- `IDENTIFIER(<object_name>)` -> get table object in a dynamic stored proc


### Estimating functions
- Number of distinct values : `HLL()` (alias of `APPROX_COUNT_DISTINCT()`)
- Frequent values : `APPROX_TOP_K()`
- Percentile values : `APPROX_PERCENTILE()`
- Similarity of 2 or more sets : `MINHASH` + `APPROXIMATE_SIMILARITY()`
  ```SQL
  SELECT APPROXIMATE_SIMILARITY(mh) FROM(
    SELECT MINHASH(100, *) AS mh FROM table1
    UNION ALL
    SELECT MINHASH(100, *) AS mh FROM table2
  )
  ```


## Aggregate functions
- MIN, MAX


## Table functions
- `SELECT * FROM TABLE(VALIDATE(<table_name>, JOB_ID => '_last')`


## SYSTEM functions
- `TYPEOF()` or `SYSTEM$TYPEOF('abc')` -> varchar(3)
- SYSTEM$CANCEL_ALL_QUERIES
- SHOW TABLES LIKE '%_customer_%';
- SHOW SCHEMAS;
- SHOW DATABASES;
- SHOW PARAMETERS
- LAST_QUERY_ID(-2) -> returns the second most recently-executed query
- SYSTEM$IS_LISTING_PURCHASED : control access to data in a share and allow specific data only to paying customers


