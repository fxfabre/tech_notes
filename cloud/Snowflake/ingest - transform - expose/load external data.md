# File format

Specific behaviour :
- PARSE_HEADER : …

Available file formats :
- CSV, JSON, AVRO, ORC, PARQUET, XML

File format options :
- RECORD_DELIMITER : char to split rows

Alter file format :
- `ALTER FILE FORMAT file_format_name SET PROPERTY = VALUE;`
- Can't change the type of file format : each type has its own properties


```sql
create file format file_format_name
    RECORD_DELIMITER = '^'
    type = 'csv';
```

# Stage
- Def : named gateway into a cloud folder where, data files are stored.  
2 ways bridge between datasource and Table : read file or write file  
Composé d’un file format et d’une source (snowflake par défaut)

Location of stage :
- Internal Stages : Managed by Snowflake
- External stage : cloud storage (S3, GCS …)

3 types of stage :
- User stage : can only be used by that user, cannot be altered or dropped  
  Every user has a default stage  
  Identifier to query : `@~`
- Table stage : can only be used with the associated table, cannot be altered or dropped  
  Automatically created when a stage is created  
  Identifier to query : `@%table_name`
- Named stage : can be used by multiple user and associated with multiple tables

Specific behaviour :
- Enabling directory table is required to see the files stored on the stage
- Files on stage are compressed by default with gzip (Property : `AUTO_COMPRESS = TRUE`)
- Files on stage are encrypted by default with 128-bit or 256-bit key

## Create Stage
- Create an Internal Stages :
```sql
CREATE STAGE db.schma.stage_name
    DIRECTORY = ( ENABLE = true ) 
    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' );
```

- Create an external stage : cloud storage (S3, GCS …)
```sql
CREATE OR REPLACE STAGE db.schma.stage_name
    url = 's3://bucket/folder_name/'
    file_format = (FORMAT_NAME=db.schma.ff_name);
```

## Delete Stage files
```SQL
REMOVE @stage_name PATTERN=file_pattern
DROP stage_name -- without @
```

## Stage commands, Query Stage data

- `SHOW STAGES;`
- List stage content :
  - `ls @stage_name`
  - `list @stage_name`
  - `select * from directory(@stage_name);`
- Query file content : `SELECT $1, $2 FROM @stage_name/file_name.csv`

Stages have properties set at creation, or default properties :
- To view props : describe stage : `DESC STAGE @stage_name`
- Can be overwritten in the file format object

Specific behaviour :
- On external stage : can’t run `select *`, must run `select $1, ..., $n`  
But it is working on JSON files

Copy local file to DB
```SQL
PUT file://C:\folder\file_name.csv @stage_name;
PUT file:///tmp/load.csv @stage_name;
```

# In place data sharing across regions
    
```sql
CREATE DATABASE shared_data
FROM SHARE data_shareing_account.data_to_share
```

# COPY INTO
Copy data between DB, internal stage & external stage

Limitations :
- Not possible to copy from internal stage (from | to) external stage ?
- Can't use FLATTEN & aggregations functions (max, sum ...)
- Can't use GROUP BY, WHERE & JOIN

Copy options :
```sql
COPY INTO dataset.schema_name.table_name
FROM @stage_name
    copy_options;
```

copy_options :
- File format :
  - `FILE_FORMAT = (format_name = FF_JSON_LOGS)` for custom file format
  - `FILE_FORMAT = (TYPE = 'CSV')` for default CSV file format
  - `FILE_FORMAT = (TYPE = 'CSV' field_delimiter = ';' skip_header = 1)` for CSV file format
- `ON_ERROR = CONTINUE | SKIP_FILE | SKIP_FILE_xx`.
  - Continue = ignore row
  - SKIP_FILE = SKIP_FILE_1 (default for PIPE) = if 1 error on a row, ignore file
  - SKIP_FILE_xx : skip file if nb errors >= xx
  - SKIP_FILE_10% 
  - ABORT_STATEMENT (default on COPY command) -> cancel all copy
- SIZE_LIMIT = 25000000 : charge tout le fichier tant que le volume total déja chargé n'a pas dépassé
- PURGE = TRUE | FALSE : Remove files from stage after load
- MATCH_BY_COLUMN_NAME : CASE_SENSITIVE | CASE_INSENSITIVE | NONE (default)
- ENFORCE_LENGTH : (opposite of TRUNCATECOLUMNS)
  - TRUE (default) : produces error if string too long for column format
  - FALSE : Truncate value to fit column format
- `FORCE=TRUE` to force re-load data, for files in INFORMATION_SCHEMA.COPY_HISTORY (last 14 days)
- `LOAD_UNCERTAIN_FILES=TRUE` to load files with last_modified_date > 64 days (ignored by default)
- `VALIDATION_MODE = RETURN_n_ROWS | RETURN_ERRORS`
  - RETURN_5_ROWS : return 5 first rows if no error. Else return first error
  - RETURN_ERRORS : return all errors across all files

Where to define FILE FORMAT options :
- In COPY command
- In stage
- In separate file format object

## Copy DB to DB

Specific behaviour :
- Does not re copy files already in DB
ie : can be re-done any-time, does not duplicate data - process IDEMPOTENT

Batch copy from subfolder :
```sql
COPY INTO dataset.schema_name.table_name
FROM ...
```

## Copy stage to DB

Batch copy from subfolder :
```sql
COPY INTO dataset.schema_name.table_name
FROM @dataset.schema.stage_name/raw_pos/menu/;
```

Load specific file :
```sql
COPY INTO dataset.schema_name.table_name
FROM @stage_name
    FILES = ('file_1.csv', 'file_2.csv')
    FILE_FORMAT = 'file_format_name'
```

Load with pattern :
```sql
COPY INTO dataset.schema_name.table_name
FROM @stage_name
    PATTERN = '.*export.csv'
```

## Copy from DB to stage (unloading)
- To internal & external stage, format CSV, TSV, JSON, PARQUET, XML ...

Default :
- File format = CSV
- Header = False
- Split data in many files, by chunks of 16MB
- File prefix = 'data_'

Options :
- SINGLE=TRUE : export in 1 file
- MAX_FILE_SIZE_xxx : split files every xxx octets
- FILE_FORMAT=(TYPE=CSV)
- HEADER=TRUE : include col names

```SQL
COPY INTO @stage_name
FROM dataset.schema_name.table_name
    FILE_FORMAT=(TYPE=CSV)
    HEADER=TRUE
```

Set a file prefix (data_ by default):
```SQL
COPY INTO @stage_name/file_prefix
FROM dataset.schema_name.table_name
```

## Directory table
- To store metadata of a stage
- Must be enabled on stage, at creation or via ALTER STAGE (default : disable)
- Retrieve files URL to access file
- A directory table is not a separate database object, it is more like an implicit object layered on a stage.
- Right after stage creation, no data available. Must refresh stage before
  - Manual refresh : `ALTER STAGE stage_name REFRESH` (warning, no @ needed)
  - List stage content is enough ?
- `SELECT * FROM DIRECTORY(@stage)` -> relative path, size, last modified, md5, scoped url

## Get logs of COPY INTO
`VALIDATE( <table_name>, JOB_ID => '<query_id> | _last')`
- View all encountered errors in a past execution of the COPY INTO command
- IF COPY with `ON_ERROR = ABORT_STATEMENT` : no logs available

