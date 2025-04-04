# Security
- Snowflake use a hierarchical key model which is rooted in a hardware key

## Discretionary access control (DAC)
- Each object has an owner.
- Authentication : prove your identity, who you are
- Authorization : prove your role, you are allowed to do it

Key concepts
- Securable object : access can be granted, denied by default. An object is owned by only one single role
  Organization, account, user, roles, warehouse, database ...
- Privilege : Defined level of access
- Role : privileges granted to role. Role assigned to roles & users
- User : identity associated with a person or program

Proces :
- When an object is created : owned by the current role
- The role can grant access to another role
- Multiple privileges can be assigned to a role
- Multiple roles can be assigned to a user

Hierarchy of objects
- Organization > account > database > schema > tables
- To access a table, a user must have enough privileges (usage) on parent object (schema, db ...)

Operations :
- Grant a privilege : `GRANT <privilege> ON <object> TO <role>`
- Revoke a role : `REVOKE <privilege> ON <object> FROM <role>`
- Grant role : `GRANT <role> TO <user>`

6 system defined roles in any account - can add role, but can't revoke role / delete :
- OrgAdmin → Peut lier / gérer plusieurs comptes Snowflake ensemble
Role a part, pas directement lié aux autres roles. Create / view accounts, view account usage information
- AccountAdmin → role par défaut, tous les droits (create shares, resource monitor). SysAdmin + Security Admin
- SysAdmin (ops) → Create DB, tables, warehouse
- SecurityAdmin : manage grants to any objects + UserAdmin
- UserAdmin - User and Role Administrator
- Public → granted to all users

Inheritance :
- When we are given role “AccountAdmin”, we automatically get SecurityAdmin & SysAdmin
- A higher role can impersonate a lower role anytime = act as this role, with lower access
- AccountAdmin > SecurityAdmin > UserAdmin > Public
- AccountAdmin > SysAdmin

Best practices 
- Add custom roles under SYSADMIN

Global privileges
- CREATE / IMPORT a share
- APPLY MASKING POLICY
Warehouse privileges :
- MODIFY : alter properties
- MONITOR : view executed queries
- OPERATE : change the state (suspend / resume manually)
- USAGE : use & run queries
- OWNERSHIP : full control
- ALL : all except ownership
Databases pribileges :
- MODIFY : alter props
- MONITOR : run DESCRIBE
- USAGE : use & execute SHWO DATABASES
- REFERENCE_USAGE : can use a shared secure view to reference another object in a different database
- ALL, OWNERSHIP, CREATE SCHEMA
Stages privileges
- READ, Internal stage only : perform read operations (GET, LIST, COPY INTO)
- WRITE, Internal stage : perform write operations (PUT, REMOVE, COPY INTO)
- USAGE, External stage : can use it
- ALL, OWNERSHIP
Tables privileges
- SELECT, INSERT, UPDATE, TRUNCATE, DELETE, ALL, OWNERSHIP


## MFA
- Multi factor authentication is powered by Duo Security, but managed by Snowflake.
- Available for all editions
- Go to profile, and "Enroll" to activate it
- SecurityAdmin can disable MFA for one user
- Fully supported by web interface, SnowSQL, Snowflake ODBC / JDBC and python connectors.
- MFA token caching can be enabled to reduce number of prompts during authentication. Token valid for 4 hours max. Works with ODBC / JDBC driver + python connector


## Federated authentication - SSO
- Available for all editions
- login, logout & timeout due to inactivity
- Require an External Identity provider (IdP) + service provider (Snowflake)
- Most SAML-2.0 are supported. Native support for Okta and Microsoft AD FS
- Share users : Snowflake support SCIM 2.0. If an account is created in the IdP, Snowflake can create it


## Key pair (Public / Private) authentication
- Only 1 or 2 public keys
- Enhanced security, alternative to basic username / password
- Min : 2048 bit RSA
- `ALTER USER user_name SET RSA_PUBLIC_KEY 'the_key`


## Column level security
- Available on Enterprise Edition
- Dynamic data masking at query time
```sql
CREATE MASKING POLICY my_policy
AS (val varchar) returns varchar ->
    CASE
        WHEN current_role() in (role_name) THEN val
        ELSE '###-###'
    END;

ALTER TABLE table_name MODIFY COLUMN phone
SET MASKING POLICY my_policy;
```
- External tokenization : data tokenized pre-load or via external function. When sensitive data needs to be protected on a column-level but the analytical value of the column needs to be preserved


## Row level security
- Available on Enterprise Edition
- Filter data (add a where condition) dynamically based on user name or role
```sql
CREATE ROW ACCESS POLICY my_policy
AS (col varchar) returns boolean ->
    CASE
        WHEN current_role() = 'role_name' and col = 'value1' THEN true
        ELSE false
    END;

ALTER TABLE my_table ADD ROW POLICY my_policy ON (column_name)
```

## Network policies
- Standard edition
- Restrict access to account based on user IP address
- Deny, allow, Deny : List of allowed / blocked IP address
  - If IP address in Deny list -> blocked
  - Then if IP address in Allow list -> allow
  - Else block -> for all others IP
- Examble : allow 192.168.0.0/16, deny 192.168.1.92
- Support only IP v4

Roles :
- To create : global `CREATE NETWORK POLICY` privilege - included in securityAdmin
- To assign : OWNERSHIP of network policy + OWNERSHIP of user

```sql
USE ROLE SECURITYADMIN;

CREATE NETWORK POLICY my_network_policy
ALLOWED_IP_LIST = ('192.168.1.2', '192.168.0.0/24')
BLOCKED_IP_LIST = ('192.168.1.2');

ALTER ACCOUNT SET NETWORK_POLICY = my_network_policy;
ALTER ACCOUNT UNSET NETWORK_POLICY;

-- Require ownership of user + network policy
ALTER USER SET NETWORK_POLICY = my_network_policy;
```

## Data encryption
Data encrypted at rest
- Automatically by default, for all editions (from Standard)
- For tables & internal stages
- AES-256-bit encryption, Snowflake managed
- Key rotation every 30 days (for new data only, do not translate existing data)
- Old keys kept until all corresponding data deleted
- Can enable re-keying every year (Enterprise edition) to convert all old data to the new key
- Possible to enable client side encryption on external stages

Data encrypted in transit
- Automatically by default, for all editions (from Standard)
- for webUI, SnowSQL, JDBC, ODBC, python connector
- End to end, use TLS 1.2

Tri-secret secure
- Business critical edition
- Enable customer to use own keys
  - Customer managed key : eg Azure key Vault
  - Still use Snowflake managed key
  - both keys generate a composite master key


-------------------------------
Behaviour :

- DAC : Discretionary Access Control : “you create it, you own it”
If SYSADMIN creates a database, they own it
- Each USER has a default role they are assigned. Used role go back to default role when we login
- Ce ne sont pas les personnes, mais les rôles qui détiennent les ressources (base, warehouse …)
    - Je ne peux voir la ressource que si mon rôle actif est suffisant
    - Je peux transferer une ressource à un autre role

Display roles :

- UI : Admin > User & roles > tab “Roles” > Graph

Change role :

- UI for DB or schema → Go to db / schema and on the “…” > “Transfer ownership”

```sql
CREATE ROLE tasty_de;
SHOW GRANTS TO ROLE accountadmin;
USE ROLE tasty_de;
```
