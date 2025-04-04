Standard edition

Enterprise edition
- Search optim, row/col security, materialized view, re-keying (365), Multi cluster Warehouse


Caching : USE_CACHED_RESULT
- Warehouse : reset on resize, suspend.
- Metadata : count, range of values, min/max
- Cloud layer : no UDF, external func, 24h, purged 31 days.
Search optimization : need a "search access path", "ALTER ... ADD SEARCH OPTIMIZATION"
Scripting stored proc : if/else, loops, cursors, resultset. Use objects outside block

Tables : permanent, transient, temporary
External table : wrap external stage, can share, cant clone, no XML file, on error skip file, 
Materialized view : cache enabled, no (join, window func, udf, aggregation, search optim). info_schema.materialized_view_refresh_history
Dynamic table : refresh rate, no limit on join & operations
Clone : except pipe on internal stage, named internal stage. dont keep load history

Time travel : AT(timestamp), AT(offset), BEFORE(statement). Require ownership to undrop
External function : call lambda / API / pubsub. dont share, dont use in shared view, max response 10MB

Alert : need warehouse + schedule, run insert into
Drivers : go, O/JDBC, .net, node.js, go, PHP
Connectors : python, kafka, Spark

ResourceMonitor : AccountAdmin. only 1 account monitor
MFA : SnowSQL, SnowSite, ODBC, JDBC, python connector
MFA token caching : ODBC, JDBC, python connector
SSO : saml2.0, service + IdP, Okta, AD FS. SCIM 2.0
TLS 1.2 in transit : web, snowSQL, O/JDBC, python

Col level security : "Create masking policy", external tokenization
Row : create row access policy
Encryption at rest : AES 256, 30 days key rotation
re-keying (enterprise edition) every year

Warehouse auto_suspend = seconds
Task : run on a schedule, when stream has data. USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE
Pipe : ingestion from file / queue, kafka, COPY INTO, only new files after pipe creation. Cant purge, history 14 days (pipe_usage_history / copy_history)
Stream : record (insert, update, delete) to a table : (action, isupdate, row_id)
Streams : standard (ins, update, del), insert only (insert, external table), append only (insert, other tables / view)

File formats : csv, json, orc, parquet, avro, xml
user stage : single user, to multiple tables
Table stage : single table, multiple users, no privilege, cant alter / drop, REMOVE @stage_name PATTERN=file_pattern

COPY INTO : cant use flatten, aggregation (max, sum), groupby, where, join.
Default = abort_statement, LOAD_UNCERTAIN_FILES > 64 days, 
Directory table : ALTER STAGE stage_name REFRESH

Share = privileges on object + accounts, as accountadmin
Share to non snowflake user : "Create managed account"
DB replication : between accounts, standard edition. must def primary DB


Types d’abonnement + included features
- Hors abonnement :
  - You don’t need a Snowflake edition to browse the Snowflake marketplace listings
- Standard edition
  - automatic data encrypt, time travel 1 day, 7 days fail safe beyond time travel (need to ask Snowflake)
  - MFA, object level access control,
  - dynamic / external / hybrid tables, iceberg
- Enterprise edition
  - multi cluster warehouse, time travel 90 days, periodic re-keying
  - row/column level security (row access policy, masking policies)
  - data quality / metrics functions
  - materialized view, query acceleration, search optimization
  - Feature store (ML)
- Business critical edition for sensitive data : more security
  - customer key (tri secret secure), data specific regulation, DB failback
- Virtual private Snwoflake
  - dedicated servers, off cloud, isolated from all others SF accounts


