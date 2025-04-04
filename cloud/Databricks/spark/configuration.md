# Configuration

## Spark config
- Config dir : SPARK_CONF_DIR = $SPARK_HOME/conf
- Config files
  - spark-defaults.conf : environmental settings when running spark-submit
  - log4j2.properties : https://logging.apache.org/log4j/2.x/manual/configuration.html
- Set config in code
    ```python
    from pyspark import SparkConf
    from pyspark.sql import SparkSession
    conf = SparkConf().set("spark.hadoop.abc.def", "xyz")
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    ```
- Set config at runtime
    ```bash
    ./bin/spark-submit \
      --name "My app" \
      --master local[4] \
      --conf spark.eventLog.enabled=false \
      --conf "spark.executor.extraJavaOptions=-XX:+PrintGCDetails -XX:+PrintGCTimeStamps" \
      --conf spark.hadoop.abc.def=xyz \
      --conf spark.hive.abc=xyz
      myApp.jar
    ```

  
### Log4J config
Structure : 
- paramètres généraux
- définition des appenders
- définition des loggers (pour des packages ou classes spécifiques)
- root logger


## Hadoop config
- conf dir : HADOOP_CONF_DIR = /etc/hadoop/conf
  - To be defined inside $SPARK_HOME/conf/spark-env.sh
- Config files :
  - hdfs-site.xml, which provides default behaviors for the HDFS client. 
  - core-site.xml, which sets the default filesystem name.
  - yarn-site.xml
  - hive-site.xml

