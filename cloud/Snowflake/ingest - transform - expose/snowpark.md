# Snowpark : python, java, scala

Snowpark = set of non-SQL capabilities : python, java, scala

Snowpark functionnalities :
- python UDF, python stored proc
- snowpark dataframes (python, scala, java)
- snowpark ML
- snowpark container service

Notes
- lazy evaluation
- pushdown : code pushed down to snowflake, and executed there
- UDFs inline : Created function can be executed in UDFs

# Snowpark Dataframes

Lib to transform data
- ingestion : data to ODS
- transformation : ODS → DW → DM
- delivery : DM → external

La fonction définie par le handler (main) doit renvoyer soit :
- string
- variant
- Table

Imports :

```python
from snowflake import snowpark
from snowflake.snowpark.functions import col
```

Fonctions :
- `df_table.show()` : print dans l’onglet “py output”
- `return` : string, variant ou Table, affiché dans onglet “output”
- `session.sql(…)` : exécuter une requete SQL
`session.table(name)`  : récupérer une DF, execution lazy

```python
df_table = df_table.filter(
    col("TRUCK_BRAND_NAME") == "Freezing Point"
).select(
    col("MENU_ITEM_NAME"), 
    col("ITEM_CATEGORY")
).save_as_table(
	  "DATABASE.SCHEMA.TABLE_NAME"
)
```

## Vrac

1. DB connectors

```python
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
engine = create_engine(URL(
	account="myorg-myaccount",
	user="username",
	password="pwd",
	database="db_name",
	schema="public",
	warehouse="wh_name",
	role="myrole",
))
connection = engine.connect()
```

- Snowflake native connectors (SaaS, Databases)
    
    ```python
    from snowflake.sqlalchemy import URL
    engine = create_engine(URL(
    		account="", user="", password="",
    		database="", schema="", warehouse="", role=""
    ))
    connection = engine.connect()
    ```
    

- Transformation
    - Snowpark dataframes
    - Dynamic tables with incremental refreshes
    - SQL, Stored proc, UDF, UDTF

1. Snowpark dataframe
    
    ```sql
    f_table = df_table.SELECT(COL("col_name"), COL("COL_2"))
    ```
