# Time travel / Fail safe

- Snowflake keeps track of all changes that happens in the last days
- Allow to query data at any time during the retention days
- Have to pay for all data stored
- Applies to database & schemas : used by UNDROP actions

Operations :
- Query deleted or updated data
- Restore dropped tables, schema & databases
- Create clone of table, schema & database from previous state


## Query historic data
As of a timestamp
```sql
SELECT *
FROM db.schema.table_name
AT(TIMESTAMP => '2024-12-03 10:11:12.000'::timestamp);
```

With an offset in seconds
```sql
SELECT *
FROM db.schema.table_name
AT(OFFSET => -3600);
```

Before a (bad) query
```sql
SELECT *
FROM db.schema.table_name
BEFORE(STATEMENT => <query_id>);
```

Tips :
- Use command `ALTER SESSION SET TIMEZONE = 'UTC` to use UTC timestamp
- Find query_id (UUID) in Home > Activity > Query history
- current TS : `SET good_data_timestamp = CURRENT_TIMESTAMP;`
- Last query id : `SET good_data_query_id = LAST_QUERY_ID();`


## Recover objects
On table, schema or complete database
```sql
UNDROP TABLE db.schema.table_name;
UNDROP TABLE db.schema;
UNDROP TABLE db;
```

Limitations :
- UNDROP fails if an object with the same name already exists. Rename new object before
- Ownership privileges are needed for an object to be restored


## Retention period
- Number of days for which this historical data is preserved and Time Travel can be applied
- Max value = 1 day for standard edition, 90 days for enterprise editions

Settings :
- `DATA_RETENTION_TIME_IN_DAYS` : on account, db, schema & table
- `MIN_DATA_RETENTION_TIME_IN_DAYS` : on account only, only applies to permanent tables
- retention time = max(MIN_DATA_RETENTION_TIME, DATA_RETENTION_TIME)
- Default = 1 day, for all accounts
- Set to 0 to disable

|     | min retention | default retention | max retention | fail safe | auto delete |
| --- | --- | --- | --- | --- | --- |
| Permanent Table | 0 | 1 day | 90 days (enterprise) | yes | / |
| Transient Table | 0 | 1 day | 1 day | no | / |
| Temporary Table | 0 | 1 day | 1 day | no | on session close |

Set with table creation :
```sql
CREATE TABLE table_name (
    col_id int,
    col_name varchar
)
DATA_RETENTION_TIME_IN_DAYS = 2;
```

Display, col `retention_time` :
- SHOW TABLES;
- SHOW SCHEMAS;
- SHOW DATABASES;

Update :
- on a db, schema or table : `ALTER TABLE table_name SET DATA_RETENTION_TIME_IN_DAYS=2`
- On account : `ALTER ACCOUNT SET (MIN_)DATA_RETENTION_TIME_IN_DAYS=2`


## Fail safe
- 7 days beyond time travel
- Not enabled on transient tables
- Only a disaster recover, must call snowflake support
- Contributes to storage cost
- Can't be configured
