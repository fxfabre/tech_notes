# Automate processings

## Delta live tables DLT
- Declarative ETL framework : batch + streaming
- Workload specific autoscaling
- Good for :
  - ETL job, batch or streaming
  - With data quality constraints, monitoring, logging
  - Can be added as a single task in a Workflow
- Create in Workflows -> tab delta live tables

## Workflow jobs
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
