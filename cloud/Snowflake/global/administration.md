# Interface administration

## Calcul des couts
Calcul des couts basés sur 4 critères, dépendant de edition snowflake + région :
- Stockage moyen compressé utilisé sur le mois
- Temps CPU utilisé
- Cloud services (billing AWS, GCP, Azure) for state management & coordination. Up to 10% of daily compute credits included.
- Serverless features like snowpipe, replication & clustering
- Data stansfer ?

## Consumption > Budget

- Must be manually enabled with a SQL function
- Projections of where your usage might be heading for the month.

## Observability

- Alerts : takes an action when a condition is met
Check if query is taking too long
    
    ```sql
    CREATE ALERT my_alert
      WAREHOUSE = 'wh_name'
      SCHEDULE = '1 minute'
      IF (
        EXISTS(SELECT ... FROM ...)
      ) THEN
        INSERT INTO table_name VALUES(current_timestamp());
    ```
    
- notifications : similar
    
    ```sql
    CALL SYSTEM$SEND_EMAIL ('src@email.xx', 'dst@email.xx', 'title', 'content');
    ```
    
- Logs, events : log messages, error from stored proc, …
    ```sql
    CREATE EVENT TABLE db.schma.tble;
    ```
    
- Visual DAG viewer → to view dependencies between tasks
