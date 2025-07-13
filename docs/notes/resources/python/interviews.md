# Interviews

## Junior

**Q: What’s the difference between a list and a tuple?**  
A: Lists are mutable, tuples are immutable — use tuples when data shouldn’t change.

**Q: What is PEP8?**  
A: It’s the style guide for Python code — consistency matters in team projects.

## Mid-Level

**Q: How is Python’s memory managed?**  
A: Python uses reference counting with garbage collection via the `gc` module.

**Q: Explain list comprehension with an example.**  
A: `[x for x in range(5) if x % 2 == 0]` creates `[0, 2, 4]`.

**Q: What are decorators?**  
A: Functions that modify behavior of other functions — useful for logging, auth, etc.

## Senior

**Q: How do you manage dependencies across environments?**  
A: Use `venv` or `poetry`, and store packages in `requirements.txt`.

**Q: What’s the GIL, and how does it affect concurrency?**  
A: The Global Interpreter Lock prevents multiple native threads from executing Python bytecodes simultaneously — use multiprocessing for CPU-bound tasks.