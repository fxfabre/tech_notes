# Data sampling
Query a subset of the table -> useful for dev
Available methods :
- row (= bernoulli) -> to use on smaller tables
- system (= block) -> apply on blocks, for larger tables

Use method ROW, take 10% of the table, set seed to reproduce
```sql
SELECT * FROM table
SAMPLE ROW(10) SEED(15)
```

## Create table
```sql
CREATE OR REPLACE TABLE $DATABASE.$SCHEMA.table_name
    CLONE tasty_bytes.raw_pos.truck;

CREATE TABLE <table_name> (ID, maker) AS 
    SELECT TRUCK_ID, MAKE FROM tasty_bytes.raw_pos.truck;
```


## INSERT INTO

Insert all columns :
```sql
INSERT INTO table_name
VALUES
    (value1, value2, value3, ...),
    (value4, value5, value6, ...),
```

Insert specific columns :
```sql
INSERT INTO table_name (column1, column2, column3, ...)
VALUES
    (value1, value2, value3, ...),
    (value4, value5, value6, ...),
```

Truncate table before inserting data:
```sql
INSERT OVERWRITE INTO table_name (column1, column2, column3, ...)
VALUES
    (value1, value2, value3, ...),
    (value4, value5, value6, ...),
```

Insert JSON
```sql
INSERT INTO table_name
SELECT parse_json('{"key1": "value1", "key2": "value2"}')
```

## Lateral flatten
```python
{
		menu_id: 12,
		item_category: 'Dessert',
		menu_item_health_metrics_obj: {
				"menu_item_health_metrics": [
				{
						"ingredients": ["Lemons", "Sugar", "Water"],
						"is_dairy_free_flag": "Y",
						"is_gluten_free_flag": "Y",
				}
	  ]
}
```

Requete :
```sql
SELECT
    m.menu_id,
    m.item_category,
    det.index,
    ing.index,
    ing.value
FROM menu m,
    LATERAL flatten(input => m.menu_item_health_metrics_obj['menu_item_health_metrics']) det,
    LATERAL flatten(input => det.value['ingredients']) ing;
```
