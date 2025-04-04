# Points à réviser

outils complementaires à voir :
- yarn, k8s
- exchanges

## Archi, composants & definitions
- Catalyst optimizer : faire optim pour trouver chemin le plus court pour exécuter la requete (python, SQL, scala, autre ?)
- DAG : plan d'exécution logique, transformé en plan physique au run

Spark DF vs pandas DF
- spark est lazy

Opérations
- Transformations : Opération lazy
- Action : show, write.table, collect ... : lance l'exécution des transformations en attente


Vrac :
- Shuffle : réordonner les data. Utile pour groupby, sort ou join par exemple. Redistribuer les données pour optimiser traitement
- Explain : plan physique, p26
- Create or replace tmp view pour utiliser SQL
- RDD : Collection d'objets distribués.
  - Dataframe : API plus récente, RDD sous forme de tableau
  - Datasets : accessible uniquement en scala, collection de rows
  - p57 : DF vs dataset
- Les types doivent correspondre aux types JVM
- Catalog : passer du "unresolved logic plan" to "resolved logic plan"
  - was : hive metastore
  - Contient metadata de la table
  - Databricks ont dev le Unity catalog en remplacement de Hive
- Lire p260 : On n'utilise plus trop spark context. Spark session is enough
- Tester si je peux me creer un compte Databricks community edition
- Mecanismes de cache
  - Si .show et .write sur une meme DF -> lance 2x le job
  - Utiliser .collect pour le recuperer sur le driver (client)
  - Utiliser .persist pour sauv l'etat du traitement sur workers
- Broadcast variables : 
  - Peut eviter un shuffle, apres un join.
  - Broadcast une petite table sur chaque worker automatique si < 10M (broadcast join)
- cluster manager : yarn, k8s
  - option pyspark --master yarn

## Runtime archi
- Submit a job with "spark-submit"
- Request is handled by Yarn ressources manager (Yarn RM)
- Yarn RM will create 1 Application Master (AM) Container on a worker
  - AM contains PySpark driver & JVM Application driver
  - PySpark driver use Py4J to call java functions
- Application driver ask Yarn RM for executors containers
- Application master & executors containers runs JVM to run Spark
  - Add a PySpark driver in the Application Master container if running python
  - Add a Python worker in the executor container if using custom libs or python UDF
- Spark application will start Jobs
- Jobs are split into stages
- Stages are composed of parallel tasks
- A task can run on an executor on 1 thread only


## Dataframe operations
- Actions : trigger a spark job & return to the spark driver
  - **read, write, collect, show**, count, descrive, first, foreach, foreachPartition, 
  - head, summary, tail, take, toLocalIterator
- Transformations : Lazy produce a new dataframe
  - agg, crossJoin, crosstab, cube, drop, filter, groupby, join, orderBy, limit,
  - sample, select, sort, union, where,  ...
  - Narrow dependency partition : Each worker can apply the transformation without knowding data on the others workers.
    Transformations runs independently on each worker.
    Simply merge transformation from each worker to get the complete result
    eg : .select, filter, withColumn, drop
  - Wide dependency partition : require data from others partitions to produce valid results
    Require a *shuffle & sort* operation. Split partition by key to make transformation independent
    eg : .groupby, join, cube, rollup, agg ...
- Utility functions or methods
  - approxQuantile, cache, checkpoint, create(global)TempView, explain,
  - persist, toDf, toJson, unpersist, writeTo, withWatermark ...

## Jobs, stages, task
- A job is a succession of transformations + 1 action.
  The code is split after each action to determine all jobs to run = the logical execution plan.
- Inside each job : Split tranformations after each wide transformation.
  A Stage is some narrow tranformation + 1 wide transformation.
  The stage finished by writing to the write exchange (the output of the wide transfo).
  Next stage reads from "read exchange". Read & write exchanges can be on different workers. 
  A copy is required from Write to Read exchange = "Shuffle / Sort" operation : réorder data to finish wide transfo
- A Task contains all transformations inside a Stage.
  Task = 1 data partition + a suite of transformations
  If there are many partitions in the data -> 1 Task for each partition => indépendant operation, runs in parallel
- Runtime execution plan : contains read / write exchanges, shuffle Sort & parallel tasks
- Slots = 1 core on the executor. Memory shared between cores.

## Memory
- Driver memory
  - spark.driver.memory : dedicated memory for the driver process (Spark context)
  - spark.driver.memoryOverhead = 0.1 : max(10% spark.driver.memory, 384 Mo).
    Memory overhead = used by container process or any non-JVM process
- Executor memory (container memory)
  - spark.executor.memoryOverhead
  - spark.executor.memory
  - spark.memory.offHeap.size
  - spark.executor.pyspark.memory
  - yarn.scheduler.maximum-allocation-mb = max worker memory
  - yarn.nodemanager.resource.memory-mb
- JVM executor memory = spark.executor.memory
  - Reserved memory = 300 Mo for spark engine
  - Spark Memory = 60% of (spark.executor.memory - 300 Mo)
    Proportion def by spark.memory.fraction = 0.6 by default.
    - Split into Storage memory pool. spark.memory.storageFraction = 0.5 by default.
      Cache memory for data frame
    - And executor memory pool : buffer memory for DF operations
    - The limit between Storage & executor memories is not a hard limit.
  - User Memory = 40% of (spark.executor.memory - 300 Mo)
    Used for user defined data structures, spark internal metadata, UDF, RDD conversions operations, RDD lineage & dependency

## Adaptative query Execution (shuffle partitions, join strategies & skew joins)
**Adaptative query Execution - coalesce shuffle partitions** 
- Shuffle operations have a high impact on Spark performance
- Tune it with spark.sql.shuffle.partitions
- If number of partitions too small :
  - Large partitions size, need large amount of memory -> Out Of Memory exception
  - Reduce parallelization -> slower
