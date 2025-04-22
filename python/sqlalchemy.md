# Sqlalchemy

## Présentation générale
probleme : "object relational impedance mismatch" a résoudre (TODO : detailler)

SQLAlchemy n'est pas une lib qui masque la structure d'une DB relationnelle, mais un toolkit qui permet de simplifier son utilisation, en étant plus haut niveau.

Core layer : dbapi intégration, génération des requetes SAL, schema management.
ORM layer : object relationnal mapper. Couche d'abstraction , surcouche de la Core layer. Contient les object MetaData, Table, select (qu'est ce que c'est ?) et ResultProxy

Clair découpage ORM / core :
- Permet plus de souplesse, peut utiliser celui que l'on veut.
- Mais pertes de performances : plus d'étapes nécessaires pour faire la même chose. Solution partielle : utiliser l'interpreteur Pypy, permet d'éviter des allers-retours entre python et le C ?

MetaData : pour représenter une collection de Table.
Table = Columns + Constraints
SQLBuilder : génération automatique de la requete SQL, adapté à la base.


## Code python

```python
from sqlalchemy import create_engine
import os

user = os.getenv("DB_USER")
pwd = os.getenv("DB_PASSWORD")
host = os.getenv("DB_SERVER", "localhost")
db = os.getenv("DB_NAME")
port = os.getenv("DB_PORT", 5432)
cx_string = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"

engine = create_engine(cx_string)
engine.connect().execution_options(autocommit=True)
```

### Declarative mapping :
```python
from sqlalchemy import DateTime, Float, Integer, String, Uuid, Boolean
from sqlalchemy import create_engine, Column, UniqueConstraint
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class SqlClassName(Base):
    __tablename__ = "sql_table_name"
    __table_args__ = (
        UniqueConstraint("item_id", "col_2", name="u_item_id_col_2"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, index=True, nullable=False)
    col_2 = Column(String)
    col_3 = Column(Uuid, unique=True)

    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=datetime.utcnow().isoformat(sep=" ", timespec="seconds"),
    )
```

### Create tables from declarative mapping
```python
from sqlalchemy_utils.functions import create_database, database_exists

def init_db():
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url, encoding="utf8")
    Base.metadata.create_all(engine, checkfirst=True)

```


### Reflexion
Construction de l'objet Table à partir de la structure de la base de données.  
Cad : on ne déclare pas la table comme au dessus, on récupère un objet table à partir
de la structure de la table en base

```python
metadata = MetaData()
metadata.reflect(bind=engine)
table = metadata.tables['table_name']
# or
table = Table('table_name', metadata, autoload_with=engine)
```


## Upsert
Creer un insert, avec `on_conflict`

Cas 1 : `item_id` doit avoir `index=True, unique=True`  
- `index_elements` contient des noms de colonnes

```python
from sqlalchemy.dialects.postgresql import Insert
Insert(SqlClassName)
.values(item_id=item_id, col_1="aa", col_2="bb")
.on_conflict_do_update(index_elements=["item_id"], set_={"col": "value"})
```

Cas 2 : Avec une contrainte définie par `UniqueConstraint`  
- Le nom de la contrainte doit être celle définie dans le `UniqueConstraint`

```python
Insert(SqlClassName)
.values(item_id=item_id, col_1="aa", col_2="bb")
.on_conflict_do_update(constraint="u_call_id_content_type", set_={"col": "value"})
```


## Update
```python
Update(SqlClassName)
.where(SqlClassName.item_id == item_id, SqlClassName.id == value)
.values(
    col_xx=3,
    updated_at=datetime.utcnow().isoformat(sep=" ", timespec="seconds"),
)
```


# Alembic

https://alembic.sqlalchemy.org/en/latest/tutorial.html

Lister les templates dispo :
- `alembic list_templates`

Creer une nouvelle migration en utilisant le template par défaut.
Ca créé un nouveau fichier dans alembic/versions qu'il faut compléter
- `alembic revision -m "revision message"`

Creer une nouvelle migration,
Alembic cree le script en faisant la diff entre la structure de la base SQL
et la structure définie dans src/sql_tables
1. Mettre à jour les tables dans src/sql_tables
2. Lancer la commande `alembic revision --autogenerate -m "revision message"`
3. Vérifier le nouveau fichier dans alembic/versions

Executer les migration sur la base SQL :
- `alembic upgrade head`

- Visualisation des requetes SQL exécutées : 
- `alembic upgrade head --sql`

Executer les migrations jusqu'à la révision 68903784305d :
- `alembic upgrade 68903`

Executer 2 migrations :
- `alembic upgrade +2`

Rollback 1 migration :
- `alembic downgrade -1`


### Ré-écrire la connexion string contenue dans le `alembic.ini`
Objectif : ne pas laisser en clair la cx string dans le `alembic.ini`  
Permet de définir la cx string au runtime, en récupérant les secret dans le bon service

```python
from alembic import context

# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code
context.config.set_main_option('sqlalchemy.url', get_cx_string())
```
