# Automate processings

Warning points
- All dependent task must be in same schema
- Previous task must be suspended to link a new one
- Task must be resumed after each create or replace Task
- Task must be resumed in their reverse run order - last task to resume first

Streamlit in Snowflake (SiS)
- Warehouse runs for a mini of 15 min by default
- WH does not stop while the web page stay opened

## Init config
Enable serverless compute :
- To avoid having to pay for time wharehouse spin up and wait for timeout to stop
- Must be enabled
    ```sql
    use role accountadmin;
    grant EXECUTE MANAGED TASK on account to SYSADMIN;
    ```
- Must allow use role :
    ```sql
    use role accountadmin;
    grant execute task on account to role SYSADMIN;
    ```

## Tasks
- can run something : stored proc, SQL queries, …
- On a particular schedule : regularly or when another task complete
- Can use a task to listen for a stream, and update a table on certains conditions
- Setup initial server size in task
- Start : `ALTER TASK task_name RESUME`
- Run task once : `execute task task_name`
- Limits in DAG : 100 child task, 1000 tasks in total

Create task with this config instead of warehouse name
```sql
CREATE OR REPLACE TASK task_name
    USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE = 'XSMALL'
    after previous_task_name
AS ...
```
```sql
CREATE TASK task_name
    WAREHOUSE = server_name
    SCHEDULE = '1 minute'
    AS INSERT INTO table_name (
        SELECT KEY, data_id, amount
        FROM stream_name
        WHERE metadata$action = 'INSERT'
    );
```

## Pipe
Snowpipe :
- real time data ingestion from files / queue
- Use a COPY INTO statement
- Use serverless feature

Trigger ingestion :
- Cloud messaging : Streaming ingest (kafka) use event notifications, only external stages, low latency
- REST API : using API endpoints, internal & external stages
- PIPE doesn’t ingest files already in S3 at creation by default. Only ingest new files created after pipe creation

Properties : 
- Cost : per second, per CPU core
- File size : ideally 100 - 250 MB to optimize costs
- Load history : 14 days
- Can't use `PURGE` option in the COPY INTO. Must setup a dedicated remove task to delete file

View history :
- ACCOUNT_USAGE.PIPE_USAGE_HISTORY
- ACCOUNT_USAGE.COPY_HISTORY

Create :
```sql
CREATE PIPE s3_db.public.s3_pipe
    AUTO_INGEST=TRUE
    INTEGRATION = 'queue to trigger integration'
AS COPY INTO db.schema.S3_table FROM @S3_db.puclic.S3_stage;
```

Update :
- `ALTER PIPE SET PIPE_EXECUTION_PAUSED = True`


## Streams
- Used to record DML (insert, update, delete) changes made to a table and publish changes on the stream
- Schema level object, copied if dataset copied
- Changes recorded in the stream, with some metadata added :
  - metadata$action : insert | delete | ?
  - metadata$isupdate : TRUE | FALSE
  - metadata$row_id : hash
- Query : `SELECT * FROM stream_name`
- Consume stream : When run `INSERT INTO ... FROM stream`

Types of stream :
- Standard : insert, update, delete
- Append only : insert only, for standard tables, directory tables & views
- insert only : insert only, for external tables

Stale state :
- It becomes stale when offset is outside the data retention period of source table
  - Setting `DATA_RETENTION_TIME_IN_DAYS` on a table
  - Unconsumed changes records won't be accessible anymore
- Check column `STALE_AFTER` via `DESC STREAM` or `SHOW STREAMS`
- Stream extends retention to 14 days (default) for all Snowflake edition
- Max retention period is 90 days (enterprise edition), to view with `MAX_DATA_EXTENTION_TIME_IN_DAYS`

```sql
CREATE STREAM sales_stream
ON TABLE sales;
```

```sql
CREATE TASK my_task
warehouse = 'my_wh'
schedule = '15 minute'
WHEN SYSTEM$STREAM_HAS_DATA('stream_name')
AS INSERT INTO my_table(data) values ...
```
