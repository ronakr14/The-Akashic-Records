# AI Summary
None. Three different approaches to **concurrency / parallelism** with different trade-offs:

```table-of-contents
```

Three different approaches to **concurrency / parallelism** with different trade-offs:

1. **Async (async/await)** = best for _many_ I/O-bound tasks with low CPU usage (network, disk). Single thread, tiny memory footprint, high throughput, lower latency handling thousands+ connections.
2. **Multithread** = good for _I/O-bound_ work when you want simpler synchronous-style code or need blocking libs; in CPython threads are _concurrent_ but not truly parallel for Python bytecode because of the GIL.
3. **Multiprocess** = use when you need _true parallelism_ for CPU-bound work — each process has its own Python interpreter and memory; heavier but runs on multiple CPU cores.

---

## Quick Rules of Thumb

- If your problem is **waiting on network/db/files** → use **async** or **threads**.
- If your problem is **heavy CPU work** (ML, big loops, compression) → use **multiprocess**.
- If you need **shared memory and low complexity**, threads are easier but beware of GIL and race conditions.
- If you need **isolation, robustness, parallel CPU**, use processes (or native C extensions, or move heavy work to GPU/worker service).

---

## Practical Pros/Cons

### Async

- Pros: low memory, high concurrency, explicit flow control, predictable scheduling.
- Cons: needs async-aware libraries, callback-style mental model, debugging & stack traces can be trickier.

### Threads

- Pros: easy to reuse sync libraries, simpler code for blocking libs, shared memory (no serialization).
- Cons: GIL in CPython limits CPU parallelism; locking/race conditions; context-switch overhead.

### Processes

- Pros: true parallelism, isolation (crash one process, others survive).
- Cons: higher memory/IPC cost, serialization overhead, more complex orchestration.

---

## Python Examples

### Async (I/O-bound)

```python
import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as r:
            return await r.text()

async def main(urls):
    tasks = [asyncio.create_task(fetch(u)) for u in urls]
    return await asyncio.gather(*tasks)
```

### Threads (easier with blocking libs)

```python
from concurrent.futures import ThreadPoolExecutor
import requests

def fetch(url):
    return requests.get(url).text

with ThreadPoolExecutor(max_workers=20) as ex:
    results = list(ex.map(fetch, urls))
```

### Processes (CPU-bound)

```python
from concurrent.futures import ProcessPoolExecutor

def heavy(x):
    return sum(i*i for i in range(10_000_000))

with ProcessPoolExecutor() as ex:
    results = list(ex.map(heavy, inputs))
```

---

## Performance Considerations & Pitfalls

- **GIL**: CPython only allows one thread executing Python bytecode at a time — threads help with I/O but not CPU.
- **Memory**: processes duplicate memory (copy-on-write helps initially). Threads share memory — less memory but need locks.
- **Latency vs Throughput**: async often gives best throughput for many connections; threads/processes can reduce per-task latency if blocking libs dominate.
- **Debugging & Observability**: async stack traces and race conditions can be hard to debug; processes are easier to isolate and attach profilers to.

---

## Decision Flow

1. Need to handle thousands of concurrent network connections → **async**.
2. Using synchronous libraries that block and you don't want to refactor → **threads**.
3. Doing CPU-heavy tasks across multiple cores → **processes** (or move to C/NumPy/GPU).
4. Need isolation and fault-tolerance → **processes / separate services**.

---

## See Also

- [[python]]
- [[python — Files & Serialization]]
- [[python — Modules & Packages]]
- [[python — OOP & Classes]]
