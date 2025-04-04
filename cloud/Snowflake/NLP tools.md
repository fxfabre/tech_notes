# NLP tools

## Platform overview :

- Snowflake Cortex : ready to use Serverless AI, LLM & Search functions
    - Document AI
    - Universal Search : SQL functions to use LLM models
    - Snowflake copilot : to generate SQL from a simple sentense
    - Streamlit : deploy an ML app in minutes
- Snowpark container services :
Custom LLM, fine tuned models or LLM partners

## Cortex LLM functions :

- Summarize
`SELECT SNOWFLAKE.CORTEX.SUMMARIZE(content) FROM table_name;`
- Sentiment
`SELECT SNOWFLAKE.CORTEX.SENTIMENT(content) FROM table_name;`
- Translate
`SELECT SNOWFLAKE.CORTEX.TRANSLATE(content, 'fr', 'en') FROM table_name;`
- Answer a question on a document
`SELECT SNOWFLAKE.CORTEX.EXTRACT_ANSWER(content, 'question here') FROM table_name;`
- Answer question without context :
    
    ```sql
    # Version 1 : Answer 1 question per line :
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-7b',
        CONCAT('Tell me why this food is tasty: ', menu_item_name)
    ) FROM FROSTBYTE_TASTY_BYTES.RAW_POS.MENU LIMIT 5;
    
    # Version 2 : give history, context & options
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-7b',
        [
            {'role': 'system', # background information and instructions for response style
            'content': 'Analyze this Snowflake review and determine the overall sentiment. Answer with just \"Positive\", \"Negative\", or \"Neutral\"' },
            {'role': 'user',   # User response to previous prompt
            'content': 'I love Snowflake because it is so simple to use.'},
            {'role': 'assistant', # A response previously provided by the LLM
            'content': 'Positive. The review expresses a positive sentiment towards Snowflake, specifically mentioning that it is \"so simple to use.\'"'},
            {'role': 'user',   # New prompt
            'content': 'Based on other information you know about Snowflake, explain why the reviewer might feel they way they do.'}
        ], -- the array with the prompt history, and your new prompt
        {} -- An empty object of options (we're not specify additional options here)
    ) AS response;
    ```
    

## Snowflake Cortex ML functions

- Time series forecast :
    
    ```sql
    CREATE SNOWFLAKE.ML.FORECAST model_name(
      INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'vue_name'),
      TIMESTAMP_COLNAME => 'date',
      TARGET_COLNAME => 'sales'
    );
    call model_name!FORECAST(FORECASTING_PERIODS => 3);
    ```
    
- Anomaly detection, identify outliers
- Top insights : identify changes for metrics across time intervals
- Classification

## Snowpark ML Modeling

Run python code (including scikit-learn models) in parallel on Snowflake servers → distributed training

## Snowflake model Registry

Helps with model management : track model version & metadata

```python
registry.log_model(
    sklearn_model,
    model_name="...",
    version_name="v1",
    sample_input_data=X,
    options={"method_options": {"..."}}
)
```

## Snowflake feature store

Help create, store, manage and serve ML features used to train a model

## Streamlit

Easily create a web app

Turn data & ml models into an interactive web app without any front end dev.

Share streamlit app via url using RBAC

## Snowpark container services SPCS

Deploy custom ML models, deploy, manage & scale contenairized workload using snowflake managed infrastructure 

Run any language, on custom CPU & GPU
