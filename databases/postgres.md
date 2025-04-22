## Cas particuliers & erreurs simples
- Postgres est case insensitive  
  `drop table TableName` est interprété comme `drop table tablename` -> Renvoie table "tablename" does not exist  
  Il faut écrire `drop table "TableName"` pour garder la casse


## Start DB
docker run -d \
    --name some-postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v /custom/mount:/var/lib/postgresql/data \
    postgres

psql -h localhost -p 5432 -U postgres $db_name


## Basic commands :
- `\l` - list databases
- `\c` - Connect to database
- `\dn` - List schemas
- `\dt` - List tables inside public schemas
- `\dt schema1`. - List tables inside particular schemas. For eg: 'schema1'.
- `\d+ $table_name` - description d'une table
- `\q` - quit
- `\dx` - List of installed extensions


Afficher les tables d'une base :
- `SELECT tablename FROM pg_tables; : lister les tables d'une base`
- `SELECT * FROM pg_tables WHERE tablename !~ '^pg_' AND tablename !~ '^sql_';`

```
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
```


Display memory used by each table :
```
SELECT *, pg_size_pretty(total_bytes) AS total
    , pg_size_pretty(index_bytes) AS index
    , pg_size_pretty(toast_bytes) AS toast
    , pg_size_pretty(table_bytes) AS table
  FROM (
  SELECT *, total_bytes-index_bytes-coalesce(toast_bytes,0) AS table_bytes FROM (
      SELECT c.oid,nspname AS table_schema, relname AS table_name
              , c.reltuples AS row_estimate
              , pg_total_relation_size(c.oid) AS total_bytes
              , pg_indexes_size(c.oid) AS index_bytes
              , pg_total_relation_size(reltoastrelid) AS toast_bytes
          FROM pg_class c
          LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
          WHERE relkind = 'r'
  ) a
) a
WHERE table_schema != 'pg_catalog' AND table_schema != 'information_schema'
AND row_estimate > 0;
```


## Postgis :
- doc Postgres : https://registry.hub.docker.com/_/postgres/
- doc postgis  : http://postgis.net/docs/postgis_administration.html

- docker run --name postgis -e POSTGRES_PASSWORD=mysecretpassword -d postgis/postgis:13-3.1-alpine
- docker exec -it postgis psql -U postgres

```SQL
CREATE TABLE public.vector ( 
  id serial NOT NULL,
  vctor double precision [4]
 );

INSERT INTO public.vector (vctor) VALUES (ARRAY[2,3,4,1]);
INSERT INTO public.vector (vctor) VALUES (ARRAY[3,4,5,1]);

ALTER SYSTEM SET work_mem = '256MB';
SELECT pg_reload_conf();
SHOW work_mem;
```

### Database fragmentation :
https://www.ktexperts.com/data-fregmentation-in-postgresql/
