# ML flow

## Généralités ML
ML lifecycle :
- loop : build, training, evaluate, update params
- deploy
- Monitoring : accuracy decrease with time in prod = data drift

Challenges :
- 80% des modèles ne vont jamais en prod
- DS et OPS ne parlent pas la même langue

Deploy to prod :
- package -> docker
- Perf / test -> scaling, load balancing, GPU
- Instrumentation : repo management, security -> reproductibility
- Monitoring : accuracy, drift
- Automation : continous training

A gérer :
- Config, data collection, feature extraction
- Versionning, Resource management, Analysis tool, monitoring, Serving

## ML Flow
4 components :
- Tracking : compare parameters, results, training data
- Projet : Package code
- Models : package models
- Registry : model versioning, API & UI to manage models, Search interface, Metadata

Tracking :
- Run = a single execution. Can record (code version, hyper params, metrics, tags ...)
- Experiment = logical grouping of runs, to organize & compare runs

mlflow functions
- set_tracking_uri(uri)
  - uri = null : use local folder "mlruns"
  - uri = "file:/path/to/folder" or "./folder_name" : use this folder
  - uri = remote path "https://server:5000" : use this server
  - uri = databricks workspace "databricks://profile_name"
- Experiments
  - mlflow.create_experiment, mlflow.set_experiment, mlflow.get_experiment
  - arg "artifact_location" : to store models in a different folder
- start_run()
  - new mlflow run : run_id, experiment_id, run_name [...]

Env vars :
- MLFLOW_EXPERIMENT_ID
- MLFLOW_EXPERIMENT_NAME

## Valohai
Structure :
- Organisation
- Teams
- Projects

Modules :
- Knowledge repo : versions of models, metrics
- Smart orchestration : run models & experiments
- Developer core : models from any lib

Functionnalities :
- SSO, set access on Org, team or project
- Train model, set python code & data -> auto allocate VM, store model to registry
- Jupyter plugin : select project, env (cloud VM), run remote
- CLI & API
- Manage datasets
- View current tasks running (step name, graph training metrics, VM, docker img used, pip deps, training data, eval VM cost)
- Pipeline : config with yaml (train, evaluate, deploy)
- Manage deployments
