# General
- `DESC FUNCTION func_name(TYPE)` (same for PROCEDURE)
  - Display inner information : signature, return type, language and function body
  - We can also access inner information using the optimizer 
- Use `SECURE FUNCTION` to hide function body
  - Does not optimize query -> reduced query performance


- `SHOW VARIABLES;` to display vars across all database
- `show functions;`  to display all functions in current database
- `SHOW PROCEDURES;`  display stored proc inside current DB


# Variables

```sql
SET good_data_query_id = LAST_QUERY_ID();
SELECT $good_data_query_id;    -- Attention au $
```

# UDF
- Defined inside a database.schema -> can grant access
- Possible to overload functions (different signature)
- Supported languages : SQL, python, Java, JS, scala
- Executed with creator's rights
- Must return a value

## SQL UDF
```sql
CREATE FUNCTION max_menu_price_converted(price_coef NUMBER)
  RETURNS NUMBER(5, 2)
  AS $$
    SELECT price_coef * MAX(SALE_PRICE_USD) FROM TASTY_BYTES.RAW_POS.MENU
  $$;
```

## python UDF
```sql
CREATE FUNCTION winsorize (val NUMERIC, up_bound NUMERIC, low_bound NUMERIC)
returns NUMERIC
language python
runtime_version = '3.11'
handler = 'winsorize_func'
AS $$
def winsorize_func(val, up_bound, low_bound):
    if val > up_bound:
        return up_bound
    elif val < low_bound:
        return low_bound
    else:
        return val
$$;
```

## User Defined Table Functions
- Supported languages : SQL, python, Java, JS - but `NOT scala`

```sql
CREATE FUNCTION menu_prices_above(price_floor NUMBER)
  RETURNS TABLE (item VARCHAR, price NUMBER)
  AS $$
    SELECT MENU_ITEM_NAME, SALE_PRICE_USD 
    FROM TASTY_BYTES.RAW_POS.MENU
    WHERE SALE_PRICE_USD > price_floor
    ORDER BY 2 DESC
  $$;
```

```sql
SELECT * FROM TABLE(menu_prices_above(15));
```

# Stored proc
- Defined inside a database.schema -> can grant access
- Can use DML (update / alter table …)
- Supported languages : SQL, python, Java, JS, scala
- Have to be called as independant statement : `CALL stored_proc();`
- Doesn't need to return a value
- Can run with caller's or owner's rights, with owner rights by default

```sql
CREATE OR REPLACE PROCEDURE delete_old(max_ts TIMESTAMP)
execute as caller
RETURNS BOOLEAN
LANGUAGE SQL
AS
$$
DECLARE
  cutoff_ts TIMESTAMP;
BEGIN
  cutoff_ts := (SELECT DATEADD('DAY', -180, :max_ts));
  DELETE FROM <table_name> WHERE ORDER_TS < :cutoff_ts;
END;
$$
;
```


# External functions
- code stored & executed outside of Snowflake
- Used to use third-party libs, services, data & call API
- `api_integration` used to store credentials
- Schema level object -> can grant access

Limitations
- Must be scalar function (can't call with a table)
- Slower performance
- Not sharable
- Can't be included in a shared object (view)
- Maximum response size 10MB

```SQL
CREATE EXTERNAL FUNCTION my_az_function(param VARCHAR)
RETURNS VARIANT
api_integration = azure_external_api_integration
as 'https://my-api-management-svc.azure-api.net/my-api-url/my_http_function'
```

# Sequences
- Genereate a sequence of numbers
- Can have some gaps. ie : not sure to have all numbers
- Create : `CREATE SEQUENCE db.schema.my_seq START = 1 INCREMENT = 1`
- Use in select : `SELECT my_seq.nextval;`
- Use in table : `CREATE TABLE table_name (id int DEFAULT my_seq.nextval, ...)`

