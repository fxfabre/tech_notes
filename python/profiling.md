# Profiling & perf tools

## Links :
- https://toucantoco.com/en/tech-blog/tech/python-performance-optimization
- https://wiki.python.org/moin/PythonSpeed/PerformanceTips#Visualizing_Profiling_Results

## Eval time spent
```
import timeit
timeit.timeit(
   'pd.DataFrame(list(db.collection_name.find()))', 
   setup="import pandas as pd; from pymongo import MongoClient; client = MongoClient(HOST, PORT); db = client.db_name",
   number=500
)
29.600714206695557
```

## Quick run :
Generate the `output.pstats` file with any method :
- python -m profile -o output.pstats path/to/your/script arg1 arg2
- or use Pycharm pro, to run the python profiler (same as above)

Visualize in a web browser :
- snakeviz output.pstats

## External tools :
Yappi : Yet Another Python Profiler, but this time support Multithread/CPU time profiling
- pip install yappi


## Load test tool : siege
- https://www.tecmint.com/load-testing-web-servers-with-siege-benchmarking-tool/
- https://k6.io/blog/load-testing-with-postman-collections/
- sudo apt-get install siege
- siege --concurrent=10 --time=5M --delay=1 localhost/endpoint:1234

## Load test tool : locust
