# Some notes about Elastic Search

## Elastic stack
Open source elastic stack :
- logstash : Data loading + transform. Resource intensive. chargement de logs, ETL platform
- beats : lightweight way of getting data into ELK. Filebeats, Packetbeats ... -> lightweight, single purpose tools.
- ES : Holds all of the data. Indexing + distribute data on the nodes
- Kibana : Web frontend : search, viz, dashboards

Addons :
- For security, alerting, monitoring, reporting, graph


## Bulk API
Sample file :
1 line of metadata + 1 line of data
```json
{ "index" : {"_index":  "my_index", "_type": "data_type", "_id": 1 }}
{ "field_name": "value" }
{ "index" : {"_index":  "my_index", "_type": "data_type", "_id": 2 }}
{ "field_name": "value2" }
```

- Endpoint : `/_bulk`
- Import file : `curl -s -H "Content-Type: application/s-ndjson" -XPOST host:9200/_bulk` --data-binary "@file_path"`
- `GET /my_index/data_type/1`
- `GET _cat/indices` : display indexes


Data types :
- Core
- Complex : arrays
- Geo
- Specialized : IP, ...


## Search queries
Common query patern
```
GET index/data_type/_search
{ "query" : { $query_content } }
```

Sample query content :
- match query for text field : `"match": { "field_name": "value" }`
- term query for keywords and numeric values : `"term": { "field": 42 }`
- terms query : `"terms": { "field": [42, 56] }`

````json
GET index_name/_search
{
  "query": {
    "match_all": {}
  }
}
````

```
"bool": { "must": [
    {"match": {"field1": "value"}},
    {"match": {"field2": "value"}}
] }
```

```
"bool": { "should": [
    {"match": {"field1": "value"}},
    {"match": {"field2": {"query: "value", "boost": 3}}}
] }
```

```
"range": { "field_name": {
        "gte": 42, 
        "lt" : 78,
        "boost": 3 
} }
```


## Analyze queries
Tokenizers :
- standard : with default settings
- letter : keep only alphanum chars, removing dots
- uax_url_email : NER on email + url

```
GET index/_analyze  # output a list of tokens
{
    "tokenizer": "standard",
    "text": "The Moon is made of Cheese some Say"
}
```

Custom analyzer by field :
```
PUT /my_index
{
    "mappings": { "type1": { "properties": {
        "field_name_1": {
            "type": "text",
            "analyzer": "standard"
        },
        "field_name_2": {
            "type": "text",
            "analyzer": "english"
        }
} } } }
```

```
GET my_index/_analyze   # use the standard tokenizer
{
    "field": "field_name_1",
    "text": "Bears"
}

GET my_index/_analyze   # use the english tokenizer
{
    "field": "field_name_2",
    "text": "Bears"
}
```


## Aggregations
It is possible to run nested groupby :
- Groupby `string_field_1` then by `float_field_2`.
- Need to call `.keyword` on `string_field_1` because of type string.
```
GET index/data_type/_search
{
    "size": 0,
    "aggs": {
        "target_field_name": {
            "terms" : { "field": "string_field_1.keyword" }
        },
        "aggs": {
            "target_field_name": { "avg": { "field": "float_field_2" } }
} } }
```

Groupby + filter :
```
GET index/data_type/_search
{
    "size": 0,
    "query": {
        "match": { "field_name.keyword": "filter_value" }
    },
    "aggs": {
        "target_field_name": {
            "terms" : { "field": "string_field_1.keyword" }
} } }
```

Some operations :
- avg : https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-avg-aggregation.html
- geo : https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geobounds-aggregation.html
- matrix_stats : https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-matrix-stats-aggregation.html
- percentile_ranks : https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-rank-aggregation.html
- percentiles : https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-percentile-aggregation.html
- string_stats : https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-string-stats-aggregation.html


#### Create index to store BERT vectors :
`````python
async def clear_cache() -> Dict[str, str]:
    INDEX_CONTENT = {
        "settings": {
            "number_of_shards": 2,
            "number_of_replicas": 1
        },
        "mappings": {
            "dynamic": "true",
            "_source": {"enabled": "true"},
            "properties": {
                "title": {"type": "text"},
                "language": {"type": "text"},
                "bert_vector": {"type": "dense_vector", "dims": 768},
            }
        }
    }

    print("Creating the 'posts' index.")
    elastic.indices.delete(index=INDEX_NAME, ignore=[404])
    elastic.indices.create(index=INDEX_NAME, body=INDEX_CONTENT)
    return {"status": "success"}
`````

#### Bulk insert BERT embeddings to Elastic
`````python
from elasticsearch.helpers import bulk

def insert_in_elastic(texts: Iterable[str]):
    for start in range(0, len(texts), BATCH_SIZE):
        end = min(len(texts), start + BATCH_SIZE)
        batch = texts[start: end]

        bert_vectors = get_bert_embeddings(batch)
        requests = [
            {
                "_op_type": "index",
                "_index": INDEX_NAME,
                "title": name,
                "bert_vector": bert_vector
            }
            for name, bert_vector in zip(batch, bert_vectors)
        ]
        bulk(elastic, requests)
`````