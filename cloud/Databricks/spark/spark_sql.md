# SQL samples
References :
- Gestion des NULL : https://spark.apache.org/docs/latest/sql-ref-null-semantics.html

Main differences with generic SQL :
- Spark does not support update & delete statements. Must Truncate / Drop table


## Create table
We must define the internal storage format used.
```sql
CREATE TABLE database.table_name (
    col_id integer, col_name string
) using parquet
```

Create from dataframe view :
```sql
INSERT INTO database.table_name
SELECT * FROM global_temp.dataframe_view_name
```


## Window functions
```sql
SELECT a, b,
    dense_rank(b) OVER (PARTITION BY a ORDER BY b),
    row_number() OVER (PARTITION BY a ORDER BY b)
FROM VALUES ('A1', 2), ('A1', 1), ('A2', 3), ('A1', 1) tab(a, b);
```


## Converion functions
- Dates :
  - datetime patterns : https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html
  - date_add(dt, days), date_diff(dt1, dt2), date_sub(dt, days), add_month(dt, months)
  - day(dt), month(dt), year(dt)
  - current_date(), current_timestamp(), unix_timestamp/micro()
  - make_date(yy, mm, dd), make_timestamp(yy, ...), make_interval(yy, ...)
  - parse : to_date(str, format), to_timestamp(str, format)
- String
  - to_char(), to_number(), to_varchar()
- Conditions
  - if(cond, then, else), ifnull, nanvl
  - case when..then when..then else end 
- CSV
  - from_csv, to_csv 
- Generate table
  - explode()
