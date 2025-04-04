- Create free trial account
- Create a storage account
  - Set a resource group : "demo_account"
  - Set storage_account_name : "demostorageaccount"
  - Use same region as Snowflake to reduce costs
- Create a container
  - Set container_name : "csvcontainer"
  - Go to properties : copy container URL
- Go to Azure Active Directory -> Overview
  - In "Basic information", copy the `Tenant ID` (UUID)
- Create a `STORAGE INTEGRATION` object in Snowflake
```SQL
CREATE STORAGE INTEGRATION azure_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = AZURE
  ENABLED = TRUE
  AZURE_TENANT_ID = 'YOUR_TENANT_UUID'
  STORAGE_ALLOWED_LOCATIONS = (
   'azure://account_name.blob.core.windows.net/csvcontainer',
   'azure://account_name.blob.core.windows.net/container2'
  );
```
- Describe storage integration to copy `AZURE_CONSENT_URL`
  - `DESC STORAGE INTEGRATION azure_integration`
  - Go to the URL and grant permission
- Go to Azure -> Enterprise applications -> All applications
  - Copy the name of the Snowflake app
- Go to Azure, on the storage account
  - Go to "Access control (IAM)"
  - Click "Add" -> "Role assignment"
  - Search for "Storage Blob Data Contributor" -> Click "Select"
  - "Members" : "Select members" -> Type the name of the Snowflake app (from previous step)
  - "Select" + "Review + assign"

In Snowflake :
- Create a "file format"
- Create a stage using the storage integration + file format
```sql
CREATE OR REPLACE STAGE stage_name
  STORAGE_INTEGRATION = azure_integration
  URL = 'azure://account_name.blob.core.windows.net/csvcontainer'
  FILE_FORMAT = file_format_name;
```



