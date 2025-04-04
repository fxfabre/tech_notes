

## Pain points
- df.saveAsTable(...) : must call spark.enableHiveSupport()

## Spark-sbmit options
- master : yarn or local[n]
- deploy-mode : client or cluster = position du App driver
  - client mode used for interactive workloads : notebooks, spark-shell, pyspark & spark-sql
- driver-cores, num-executors, executor-cores
- driver-memory, executor-memory


## Useful methods
- Session
  - .getOrCreate
  - .master("local[3]")
- SparkContext : spark.sparkContext
  - .getConf().get("spark.app.name")


2 ways to read a file :
- The generic way, that support all available file format
    ```python
    spark.read \
        .format("csv").option("header", "true").option("inferSchema", "true") \
        .load("/file/path.csv")
    ```
- The helpers function, to make it easier for common formats
    ```python
    spark.read
        .csv("/file/path.csv", header=True, inferSchema=True)
    ```

Set Data schema :
- `.option("inferSchema", "true")` -> not reliable for digits, dates ...
- Use explicit schema :
  - StructType([StructField("name", "jvm_type"), StructType(...)])
  - DDL string : "col_id INT, col_name STRING, col_date DATE"
- Use implicit schema, contained in the file format : parquet

Read options :
- .format("csv"), .format("parquet") ...
- .option("header", "true")
- .schema(StructTypeObject) or .schema("ddl string")
- .option("mode", "FAILFAST") or "skip row" or "replace with null"
- .option("dateFormat", "y/M/d")

Write options `df.write` : DataFrameWriter
- .format("csv") ou "parquet" (default), "redshift", "mongodb", "deltalake" ...
- .option("path", "/path/to/file.parquet")
- .mode("append"), or "overwrite" or "errorIfExists" or "ignore"
- .partitionBy(cols) -> 1 file per partition
- .bucketBy(num_buckets, cols) : to reduce the number of partition when too many different values in cols
- .sortBy(...) : often used with .bucketBy. -> sorted buckets
- .maxRecordsPerFile()
- .save()

Spark dataframe functions `pyspark.sql.functions`
- run SQL on a df with `expr`: df.withColumn("city", expr("capitalize_udf(city)"))
- Add an id autoincrement : `.withColumn("id", monotonically_increasing_id())`
- .drop(col1, col2)
- .dropDuplicates([col1, col2])
- .sort(expr("col DESC"))
- .selectExpr : same as select, but all colums are expr : to be parsed like SQL
- .groupby().agg(f.sum("col").alias(sum_col"), f.avg(...).alias(...))

Column functions : on expr("...") or col("...")
- Cast : `.cast(IntegerType())`
- Rename

Partitions :
- Display nb partition : `df.rdd.getNumPartitions()`
- Display rows per partition : `df.groupBy(spark_partition_id()).count().show()`  
  Does not display empty partitions
- Why partitionning : run jobs in parallel + don't read useless partitions
- Target file size : 500Mo to few Go
- `df.repartition(n)` -> creates n partitions of equal size
- `df.writer.partitionby(col1, col2)` : partition files

Joins : join data split on different workers
- Shuffle join / shuffle partitions
  - Choose : how many shuffle partitions we want `spark.conf.set("spark.sql.shuffle.partitions", 3)`
  1. Each worker send records to the "map exchange" based on the join key
  2. Reduce exchange will collect all records with the same join key -> "shuffle partitions"
- Broadcast join

