# Databricks ecosystem for data eng

## Data sources


## Ingestion


## Data processing
- Delta live table (DLT) : declarative ETL framework
- Spark
- Photon

## Data storage
- Delta lake
  - Storage over a cloud : S3, ADLS, GCS
  - Open source protocol for reading and writing files to cloud storage
  - Default format for tables created in Databricks
  - Parquet files + transaction logs with metadata
    - Transaction logs : allow to travel back in time
  - Key features
    - ACID transactions
      - Atomicity : Soit l'instruction est exécutée dans son intégralité, soit elle ne l'est pas du tout
      - Consistency : une corruption ou une erreur dans les données n'a pas de conséquences sur l'intégrité des tables
      - Isolation : les transactions effectuées simultanément ne s'impactent pas les unes les autres
      - Durability : les transactions réussies sont enregistrées, même en cas de défaillance du système
    - Data Manipulation Language (DML) operations
      - Insert, update, delete, merge
    - Time travel
      - Query historical data
      - Snapshot isolation
      - Auditing
    - Schema evolution & enforcement
      - Auto adjust the schema without manual intervention
      - Ensure that all data matches the table's defined schema
    - Unified batch / Streaming
    - Scalable metadata

## Orchestration
Workflows

## Data governance, access and security
Unity catalog

## Usages
- DBSQL : BI
- Mosaic AI : Data science / ML
- Delta sharing : Data sharing

