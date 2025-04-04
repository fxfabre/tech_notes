## WAREHOUSE : Equivalent VM
- Provide compute resources

Types of warehouses :
- Standard : for general use
- Snowpark optimized : memory intensive (ML training)
  - Smallest size is MEDIUM
  - Cost 25% more than standard
Multi-cluster warehouse
  - For many users sharing the same warehouse -> auto scaling
  - Not for complex workloads (ML)
  - Mode "maximized": Always to maximum size. min size == max size
  - Mode "auto scale": Can add new cluster
    - Scaling policy "standard" : minimize queuing
      start a new cluster when there is a waiting task
      stops if, for the last 3 min, tasks can be redistributed to other clusters
    - Scaling policy "economy" : more conservative  
      start when there is enough task for a server to work for 6 min
      stops if, for the last 6 min, tasks can be redistributed to other clusters

Tips :
- Enable auto suspend - auto resume 


```sql
CREATE OR REPLACE WAREHOUSE wh_name  --> Create & use it
    WAREHOUSE_SIZE = 'xsmall'
    WAREHOUSE_TYPE = 'standard'
    AUTO_SUSPEND = 60 -- seconds
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    MAX_CLUSTER_COUNT = 3
    COMMENT = 'demo build warehouse for tasty bytes assets';
SHOW WAREHOUSES;
USE WAREHOUSE wh_name;

-- Require MODIFY privilege
ALTER WAREHOUSE wh_name SET warehouse_size=MEDIUM AUTO_RESUME = FALSE;

DROP WAREHOUSE wh_name;
```

- Scale up & down (Resizing) : change warehouse to a bigger / smaller one. Finish current running queries first.
- Scale out = automatic extend current server to add more computing power (don’t stop current server, just add more computing power)
- Scale in = go back to it’s original size = snapping back
- Elastic Data Warehouse = Multi cluster Warehouse : Accessible uniquement à partir de enterprise edition

Dedicated warehouse
- Isolate workload of specific user
- Differennt type of workload -> different warehouse

Privileges
- APPLY : Set a tag
- MODIFY : ALTER & assign to a resource monitor (only AccountAdmin can assign a wh to a resource monitor ?)
- MONITOR : View current & past queries + usage stats
- OPERATE : change state (start, stop, suspend, resume) + view queries + abort any running query
- USAGE : run query
- MANAGE : MODIFY + MONITOR + OPERATE
