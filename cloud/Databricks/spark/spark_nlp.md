# Lancement Spark

- A partir de [https://github.com/bitnami/bitnami-docker-spark](https://github.com/bitnami/bitnami-docker-spark)
    
    [https://hub.docker.com/r/bitnami/spark](https://hub.docker.com/r/bitnami/spark)
    
    ```
    git clone [git@github.com](mailto:git@github.com):gettyimages/docker-spark.git
    docker-compose up -d
    docker exec -it docker-spark_master_1 /bin/bash
    curl https://s3.amazonaws.com/auxdata.johnsnowlabs.com/public/jars/spark-nlp-assembly-2.7.5.jar --output $SPARK_HOME/jars/spark-nlp-assembly-2.7.5.jar
    ```

- Ajouter les jar de Spark NLP
    
    Section `FAT JARs` in [https://github.com/JohnSnowLabs/spark-nlp/releases/tag/2.7.5](https://github.com/JohnSnowLabs/spark-nlp/releases/tag/2.7.5)
    
    curl [https://s3.amazonaws.com/auxdata.johnsnowlabs.com/public/jars/spark-nlp-assembly-2.7.5.jar](https://s3.amazonaws.com/auxdata.johnsnowlabs.com/public/jars/spark-nlp-assembly-2.7.5.jar) --output /opt/bitnami/spark/jars/spark-nlp-assembly-2.7.5.jar
    

cmd : 

- CMD ["bin/spark-class" "org.apache.spark.deploy.master.Master"]

# **Spark NLP**

Installation

- [https://nlp.johnsnowlabs.com/docs/en/install](https://nlp.johnsnowlabs.com/docs/en/install)
- [https://cedric.cnam.fr/vertigo/Cours/RCP216/tpNlp.html](https://cedric.cnam.fr/vertigo/Cours/RCP216/tpNlp.html)
- [https://www.youtube.com/watch?v=RZYXTSqV-mQ](https://www.youtube.com/watch?v=RZYXTSqV-mQ)

Utilisation

- [https://nlp.johnsnowlabs.com/docs/en/concepts](https://nlp.johnsnowlabs.com/docs/en/concepts)
- [https://nlp.johnsnowlabs.com/docs/en/pipelines#french](https://nlp.johnsnowlabs.com/docs/en/pipelines#french)
- [https://databricks.com/fr/session_na20/advanced-natural-language-processing-with-apache-spark-nlp](https://databricks.com/fr/session_na20/advanced-natural-language-processing-with-apache-spark-nlp)
- [https://github.com/maobedkova/TopicModelling_PySpark_SparkNLP/blob/master/Topic_Modelling_with_PySpark_and_Spark_NLP.ipynb](https://github.com/maobedkova/TopicModelling_PySpark_SparkNLP/blob/master/Topic_Modelling_with_PySpark_and_Spark_NLP.ipynb)

## Spark run

- [https://www.xspdf.com/resolution/58409596.html](https://www.xspdf.com/resolution/58409596.html)
- Lemmatizer :
    - en, fr, de, it, portugais pt, es
    - dutch nl, norwegian nb, finnois fi, suedois sv
    - polonais pl
    - russe ru
    - bulgare bg
    - tcheque cs
    - grec el
    - hongrois hu
    - roumain ro
    - slovaque sk
    - turque tr
    - ukrainien uk
- The model with 7 languages: Czech, German, English, Spanish, French, Italy, and Slovak
- The model with 20 languages: Bulgarian, Czech, German, Greek, English, Spanish, Finnish, French, Croatian, Hungarian, Italy, Norwegian, Polish, Portuguese, Romanian, Russian, Slovak, Swedish, Turkish, and Ukrainian
- Pas de modèle multi langue

Java :

- Morpha stemmer

# Documentation

- [https://medium.com/spark-nlp](https://medium.com/spark-nlp)
- [https://towardsdatascience.com/diy-apache-spark-docker-bb4f11c10d24](https://towardsdatascience.com/diy-apache-spark-docker-bb4f11c10d24)



Spark

- Docker setup from [https://github.com/sdesilva26/docker-spark](https://github.com/sdesilva26/docker-spark)
- [https://spark.apache.org/docs/latest/quick-start.html](https://spark.apache.org/docs/latest/quick-start.html)
- [https://spark.apache.org/docs/latest/api/python/pyspark.html](https://spark.apache.org/docs/latest/api/python/pyspark.html)
- [http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.SparkContext](http://spark.apache.org/docs/latest/api/python/pyspark.html#pyspark.SparkContext)

Spark Streaming

- [https://spark.apache.org/docs/latest/streaming-programming-guide.html](https://spark.apache.org/docs/latest/streaming-programming-guide.html)

Spark NLP

- Notes :
    - Certainement beaucoup de potentiel : scalabitité + perf
    - Mais qualité pas au niveau : "Nous n'avions pas ..." ⇒ "n'" n'est pas séparé, le verbe ne passe pas à l'infinitif. Idem avec les l'
    - Documentation incomplète, beaucoup de mal à avoir un serveur up et fonctionnel.
- Liens:
    - [https://github.com/JohnSnowLabs/spark-nlp](https://github.com/JohnSnowLabs/spark-nlp)
    - [https://github.com/JohnSnowLabs/spark-nlp-workshop](https://github.com/JohnSnowLabs/spark-nlp-workshop)
    - [https://spark-packages.org/package/JohnSnowLabs/spark-nlp](https://spark-packages.org/package/JohnSnowLabs/spark-nlp)
    - [https://spark.apache.org/docs/latest/api/python/pyspark.html](https://spark.apache.org/docs/latest/api/python/pyspark.html)
    - [https://nlp.johnsnowlabs.com/docs/en/install](https://nlp.johnsnowlabs.com/docs/en/install)[https://nlp.johnsnowlabs.com/docs/en/transformers](https://nlp.johnsnowlabs.com/docs/en/transformers)
- Articles / cas d'usage :
    - [https://medium.com/trustyou-engineering/topic-modelling-with-pyspark-and-spark-nlp-a99d063f1a6e](https://medium.com/trustyou-engineering/topic-modelling-with-pyspark-and-spark-nlp-a99d063f1a6e)
- Articles / comparatifs :
    - [https://www.oreilly.com/content/comparing-production-grade-nlp-libraries-accuracy-performance-and-scalability/](https://www.oreilly.com/content/comparing-production-grade-nlp-libraries-accuracy-performance-and-scalability/)
    - [https://www.oreilly.com/content/comparing-production-grade-nlp-libraries-training-spark-nlp-and-spacy-pipelines/](https://www.oreilly.com/content/comparing-production-grade-nlp-libraries-training-spark-nlp-and-spacy-pipelines/)
    - ⇒ Une blague. Ecrit par un dev de Spark NLP, regarde juste le temps d'exécution où le nombre de mots sans regarder la qualité
- Doc Youtube :
    - [https://www.youtube.com/channel/UCmFOjlpYEhxf_wJUDuz6xxQ/videos](https://www.youtube.com/channel/UCmFOjlpYEhxf_wJUDuz6xxQ/videos)

# Monitoring
[http://localhost:8080/](http://localhost:8080/)

[http://localhost:4040/jobs/](http://localhost:4040/jobs/)


# Ecosysteme Hadoop
- Spark : moteur de calcul qui effectue des traitements distribués en mémoire sur un cluster
- Hive : fournit un langage de requête basé sur le SQL : HiveQL
- Pig : ETL. Environnement d'exécution de flux interactifs de données. Langage Pig latin
- Hbase ; SGBD distribué, orienté-colonne
- Sqoop : import / export SGBDR <—> hadoop 
- Storm : une implémentation logicielle de l'architecture λ
- ZooKeeper est le moyen utilisé par Hadoop pour coordonner les jobs distribués.
- Oozie : planificateur d'exécution des jobs


# Scala sample
```scala
val texteEn = spark.read.textFile("texteEn.txt").toDF("text").where(length($"text") > 0)
val explainPipelineModel = PretrainedPipeline("explain_document_ml").model
val finisherExplainEn = new Finisher().setInputCols("token", "lemma", "pos")
val pipelineExplainEn = new Pipeline().setStages(Array(explainPipelineModel,finisherExplainEn))

val modelExplainEn = pipelineExplainEn.fit(texteEn)
val annoteTexteEn = modelExplainEn.transform(texteEn)

annoteTexteEn.show()
annoteTexteEn.select("finished_token").show(false)
annoteTexteEn.select("finished_lemma").show(false)
annoteTexteEn.select("finished_pos").show(false)

val testSentimentData = Seq("The movie was great. But the cinema was quite dirty.").toDF("text")
val sentimentPipelineModel = PretrainedPipeline("analyze_sentiment").model
val finisherSentiment = new Finisher().setInputCols("document","sentiment")
val pipelineSentiment = new Pipeline().setStages(Array(sentimentPipelineModel,finisherSentiment))

val modelSentiment = pipelineSentiment.fit(testSentimentData)
val sentimentTestSentimentData = modelSentiment.transform(testSentimentData)
sentimentTestSentimentData.show(false)
```
