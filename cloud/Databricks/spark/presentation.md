# Hadoop, Spark

- Hadoop = platforme de traitement des données distribuées qui offre 3 fonctionnalités principales :
  - Yarn = ressources manager ou "Hadoop cluster OS"  
    Share resources (CPU, RAM, ...) to the apps. 3 main components :
    - RM : resources manager : control the master node
    - NM : node manager : control the worker nodes
    - AM : application master : inside a NM, on the worker.  
      Multiple AM can run on one worker (NM)
  - HDFS : Hadoop distributed FS. Distributed storage on Hadoop cluster. 2 main components
    - NN : Name node : Control the master node, how to distribute data on the workers.
      Keep metadata of all blocs : file (name, size) + block (id, sequence, location)
    - DN : Data node : control the worker node, save partitions (blocs of 128 Mo) of original data
  - Map / Reduce : 2 components
    - Programming model : a method to resolve the problems : Split work into map tasks & reduce tasks.
      Launch a Map job or a Reduce job on the workers as needed
    - MapReduce framework : Set of API & services that allow you to apply the programming model.
      Obsolete, and not used anymore

- Composants supplémentaires :
  - Pig
  - Hive : relational database. Create DB, tables, views & translate SQL to map/reduce jobs.
    Permettait de traduire SQL + distribuer les calculs sur les serveurs, mais pas efficace.
    Obsolete, remplacé par Spark SQL
  - Hbase
  - Spark : abstraction level over map/reduce
  - Oozie

Evolution de MapReduce
- Initié en 2004 par google pour résoudre BigData problem : variety, volume, velocity
- Développé en open source par Apache
- Très vite devenu trop complexe, trop difficile d'écrire des jobs MapReduce.
  Les services cloud sont devenus moins cher / plus efficaces
- Création de Spark pour remplacer Hadoop (pas que MapReduce)

Spark :
- remplace Hadoop, en reprenant certains composants
- 10 ~ 100x faster than MapReduce
- Easier to use :
  - Spark SQL
  - High performance SQL engine
  - Composable Function API : easier to use than M/R
- Language support : Java, scala, python, R
- Storage : HDFS or cloud storage
- Resource management : Yarn, Mesos, Kubernetes
- Run in 2 setups :
  - With Hadoop : Data lake
  - Without Hadoop : Lakehouse

Spark components
- Lower level components, used by Spark but not included inside spark :
  - Distributed storage : HDFS, S3, GCS, Azure datalake storage, Cassandra FS, (No)SQL
  - Cluster manager : yarn, kubernetes or Mesos to manage compute hardware
- Spark engine : Spark core. Distributed computing engine over the cluster manager.
  Link Spark with lower level components, Based on RDD
- Spark libs :
  - Spark SQL, dataframes
  - Streaming
  - MLlib
  - GraphX : graph computation
- Programming languages : Scala, java, python, R. 

DataBricks
- Provide an optimized Spark (x5 faster) on AWS, GCP or Azure
- Easy way to config, launch clusters
- Easy administration, delta lake integration, ML Flow ...

Storage :
- Database tables
  - Layer 1. Physical storage layer, on hard disk. Format CSV, JSON, Parquet, Avro ...
  - Layer 2. Compute (logical) layer, visible across application.  
    Map physical partitions from data storage to a worker
  - Layer 3. Metadata store, persistent : table schema, require predefined table schema
  - Query data using SQL only. Does not support API
- DataFrame 
  - Layer 1. Physical storage
  - Layer 2. Compute (logical) layer. In memory storage, visible to the current application only
  - Layer 3. Metadata Catalog, available during runtime only : DF Schema, schema-on-read
  - Query data using APIs, does not support SQL
- Table object & DataFrames are convertible objects, read one, save it into the other


Spark API :
- High level APIs (Spark SQL, Dataframe API, Dataset API) call Catalyst optimizer.
  It determines how it should be executed, and produce the execution plan.
  Then call RDD API (raw API, not to be used directly) to run.
  Prefer using Spark SQL when possible
- RDD : Resilient distributed dataset
  - records of JVM native objects. No row/col structure, nor schema
  - Broken into partitions -> Distributed collection
  - Fault tolerant : can handle a crash of a runner to re-run processing
  - Save data + transformations to re-create it if needed
  - Offer only basic transformations : map, reduce, filter, foreach ...
- Catalyst optimizer (= Spark SQL engine)
  - Input = SQL or dataframe or datasets
  - Analyse code & generate an AST. Validate cols names & operations logic
  - Logical optimization : rule based. Generate multiple execution plans.
    Use cost-based optimization to assign a cost to each one
  - Physical planning : pick the best logical execution plan to gen the physical plan.
    = a list of RDD operations to plan the execution on the cluster
  - Code generation : Java bytecode to run on each machine
- DataSet API : Strongly typed, JVM native objects. Not to be used in python
- DataFrame : if Spark SQL is not enough
- Spark SQL


Spark Databases & tables
- Internal Spark databases : Tables + views
  - Spark Tables :
    - Table data inside the Spark Warehouse : Parquet format by default
    - Table metadata in the Catalog Metastore : schema, db name, table name, partitions
      and file physical location
  - Spark Views : Only metadata inside Catalog Metastore
- Managed tables
  - `df.write.saveAsTable("db.table_name")`
  - Can set bucketing & sorting
- Unmanaged tables (external table) to reuse existing data files
  - Manage metadata
  - Must set location at creation to be able to get data


Config
- Config folder in $SPARK_HOME/conf
- Logging : must configure log4j to get the worker logs. Python logging don't allow to access worker logs

Run :
- Each task will create a driver process in the master node.
- Then the driver will create an executor process in worker nodes

Run params :
- Cluster manager : local[n], yarn, kubernetes, mesos, standalone
- Deployment modes :
  - Client mode : driver on the client host, slave/executor in the spark cluster
  - Cluster mode : driver inside the spark cluster

Data sources :
- Supported data sources for input & output :
  - JDBC : Oracle, SQL server, PostgreSQL ...
  - NoSQL : Cassandra, MongoDB ...
  - Cloud : Snowflake, Redshift ...
  - Stream : Kafka, Kinesis ...
- Use external data :
  - Use a data integration tool (talend, AWS Glue ...) to ingest data : best for batch process
  - Use Spark data source API to direct connect : best for stream process
- Internal data source : HDFS, S3, GCS, Azure blob
  - Supported file format : CSV, JSON, Avro, Parquet
  - Supported tables : Spark SQL Tables & Delta Lake
