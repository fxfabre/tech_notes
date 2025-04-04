# Performance concepts

Find query history :
- In UI : Activity -> Query history
- `SELECT * FROM table(information_schema.query_history())`
- `SELECT * FROM snowflake.account_usage.query_history`


## Query profile
- Performance & behavior of a query, identify perf bottlenecks

Content :
- Operator tree : graph representation of building blocs (Nodes)
- Nodes : 
  - operator type : filter, table scan, ...
  - percentage of total time
  - Between nodes : nb of records processed
  - Query result reuse : not from virtual warehouse cache, but from cloud service layer
- Right side infos :
  - Profile overview
  - Statistics :
    - bytes spilled to local storage = not enough memory on warehouse, use local storage (swap)
    - If not enough memory on local storage, can use remote storage : write to an external bucket


## Caching : Improve query performance
- Result cache : in cloud service layer
  - Exactly same result, if table data & micro-partitions has not changed
  - If query doesn't include UDF or external functions
  - Require sufficient privileges
  - Cache data available for 24h after last usage, purged anyway after 31 days
  - Enabled by default, can be disable with `USE_CACHED_RESULT` parameter
- Metadata cache : in cloud service layer
  - Statistics & metadata about objects
  - Properties for query optimization & processing : range of values in micro partition
  - Count rows, count distinct values, min/max
  - Does not need warehouse
  - Describe + system defined functions
  - Virtual private edition : dedicated metadata store
- Virtual Warehouse cache (Data cache)
  - local cache data of the query, on warehouse local disc
  - Cannot be shared with another warehouse
  - Purged if warehouse is suspended or resized
  - Size depends on warehouse size
- Remote disk

Disable cache
- For a given user : `ALTER USER <user_name> SET USE_CACHED_RESULT = false`;
- For current session : `ALTER SESSION SET USE_CACHED_RESULT = false;`
- For current account : `ALTER ACCOUNT SET USE_CACHED_RESULT = false;`


## Micro partitions
- Data in Tables stored in micro-partitions, in external cloud provider
- Data is compressed automatically
- Allow granular partition prunning -> read only required partitions for the query
- Micro partitions props :
  - Immutable
  - New data = new micro partitions, following insert order
  - 1 micro-partition contain 50 - 500 MB of uncompressed data
  - Data stored in columnar format
- Some metadata stored in each micro partition :
  - Range of values (for most important columns ?)
  - Nb of distinct values
  - And some additional props to optimize queries
- Metadata on table :
  - Number of micro partitions
  - Clustering depth = Average depth = how many partition share the same value for a specific column. Should be 1 if well partitioned
  - Nb of overlapping micro partitions = nb of partition with a depth > 1

## Clustering keys
- To apply on large tables, on columns used for where / join operations
- Require enough distinct values to be effective
- Too many distinct values (high cardinality) generate an expensive re-clustering (keep a date instead of a timestamp)
- Clustering improve data distribution -> Optimize partition pruning
- Improve scan efficiency + better column compression
- A `constant partition` = perfect partition, depth = 1, overlap = 0
- Best practice is to cluster first on low cardinality column, then high cardinality cols
- Recommended maximum number of columns per clustering key : 3 or 4
- `CREATE TABLE <name> CLUSTER BY (col1)`
- `ALTER TABLE <name> CLUSTER BY (col1, date(col2));`
- `ALTER TABLE <name> DROP CLUSTER KEY`

Example :
- a table with 3 micro partitions for col id: range(1, 4), range(3, 7), range(6, 9)
- Clustering depth = 2. On average, we can find each value in 2 partitions
- Overlapping partitions = 3. All partitions share at least one value with another partition

Reclustering, consolidation
- Imply additional costs : clustering not for all tables
- Does not happen right after the definition of the clustering key, but on a periodic schedule
- Done automatically : "automatic reclustering"
- Serverless feature, does not need a warehouse
- Create new partition, copy data and mark old partition as 'deleted'
- Old partitions still require storage (costs) for time travel

System functions
SYSTEM$CLUSTERING_INFORMATION
- Get clustering infos on a table :
- Display nb cluster, average overlap, depth ...
- Can display notes to help improving clustering
- `SYSTEM$CLUSTERING_INFORMATION('<table_name>')` : for current clusters
- `SYSTEM$CLUSTERING_INFORMATION('<table_name>', '(col1, col3)')` : if cluster on (col1, col3)
SYSTEM$CLUSTERING_DEPTH
- Get clustering depth
- `SYSTEM$CLUSTERING_DEPTH(<table_name>)` : On average, on all columns
- `SYSTEM$CLUSTERING_DEPTH(<table_name>, '(col)')` : on that column(s)

## Search optimization
- Enterprise edition
- Can improve performance of certain types of lookup & analytical queries
- Best for :
  - Selective point look-up query -> return very few rows
  - For "equality predicate", or "IN predicate" : `WHERE col IN (1, 2)`
  - For substring and regex search : LIKE, ILIKE or regex on VARIANT column
  - For selective geospatial function : with GEOGRAPHY values
- Serverless feature + Additional storage needed -> costs
- Require OWNERSHIP or "ADD SEARCH OPTIMIZATION" privileges on schema
- `ALTER TABLE <table_name> ADD SEARCH OPTIMIZATION`
- `ALTER TABLE <table_name> ADD SEARCH OPTIMIZATION ON EQUALITY(*)` -> all columns, for equality test
- `ALTER TABLE <table_name> ADD SEARCH OPTIMIZATION ON GEO(col_name)` -> GEOGRAPHY values on 'col_name'
- The search optimization service create & maintain a data structure `Search Access Path` to keep track of which values can be found in which partition




