# SnowFlake

- Essai 120 jours coursera : https://signup.snowflake.com/?trial=student&cloud=aws&region=us-west-2&utm_source=coursera&utm_campaign=introtosnowflake
- New trial account : https://signup.snowflake.com/?utm_cta=website-learn-snowflake-university_cmcw
- Trial account badge 3 : https://signup.snowflake.com/?utm_cta=website-learn-snowflake-university_dabw
- Cours Udemy Nikolai Schuler : https://drive.google.com/drive/folders/1hjfEJ0oFoBrWkN1jXw9pIB1NT20ECFi3
- Cours Coursera DE : https://github.com/Snowflake-Labs/modern-data-engineering-snowflake

Rex certif Snowpro core
```md
    Déroulement examen :
    - 115 minutes, 100 questions
    
    Contenu
    - tables / vues / SQL
    - Stockage S3
    - Interface Snowflake : snowsight, snowcd, driver, connecteur
    - Couts à la minute
    - Archi en 3 couches
    - Gerer données non structurées : json
    - Gestion acces :
        - Historique acces
        - Auth, acces RBAC
        - vue sécurisée
    - Perf
        - Scaling up - out, taille
        - différents cache
        - micro partitionning
        - Resource monitor
        - Search query optim service
    - Data loading :
        - Snowpipe : données sur 14 jours ?
        - Copy into : sur 64 jours ?
        - format fichier
        - commandes de création
    - Data protection & sharing
        - Time travel
        - Fail safe : 7 jours, demande à Snowflake à faire
        - marketplace, data exchange
```

Formation Badge Snowflake
- app: [https://ysa.snowflakeuniversity.com](https://ysa.snowflakeuniversity.com/)
- YOUR UNI ID: 005VI00000E1fSTYAZ
- Your UUID : 8e465cfe-7d49-44f1-98c9-40745e5b7b3b

Objectifs Snowflake (comment ils se vendent ?)
- Réduire les silos entre équipes et données fonctionnelles → Toutes les données sont au même endroit
- Partager facilement des données entre entreprises
- Possibilité d’importer des données facilement via “Data products” > “Marketplace”
- Possibilité d’exécuter des requetes SQL sur des fichiers CSV → 1 seule source de vérité

Types d’abonnement + included features
- Hors abonnement :
  - You don’t need a Snowflake edition to browse the Snowflake marketplace listings
- Standard edition
  - automatic data encrypt, time travel 1 day, 7 days fail safe beyond time travel (need to ask Snowflake)
  - MFA, object level access control,
  - dynamic / external / hybrid tables, iceberg
- Enterprise edition
  - multi cluster warehouse, time travel 90 days, periodic re-keying
  - row/column level security (row access policy, masking policies)
  - data quality / metrics functions
  - materialized view, query acceleration, search optimization
  - Feature store (ML)
- Business critical edition for sensitive data : more security
  - customer key (tri secret secure), data specific regulation, DB failback
- Virtual private Snwoflake
  - dedicated servers, off cloud, isolated from all others SF accounts

Dictionnary :
- Snowsite : Snowflake UI. History tab keep queries for 14 days
- Snowpark : Snowflake tools to use python, and other languages
- Snow SQL : Command line client. Can be installed on Win + Linux + MacOS
- The Account Usage Share : another name for "THE SNOWFLAKE database" → Shared DB

Costs :
- Depends on the region / cloud provider, charged in snowflake credits, less expensive for standard edition
- Warehouse :
  - standard query processing
  - cloud services : only charged if > 10% of warehouse consumption
  - Serverless : Search optimization snowpipe
- Compute
  - Charged for active warehouse
  - Billed by second, min 1 min
  - Depends on size
- On demand Storage
  - Based on average storage used per month
  - Cost calculated after compression
- Capacity storage :
  - cheaper storage, but pay for it, even if not used
- Data transfer :
  - Data ingress : free
  - Data egress : charged, depends on destination (region, cloud provider)

Supported languages :
- Programmatic interfaces : python, Spark, Node.js, .NET, .js, PHP, Go
- UDF : SQL, python, Java, JS, scala
- UDTF : SQL, python, Java, JS
- Stored proc : SQL, python, Java, JS, scala


## Snowflake releases
Weekly new releases : no downtime
- Full releases :
  - New features
  - Enhancements / updates / fixes
  - Behavior changes (monthly schedule) : can impact our code / workload
- Patch releases : only fixes

Release process :
- Day 1 : early access, Enterprise account request it
- Day 1 or 2 : Regular access, Standard account
- Day 2 : Final access, Enterprise account
