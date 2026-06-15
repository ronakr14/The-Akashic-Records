Analyze:

```
Join typeBroadcast usageShuffle sizeSkew
```

Example:

```
orders2 GBcustomers10 MB
```

Current:

```
SELECT *FROM orders oJOIN customers c
```

Agent:

```
Broadcast join possible.Current shuffle:2.1 GBExpected shuffle:10 MB
```

Estimated runtime reduction:

```
45%
```