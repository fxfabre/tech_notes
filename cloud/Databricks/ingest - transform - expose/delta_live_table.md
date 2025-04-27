# Delta live table
Create an ETL, a Streaming pipeline application by defining views depending on other table / views.

## Delta live tables DLT
- Declarative ETL framework : batch + streaming
- Workload specific autoscaling
- Good for :
  - ETL job, batch or streaming
  - With data quality constraints, monitoring, logging
  - Can be added as a single task in a Workflow
- Create in Workflows -> tab delta live tables

```sql
CREATE OR REFRESH MATERIALIZED VIEW v_name AS
    SELECT col_a, SUM(col_b)
    FROM LIVE.tbl_source
    GROUP BY 1
```

## Streams
Create streaming table. Constraints :
- tble_source must be an append only source. No update / delete
- Must not define an aggregate function
- Any append only table can be used as a stream
```sql
CREATE STREAMING TABLE tble_name
       AS SELECT * FROM STREAM(tble_source)
```

## Expectations
- To ensure data quality / correctness
- true / false expressions used to validate each row
- 3 kind of checks
  - Track number of bad records
  - Drop bad records
  - Abort processing

```sql
... CONSTRAINT constraint_name
EXPECT (col_a > '2020-01-01')
ON VIOLATION DROP;
```

```python
@dlt.expect_or_drop("constraint_name", col("col_name") > "2020-01-01")
```

## Pipeline UI
- view data flows between tables
- Discover metadata & quality of each table
- Access to historical updates
- Control operations (top right menu)
- Full refresh all table
  - Access from "start" button dropdown
  - option : pipelines.reset.allowed
- Deep dive into events

## Event log
- Operational statistics
- Provenance : table level lineage
- Data quality
