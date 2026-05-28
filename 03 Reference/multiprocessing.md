# MultiProcessing

Best use case:  
CPU-bound parallelism—run compute-heavy tasks across cores (data processing, simulations) bypassing Python’s GIL.

Alternative: — Concurrent.futures when you want simpler API (ProcessPoolExecutor) with less boilerplate for parallel execution
