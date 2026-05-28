# Threading

Best use case:  
Concurrent I/O-bound tasks (network calls, file ops) to improve throughput without multiprocessing overhead.

Alternative: — [[Asyncio]] when you need scalable async concurrency with better control over event loops and high-load systems
