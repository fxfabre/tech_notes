# Storage containers : DB, Schema, Table, View
6 categories de données : https://docs.snowflake.com/en/sql-reference/intro-summary-data-types

Notes :
- Select peut utiliser pour la col 2 le résultat généré pour la col 1
`select replace(col_x, “”) as col_name_1, replace(col_name_1, “…”) as col_2 …`

## DATABASE (= CATALOG)

- `SHOW DATABASES;`
- `CREATE DATABASE db_name` → Create & set as current DB

## SCHEMA

Default schema :
- INFORMATION_SCHEMA : system data, cannot be drop
Composed of views
- PUBLIC : can be drop

`SHOW SCHEMA IN ACCOUNT` → All schema from all DB

## Table
- Permanent table :
  - Default table type `CREATE TABLE`
  - max retention_time = 90 day
  - Persistance until dropped
- Transient table :
  - `CREATE TRANSIENT TABLE`
  - max retention_time = 1 day
  - Persistance until dropped
  - For large tables that does not need to be protected
- Temporary table : max retention_time = 1 day & auto delete when user session closes.
  - `CREATE TEMPORARY TABLE`
  - max retention_time = 1 day
  - Only visible in current session, can't be shared with so else, auto delete at the end of session
  - All temporary table does not cause conflicts with existing tables. ie : temporary tables can be used to temporary replace a permanent / transient table.

NB :
- Applies to sql objects : permanent, transient & temp database, schema, tables & stages. If database is transient, all included objects are transient
- Not possible to change the type of an object


## External table
Allow to query data stored in an external stage, as if it was a table
- S3 Folder / CSV / blob storage
- PubSub / SNS topic

Properties :
- Read only, can query, join, create (materialized) view on top
- Can be shared, Can't be cloned
- Support all "COPY INTO" formats except XML
- If error reading a file : skip file
- returns file_name, file_row_number, value::variant (row content) for all file types
- File size recommandation : 250-500MB for Parquet files, 16-250MB for others
- Create external table can reference the stage + the integration (to link the pub/sub) -> Can use `auto_refresh = true`
- Force refresh : `ALTER EXTERNAL TABLE <name> REFRESH`

```sql
create or replace external table T_CHERRY_CREEK_TRAIL(
	my_filename varchar(100) as (metadata$filename::varchar(100))
) 
location= @trails_parquet
auto_refresh = true
file_format = (type = parquet);
```

## Hybrid tables
- Pour des requetes transactionnelles (OLTP), pas analytiques
- Optimisation du stockage pour avoir des perf correctes pour du analytique
- Stockage en ligne, gestion clé primaire et FK, gestion index

## View :
- Can’t UNDROP
- Regular views do not cache data

Avantages :
- Clean code : limite les doublons
- Give access to a subset of a table with a view
- Stays up to date automatically
- Can use JOIN

```sql
CREATE VIEW
DROP VIEW
SHOW VIEWS
DESCRIBE VIEW
ALTER VIEW
```

- set `secure` :
`ALTER VIEW intl_db.public.SIMPLE_CURRENCY SET secure;`

## MATERIALIZED View
- Enterprise edition feature
- To handle performance issues on views
- Generate storage costs + serverless costs, as it is updated after changes on base data

To use when :
- query contains few rows compared to base table
- query require significant processing (intensive logic) -> to put over a table with VARIANT types ?
- query is run often
- query on an external table -> slow performances
- Base table does NOT change often

Avantages :
- Stays up to date automatically : auto update if underlying table is updated
- Query results are always up to date, even if the view is not yet updated
- Cache is enabled on materialized view, not on regular view

Inconvénients :
- Must query one single table => can’t use JOIN to create the view
- Can't query a view / materialized view
- Can't use window functions, UDF, HAVING and aggregation function
- Can't enable Search Optimization
- Can't put a materialized view directly on top of staged data. Must set an external table in between

View last refresh :
- `SELECT * FROM TABLE(INFORMATION_SCHEMA.MATERIALIZED_VIEW_REFRESH_HISTORY());`


```sql
CREATE MATERIALIZED VIEW <name> AS SELECT * FROM <table> WHERE col = 'value';
SHOW MATERIALIZED VIEWS;
DROP MATERIALIZED VIEW <name>;
ALTER MATERIALIZED VIEW <name> SUSPEND;
ALTER MATERIALIZED VIEW <name> RESUME;
```

## Dynamic table
kind of materialized view, but more flexible :
- Spec a refresh_rate of 1 min or more
- Can handle more complex transformations
- `TARGET_LAG` to control to pipeline lag
  ie : not only from table B to C, but with multiple tables A > B > C
  
  - `TARGET_LAG = '1 hour'` → refresh every hour
  - `TARGET_LAG = DOWNSTREAM` → refresh when a downstream table need a refresh
  If set on B, C must be a dynamic table. If C is a report, B will never be updated

```sql
CREATE DYNAMIC TABLE costomer_sales_data_histo
LAG='1 MINUTE'
WAREHOUSE='wh_name'
AS SELECT ... FROM ...
```

## metadata
Generer requête creation sql :

```sql
select get_ddl('view', 'DENVER_AREA_TRAILS');
```


## Iceberg Tables

A layer of functionality you can lay on top of parquet files
`DESC EXTERNAL VOLUME iceberg_external_volume;`


## Zero copy cloning
Privileges of the source object will never be cloned. If the source of the clone is a container like a schema or database, all privileges of the child objects will be inherited but not the privileges of the clone itself. If a database is cloned, privileges must be granted on the database but all privileges on the schema and the contained objects will be inherited from the source object.

- database, schema, table, stream, file format, sequence, task
- pipe on external stages
- stage except named internal stages
Cloning a database will clone all contained objects


Process
- Copy is a metadata operation, on the cloud service layer
- Clone takes a snapshot, and reference it
- A table is an aggregation of small blocks. Copy will reference the blocks. If data is updated, the corresponding block is copied, and updated -> increase storage amount
- Can be used to create backup for dev purpuse
- Load history metadata is not copied -> data can be loaded again, and generate duplicates

Privileges needed to clone :
- table : select only
- pipe, stream, task : owner
- others objects : usage


Clone Database
```sql
CREATE OR REPLACE DATABASE db_name_clone
CLONE db_name;
```

Clone Schema
```sql
CREATE OR REPLACE SCHEMA db_name.schema_name_clone
CLONE db_name.schema_name;
```

Clone table
```sql
CREATE table name
CLONE table_source;
```

Clone table from specific point in time :
```sql
CREATE table name
CLONE table_source
BEFORE (TIMESTAMP => '2024-10-01 01:05:08.000'::TIMESTAMP)
```

