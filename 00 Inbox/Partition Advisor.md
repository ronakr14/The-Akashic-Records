Input:

```
Query history
```

Agent computes:

```
Filter frequencyCardinalitySkewScan percentage
```

Example:

```
Table:salesQueries:WHERE region70%WHERE order_date20%WHERE customer_id10%
```

Agent recommends:

```
Partition:regionZORDER:order_date
```

with reasoning.