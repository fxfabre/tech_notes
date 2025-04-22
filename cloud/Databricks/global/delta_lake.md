# Delta lake
Open source project that enable building a data lakehouse on top of exiting cloud storage

## Description
- Originally developped by Databricks.
- Open source since ~ 2021
- Optimized for cloud object storage, based on parquet files
- Build for efficient metadata handling

## Architecture
- ACID transactions
  - Improve data appending -> efficient concurrent writes
  - Maintain data integrity, prevent inconsistencies due to job failures
  - Support real time operations
  - Efficient historical data versioning


## Liquid clustering : no more partitions
- Faster write, similar reads
- Self tuning : avoid over and under partitions
- Incremental : auto partial clustering of new data
- Skew-resistant : 


