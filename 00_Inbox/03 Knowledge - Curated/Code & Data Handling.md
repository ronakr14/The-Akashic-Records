```table-of-contents
```
# 🧭 When to Use **Functions**
1. Logic is **pure or mostly pure** (input → output).
2. You can unit-test it without mocks.
3. It does **one thing well**.
4. You expect to reuse it across contexts. 
5. ⚠️ Watch out if:
	1. You’re passing the _same argument bundle_ everywhere → introduce a dataclass.
	2. You’re simulating state with globals → stop and redesign.

# 🧭 When to Use **Modules**
1. Functions are **conceptually related** and deserve a namespace.
2. You’re grouping helpers, constants, or adapters.
3. You’d otherwise create a “static-only class” (anti-pattern). 
4. ⚠️ Watch out if:
	1. You need per-instance configuration or lifecycle → you need a class.

# 🧭 When to Use Dataclasses
1. The object primarily **represents data**, not behavior.
2. It’s a DTO, config object, schema, or event.
3. You want **type safety, immutability, and readability**.
4. Equality, hashing, or freezing matters. Allowed methods:
5. validation
6. derived properties
7. formatting helpers 
8. ⚠️ Watch out if:
	1. Methods start coordinating workflows or calling external systems.
	2. You’re injecting dependencies → that’s a class now.

# 🧭 When to Use **Dictionaries**
1. Data is **untrusted, external, or schema-less** (API payloads, JSON, YAML).
2. You’re at the **edges of the system** (I/O boundaries).
3. Flexibility > safety. 
4. ⚠️ Watch out if:
	1. Dicts leak into core logic.
	2. You’re doing deep key access everywhere.
	3. Bugs are “key not found” instead of compile-time errors.

# 🧭 When to Use **Classes**
1. State must persist across operations.
2. Behavior depends on history or lifecycle.
3. You need polymorphism (strategies, plugins).
4. Frameworks require them (ORMs, operators, DI). 
5. ⚠️ Watch out if:
	1. It’s just a namespaced bag of functions.
	2. `__init__` feels like a config parser.
	3. The class violates single responsibility.
