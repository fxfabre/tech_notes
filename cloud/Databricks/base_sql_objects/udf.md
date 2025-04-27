# User defined (table) functions
- Optimized for SQL UDF, not as efficient in python
- To create, need `USE CATALOG`, `USE SCHEMA` and `CREATE FUNCTION` on the schema.
- To use, need `USE CATALOG`, `USE SCHEMA` and `EXECUTE` on the function

```sql
CREATE FUNCTION fct_name(item_name STRING, price INT) RETURNS STRING
    RETURN concat(item_name, " is no sale for $", round(price * 0.8, 0))
```

View details + function body :
```sql
DESCRIBE FUNCTION EXTENDED function_name
```