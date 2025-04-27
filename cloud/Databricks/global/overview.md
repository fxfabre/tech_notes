# Databricks fundamentals

## Infrastructure : 2 internal layers
- Extarnal layer : web users and API
- **Control plane**
  - Unity catalog
  - Web apps
  - Mosaic AI
  - Workflows
  - Git folders
  - Notebooks
  - DB SQL
- **Serverless Data Plane** (optional)
  - Elastic compute : Cluster / SQL Warehouse
  - Unallocated pool
- **Data plane**
  - Data stays on the cloud provider storage
  - Elastic compute :
    - Cluster
    - SQL Warehouse
  - Storage (Delta lake)
    - S3, ADLS, GCS

## Object hierarchy
- Metastore : default location for data, managed by Databricks
  - Created by Dbx admin
  - A workspace have only 1 metastore
- Catalog : a group of schemas
- Schema (or Database)
- Data objects
  - Table : Collection of structured (tabular) data
    - Managed table : data stored inside the metastore
    - External table : need storage credential, data in external storage
  - View
    - Temporary view
    - Global temporary view
    - Standard view
  - Function
    - UDF : Return a scalar value
    - UDTF : return rows

## Unity catalog
- provides the following functionalities across Databricks workspaces.
  - Metastore
  - access control, auditing, lineage and data discovery
- One security & governance model for structured / unstructured data + AI
- Allow to connect with
  - Cloud storage : Azure data lake storage, S3, GCS
  - Catalog federation : Hive, AWS glue
  - External compute platforms : Amazon Athena, Presto, Amazon EMR, trino, spark
  - Data federation : redshift, snowflake, BigQuery, SQL DB

## Metastore
- top-level container for metadata
- It registers metadata about data and AI assets and the permissions that govern access to them
- You should have one metastore for each region in which you have workspaces
- Hierarchy
  - Level one
    - Catalogs : used to mirror organizational units or software scopes
    - Non data securable objects : credentials, external locations
  - Level two : schemas (or databases)
  - Level 3
    - Volumes : unstructured, non-tabular data, managed or not
    - Tables, Views, UDF, Models

## Databricks compute
Runtimes : Enhanced with databricks Photon
- **Standard**
  - Spark + others
- Machine learning
- Specialized compute
  - SQL Warehouses : SQL BI workloads

## Serverless
- Higher user productivity
  - User query start instantly, no waiting for cluster start-up
  - Add more concurrent user with instant cluster scaling
- Zero management
  - No config / performance tunning / capacity management
  - Auto upgrade / patching
- Lower cost
  - Pay as you go : no idle cluster time / no over provisioning
  - Idle capacity removed 10 min after last query

## Data intelligence platform
- Build on the lakehouse paradigm
- Layers :
  - Usage : workflows, Delta live tables, SQL, AI/BI dashboards and genie, Mosaic AI
  - Unity catalog : unified governance layer
  - Storage : Delta lake
- Data science, ML & gen AI supported by Mosaic AI
  - ML flow, Auto ML, feature store, model serving, vector search, agent framework, training

## Storage & governance
- Works with any cloud : AWS, Azure, GCP
- Use & support open source projects : Delta lake + Unity catalog
- Delta sharing : consume & share data products
  - Databricks marketplace
  - Databricks clean rooms
- Partner connect
  - Many connectors with 450+ partners : Salesforce, SAP, Fivetrans ...

## Databricks IQ
- Natural language Interfaces
- Intellignet Search & discovery
- AI powered Governance
- Simplified administration & maintenance

## Orchestration & ETL
- Databricks workflow : orchestrates pipelines, including DLT pipelines
- Delta live tables : Automated pipelines for Delta lake

## Unity catalog
- Centralize user access, metastore & access controls.
  ie : can be shared between workspaces ?
- Compute resources stays in each workspace
- Components :
  - Metastore : top level logical container
    - External storage access : Contain the ACL (access control list)
    - Catalog(s) : Contain the metadata on objects
      - Each catalog contain schemas
      - Each schemas contains table, views, volumes, functions, models
      - `SELECT * FROM catalog.schema.table_name`
    - Query federation
    - Delta sharing

## Workspace
- Catalog : view data objects : table, UDF ...
- Workspace : Create git repo, notebooks ...


