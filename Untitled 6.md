Let me build you an interactive PySpark fundamentals reference — something you can actually navigate and explore rather than read linearly.Eight sections covering the full fundamentals surface area — navigate using the left panel. A few things worth calling out given your background:

**Architecture tab first** — the Driver/Executor/Py4J model is where most performance intuition comes from. PySpark UDFs crossing the JVM→Python boundary is the #1 hidden perf sink.

**DataFrame over RDD** unless you're handling truly unstructured data or need fine-grained partition control. The Catalyst optimizer + Tungsten give you JVM-native execution that Python UDFs can't match.

**Gotchas tab** is worth a pass — the lazy evaluation trap in particular bites teams that come from Pandas where everything evaluates eagerly.

A few things that are especially relevant given production pipeline work:

- `inferSchema=True` reads the file twice — always define schemas explicitly in prod jobs
- `spark.sql.shuffle.partitions` defaults to 200 which is absurdly high for small jobs and too low for big ones — tune it per-job
- AQE (Adaptive Query Execution, Spark 3.x) handles a lot of the shuffle partition and skew problems automatically; make sure it's on

What do you want to go deeper on — window functions, Streaming, Snowflake connector specifics, or testing patterns?