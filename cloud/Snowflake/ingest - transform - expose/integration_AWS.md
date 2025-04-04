# Connecter un bucket S3

1. Creer un bucket S3 : `intro-to-snowflake-snowpipe`

2. Go to `IAM` > Account settings : Vérifier que le “security token service” est actif dans la région utilisée par snowflake (US West dans mon cas)

3. Go to `IAM` > Policies > Create policy avec :
Call this policy “snowflake_access” then “Create policy”
    
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": ["s3:GetObject", "s3:GetObjectVersion"],
                "Resource": "arn:aws:s3:::intro-to-snowflake-snowpipe/*"
            },
            {
                "Effect": "Allow",
                "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
                "Resource": "arn:aws:s3:::intro-to-snowflake-snowpipe",
                "Condition": {
                    "StringLike": {
                        "s3:prefix": ["*"]
                    }
                }
            }
        ]
    }
    ```
    
4. Go to `IAM` > roles > Create role
entity type = “AWS account”
AWS account = “This account”, require external ID = “0000” > next
Associate it with the previous policy “snowflake_access”
Name the role : “snowflake_role_snowpipe” > Create role

5. In Snowflake, run with the correct AWS role ARN, and bucket name :
    ```sql
    CREATE OR REPLACE STORAGE INTEGRATION S3_role_integration
      TYPE = EXTERNAL_STAGE
      STORAGE_PROVIDER = S3
      ENABLED = TRUE
      STORAGE_AWS_ROLE_ARN = "arn:aws:iam::626635438523:role/snowflake_role_snowpipe"
      STORAGE_ALLOWED_LOCATIONS = ("s3://intro-to-snowflake-snowpipe/");
    ```
    
6. Then run `DESCRIBE INTEGRATION S3_role_integration;` in Snowflake
To get properties `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID`

7. Go back to IAM > roles > snowflake_role_snowpipe > “Trust relationships”  
And update :
- Statement[Principal][AWS] = valeur de `STORAGE_AWS_IAM_USER_ARN`
- Statement[Condition]…[sts:ExternalId] = valeur de `STORAGE_AWS_EXTERNAL_ID` 
