# SQL metadata

| Schema name     | SNOWFLAKE.ACCOUNT_USAGE         | $DB.INFORMATION_SCHEMA              |
|-----------------|---------------------------------|-------------------------------------|
| Description     | Long term historical usage data | Object metadata                     |
| Latency         | 45 min to 3 hours               | No latency                          |
| Retention time  | 365 days                        | 7 days to 6 month, depends on views |
| Dropped objects | Included                        | not included                        |
| User role       |                                 | Results differs depending on role   |


## SQL commands
- `SHOW TABLES like '%abc%'`
- `SHOW GRANTS TO SHARE share_name`
- `SHOW MANAGED ACCOUNTS;`
- `SHOW SHARES` -> données partagées, must be accountadmin


## SNOWFLAKE.ACCOUNT_USAGE
Require AccountAdmin
- `ACCOUNT_USAGE.TABLE_STORAGE_METRICS` : Storage size used for every DB, by type (active, time travel, fail safe)
- `ACCOUNT_USAGE.COLUMNS`: list of columns for each table
- `account_usage.copy_history` : columns file_name, error_count, status, last_load_time
- `account_usage.query_history` : 
- `ACCOUNT_USAGE.STORAGE_USAGE`: used storage, stage & fail safe bytes for every day

## SNOWFLAKE.READER_ACCOUNT_USAGE
Views
- login_history
- query_history
- resource_monitors
- storage_usage
- warehouse_metering_history

## $DATABASE.INFORMATION_SCHEMA
- Automatically created, read only

Available views :
- `INFORMATION_SCHEMA.TABLES` : list of tables
  - Display tables + table type, size, retention_time
  - col `bytes` : actual size + virtual size (if clone)
- `INFORMATION_SCHEMA.TABLE_STORAGE_METRICS`: tables + storage metrics
  - active size (not clone), time travel size, fail-safe size 
  - col `active_bytes` : bytes used on storage. Can be 0 if table is a clone
