# 11. Schema Evolution
Very realistic.
Example:
Today:
```json
{
 "customer_id": 1,
 "name": "Ronak"
}
```
Tomorrow:
```json
{
 "customer_id": 1,
 "name": "Ronak",
 "email": "x@y.com"
}
```
What breaks?
What doesn't?
How do you manage it?