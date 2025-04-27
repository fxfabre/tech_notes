# Delta lake
Open source project that enable building a data lakehouse on top of exiting cloud storage

## Description
- Originally developped by Databricks.
- Open source since ~ 2021
- Optimized for cloud object storage, based on parquet files
- Build for efficient metadata handling
- Default format in Databricks
  - CREATE TABLE name USING DELTA
  - df.write.format("delta")

## Architecture
- ACID transactions
  - Improve data appending -> efficient concurrent writes
  - Maintain data integrity, prevent inconsistencies due to job failures
  - Support real time operations
  - Efficient historical data versioning
- Allow update & delete
- Data skipping index : use metadata to optimize query

## Liquid clustering : no more partitions
- Faster write, similar reads
- Self tuning : avoid over and under partitions
- Incremental : auto partial clustering of new data
- Skew-resistant : consistent file size
- Flexible : easy to change clustering columns
- Better concurrency
- Best if :
  - Table filtered by high caardinality columns
  - Table with signidicant skew in data distribution
  - Table that grow quickly
  - Table with concurrent write requirements
  - Table with access patterns that change over time
  - Table where a partition key could leave the table with too few / many partitions
- Enable with `CLUSTER BY` :
  - `CREATE TABME name CLUSTER BY (col_1, col_2) AS ...;`
  - `ALTER TABLE name CLUSTER BY (col_name);`
- Trigger liquid clustering : `OPTIMIZE table_name;`
  - To run regularly, up to every 1 or 2 hours if many insert / updates
  - Liquid clustering is incremental : Only cluster new data, since last clustering
  - Automatically run if required by the deletion vector, and `auto: true` is enabled in the "operationParameters"

## Deletion vector
- To avoid full table re-write on update / delete
- Delete, update & merge are written to a deletion vector file.
- ie : the data is still here, but marked as "to be deleted"
- Physical deletion of data happen during an `OPTIMIZE`.
- Photon use deletion vectors for predictive I/O updates, accelerating delete, merge & update operations

## Predective optimization
- Automate Optimize & Vacuum operations
- Uses ML to determine the most efficient access pattern to read data
- Leverage deletion vectors to accelerate updates by reducing the frequency of full file re-write
- Can be enabled at the account level, or on catalog and schemas
- See if enabled : run `DESCRIBE EXTENDED tble_name;`
