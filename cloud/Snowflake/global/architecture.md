# Architecure of objects & services
- A snowflake Account is restricted to a cloud provider and a single region => Can't deploy an account to multiple cloud regions
- Snowflake’s architecture is best described with multi-cluster shared data architecture which combines the benefits of shared-disk and shared-nothing architecture.
- Warehouses have their own CPU, memory, and local data cache but they can all access a central data repositor.


## Snowflake architecture :
Archi 3 + 1 layers :
- optimized storage
- Multi cluster compute
- Cloud services
- Snowgrid : cross cloud & global

Layer 1 : Optimized storage 
- structured - semi structured - unstructured (pdf, img …)
- Un-soloed access to data
- easily manage data at scale : auto control partitioning, compression, encryption
- Flexibility and interoperability

Layer 2 : Elastic multi-cluster compute
- Power AI, apps, … via a single engine
- High perf & concurrency

Layer 3 : cloud services
- Managed : auto updates & migrations
- sharing, perf optimisation, management, high availability, security, zero copy cloning
- Metadata management

Layer 4 : Snowgrid
- connect across regions & clouds
- replicate & sync accounts, pipelines …


## Object hierarchy :
- Organization : top level. Managed by OrgAdmin, but does not give access to others objects
- Account : restricted to a cloud provider (AWS, GCP, Azure) & a region. Managed by the AccountAdmin
  - Database > schema : Managed by SysAdmin
    - Tables, stage
    - UDF, UDTF, stored proc
    - Task, stream, pipe
  - Warehouse : managed by SysAdmin
  - Roles : Managed by SecurityAdmin
    - Users : Managed by UserAdmin
  - Network policy : Managed by SecurityAdmin
