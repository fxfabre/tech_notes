# Workflows
Config uniquement par UI ?

## Overview
- fully managed task orchestration
- Use nobebooks, SQL, python
- Graphical UI
- DLT pipelines can be a task in a Workflow
- Good for :
  - Jobs running on a schedule, with dependent tasks / steps
  - MLflow notebook task
  - Arbitrary code, External API calls
  - Job can contain : jar, Spark sublit, SQL task, dbt ...
- Create in Workflows -> tab task

## Workflow jobs
- Tasks composed of :
  - notebooks, python script / wheel, SQL file
  - Delta live table pipeline, dbt, JAR, spark submit
  - A task can be a group of sub tasks
- Jobs triggers
  - manual, scheduled, API trigger
  - File arrival, Delta table update, streaming
- Compute instances types
  - Interactive clusters (or all purpuse cluster)
    - Can be shared by multiple users
    - Best for data exploration or dev
    - Should not be used in prod : not cost efficient
  - Job clusters
    - approx 50% cheaper
    - Subject to cloud provider startup time
    - Can be re-used across tasks
  - Serverless workflows
    - Fully managed service, Auto scaling.
    - Lower TCO ? Only pay DBUs, no network / infra cost
    - No longer need to choose the VM type
    - Photon turned on by default
    - Fast startup. VM runs in Databricks account
- Cluster sizing
  - Memory : increases cost + GC execution time
  - Network : check the Spark UI, volume of data shuffled
  - CPU : should always be > 80% usage. 8 to 16 cores per executor

- Jobs types
  - Continuous job : for streaming. After it ends, wait for 1 min and restart
  - Conditional execution : depend on upstream task status
- Parameters / share data
  - Job parameter : given to each task. Set a value inside the notebook, or given as args
  - Job context (dynamic value references) : can reference variables, given as job parameter
  - Task values : to pass values between tasks. See TaskValues object to read
- Job features
  - Late jobs : can define a "soft timeout". If job runs longer, trigger a notification
  - Can configure jobs from git repo
  - Webhooks for jobs. Event driven integration with databricks : on start, on success, on failure
  - By default, jobs runs as the identity of the owner. Can be set to use a different identity.
  - Databricks Asset Bundles (DAB) : collection of 
    - Artifacts : jobs, ML models, DLT pipeline & clusters
    - Assets : python files, notebooks, SQL queries & dashboards
  - Repair run : on a failed run, allow to change parameters to rerun this task
- Best practices
  - Use Job clusters for production, All purpuse cluster for dev only
  - Use latest LTS databricks runtime (DBR)
  - Prefer multi task jobs (soon limited to 1000 tasks in a job)
    - Each task can run on its own cluster
  - Cluster re-use : enable tunning tasks in a databricks job on the same cluster
    - More efficient cluster usage, reduce job latency
  - Enable Photon. Multipliers apply (for price ?)
  - Use repair & re-run, late jobs and serverless to save time & money