- Large number of partitions
  - Small partitions -> inefficient
  - Many network IO => inefficient
  - Overload on the Spark Task Scheduler
- Enable Adaptative Query Partitions AQE to
  - Estimate the size of all groups of data
  - Combine small groups into one partition
  - Find a good (the best ?) shuffle partition number
- To enable coalesce shuffle partitions :
  - spark.sql.adaptive.enabled
  - spark.sql.adaptive.coalescePartitions.initialPartitionNum (max number of partitions)
  - spark.sql.adaptive.coalescePartitions.minPartitionNum (default = number of cores)
  - spark.sql.adaptive.advisoryPartitionSizeInBytes (default = 64 Mo)
  - spark.sql.adaptive.coalescePartitions.enabled

**AQE - switching join strategies**
- The physical execution plan is computed without knowing the size of data to use.
  If large table, but filter to keep few rows : the physical plan will do shuffle sort,
  but better to do a broadcast join
- One table must be shorter than `spark.sql.autoBroadcastJoinThreshold`
- AQE compute the table size at shuffle time
- Replans the join strategy at runtime converting a shuffle sort join to a broadcast hash join

**AQE - optimize skew joins**
- Skew join, one join need a lot of RAM memory to run.
- Enable / parametrize with :
  - spark.sql.adaptive.enabled = true
  - spark.sql.adaptive.skewJoin.enabled = true
  - spark.sql.adaotive.skewJoin.skewPartitionFactor (default 5).
    Partition Skewed if 5x the size of the medium partition size
  - spark.sql.adaotive.skewJoin.skewPartitionThresholdInBytes (default 256 MB)
- Split the left data (or right, the larger one) into 2 splits, and duplicate the other side.
  Create 2 smaller tasks from 1 task

**Dynamic partition prunning DPP, spark 3.0**
- Predicate pushdown : apply the where filters as early as possible, 
  while reading the input files if partition on the good column.
- Partition prunning : Ignore others partition
- To apply DPP :
  - Spark >= 3.0, enabled by default
  - Have 1 fact table partitioned (large)
  - Broadcast the dimension table (small)

**Caching DF in Spark memory**
- Spark memory divided into :
  - Executor memory pool (50% by default) to run DF computations
  - Storage memory pool to cache DF
- .cache() : use Storage memory, and swap on disk if needed. Cache 1 full partition or nothing. Not half of it.
- .persist(storage_level) : Can config storage level, ie which memory to use (memory, disk, off heap)
- df.unpersist() to remove both caches

**Repartition & Coalesce**
Repartition :
- Default number of partitions in `spark.sql.shufflePartitions`
- wide transformation, cause a Shuffle sort
- .repartition(num_partition, *cols) : hash based partitionning, same size partitions
- .repartitionByRange(num_partitions, *cols) : based on range of values. Partitions may have different sizes
  Require data sampling to determine partition range
- When to apply :
  - reuse partitions with repeted cols filters
  - Too large partitions, skewed partitions
  - Do not repartition to reduce number of partitions

Coalesce :
- To reduce the number of partitions, keep data on the same worker
- Do not cause a shuffle sort
- Can cause skewed partitions

**DF hints**
- df.hint()
- select /* hint ... */ * from ...

**Broadcast Variables**
- Used only in low level RDD
- Can use a local dict (or any var) in a func, as a udf -> Create a closure function
  Spark will broadcast it to each Task.
- Convert it as a broadcast var with : spark.sparkContext.broadcast(local_var)
  to broadcast it to each worker.
- If number of Tasks is >> number of workers, closure function will use more network

**Accumulators**
- acc = spark.sparkContext.accumulator(0)
- Global mutable variable
- Can update them per row basis
- Useful to implement counter & sums
- Can be used in actions - Spark guarantee accuracy
- Not recommended to use in transformation, may be wrong in case of job failure

**Speculative execution**
- Try to accelerate long running jobs by running it twice. Keep result from the fastest
- Usefull when the task is slow due to the worker node : overloaded, hardware issue ...
  Usefull when the task duration has high variance ?
- Do not help with skew data or worker having low memory
- enable with `spark.speculation = true` (default = false)
- `spark.speculation.interval = 100ms`
- `spark.speculation.multiplier = 1.5` : considered too long if 1.5x longer than median duration
- `spark.speculation.quantile = 0.75` : duplicate task if 75% of others tasks are finished
- `spark.speculation.minTaskRuntime = 100ms`
- `spark.speculation.task.duration.threshold = None`

**Sheduler**
Scheduling across applications
- Keep some spare workers in case a small / new job is submited to the cluster
- Resource allocation :
  - Static allocation : executors are attributed at the application level, for all stages. 
    - It allocate as many executors as asked by the biggest stage. Some executors stay idle during smaller stages. 
    - The executors are all released at the same time, when the app is finiched
  - Dynamic allocation : disabled by default.
    - `spark.dynamicAllocation.enabled = true`
    - `spark.dynamicAllocation.shuffkTracking.enabled = true`
    - `spark.dynamicAllocation.executorIdleTimeout = 60s` : release executor if idle for 60s
    - `spark.dynamicAllocation.schedulerBacklogTimeout = 1s` : request more executors if tasks waiting for more than 1s

Scheduling within an application
- By default, the app will run jobs sequentially.
- But if 2 jobs are independent, use python threads to submit them in parallel -> create competition within those jobs
- By default, spark job scheduler run tasks in FOFO order
- Use `spark.scheduler.mode = FAIR`
  - Sheduler will pick a task from job 1, then from job 2, then back from job 1 and so on. (Round robin job allocation)
  - All jobs will have running tasks









