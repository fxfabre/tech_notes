# Share data via Listing

- Available for all snowflake editions
- Share ro access to data, don't copy data -> always up to date
- The client uses his own warehouse to run tasks -> compute paid by consumer
- What is part of the share :
  - Privileges on the object
  - Account identifiers
- No timeout / expiration time

What can be shared :
- Table, external tables, secure view, secure materialized view, secure UDF
- Can't share a basic view
A share is composed of :
- DB, schema, objects, account (that can access), privileges
Best practices :
- Use a secure view instead of sharing a table
Share to a non-Snowflake user :
- Create a reader account
```sql
CREATE MANAGED ACCOUNT reader_account_name
	ADMIN_NAME = login_name,
	ADMIN_PASSWORD = 'pass_123',
	TYPE = READER;
ALTER SHARE my_share ADD ACCOUNT reader_account_name;
```
If on a 'business critical' account, add `SHARE_RESTRICTIONS=false`

Behaviour :
- Data refresh by default every day
- Can't share data with a consumer in a different cloud region / cloud provider
- I can’t share a share (I dont have access for it ?)
- Can share an unlimited number of db inside a share

Create share : as AccountAdmin, or with "CREATE SHARE" privileges
- UI : go to Data product > Provider studio
- SQL : `CREATE SHARE my_share;`

Share objects : Grant privileges + add customer account
- UI :
  - Create listing : name, availability to anyone or to specific consumers
  - Select tables, views … to include
SQL :
```sql
-- Grant privileges on shared object to share
GRANT USAGE ON DATABASE my_db TO SHARE my_share;
GRANT USAGE ON SCHEMA my_db.my_schema TO SHARE my_share;
GRANT SELECT ON TABLE my_db.my_schema.my_table TO SHARE my_share;

-- Add consumer account
ALTER SHARE my_share ADD ACCOUNT account_id;
```
Snowflake will create a new database called SNOWFLAKE$GDS and use it to automate the replication needed.

Access a data share as customer :
- UI :
  - go to data product > private sharing
  - click on “get” on the share you want
- SQL :
  ```sql
  -- IMPORT SHARE, ACCOUNTADMIN role or (IMPORT SHARE + CREATE DB) privileges required
  CREATE DATABASE new_db FROM SHARE my_share;
  ```

## Update a data share :

- go to Data product > Provider studio
- tab “listings”
- “data dictionnary” to add Description on each table
- “Sample SQL queries” to define some sample use case
- Refresh rate : Consumer accounts > update refresh frequency


From SQL :
```sql
USE ROLE ACCOUNTADMIN;
SHOW SHARES;
DESC SHARE account_id.share_name
CREATE DATABASE data_share_db FROM SHARE account_id.share_name;
SELECT * FROM data_share_db;
```

## Database replication
- Replicates a database between accounts (different cloud provider, different regions) within the same organization
- Snowflake standard feature
- Data if effectively copied -> generate transfert costs
- Data and objects syncronized periodically
- Original database is "primary database"
- Copies are "secondary database (replica)" -> always read only
- Must be enable at the account level

Steps :
1. Enable replication for source account with ORGADMIN role.
`SELECT SYSTEM$GLOBAL_ACCOUNT_SET_PARAMETER('<account_identifier>', 'ENABLE_ACCOUNT_DATABASE_REPLICATION', 'true');`
2. Promote a local DB to primary DB with accountadmin role  
`ALTER DATABASE my_db1 ENABLE REPLICATION TO ACCOUNTS my_org.accountXX, my_org.accountYY;`
3. Create replica in consumer account
`CREATE DATABASE my_db AS REPLICA OF myorg.account1.my_db1`
4. Refresh database: `ALTER DATABASE my_db1 REFRESH`. Ownership privileges required
