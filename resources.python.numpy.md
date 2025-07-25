---
id: kut2sklpl6vjnwa6lk9g8fe
title: Numpy
desc: ''
updated: 1753449708307
created: 1753449699543
---
tags: [master, numpy, python, arrays, scientific-computing]

# master.numpy

## 📌 Topic Overview

**NumPy** (Numerical Python) is the backbone of scientific computing in Python. It's a lightning-fast library for working with large **multidimensional arrays** and performing **vectorized operations**.

It's not just faster than regular Python loops — it's a whole new paradigm. If you're still using lists to do math, you're bringing a knife to a gunfight.

> ⚡ Core of most ML/DS workflows  
> 🧠 Powers pandas, TensorFlow, SciPy  
> 🧮 Enables fast numerical computation at scale  

---

## 🚀 80/20 Roadmap

| Stage | Concept                       | Why It Matters                                           |
|-------|-------------------------------|----------------------------------------------------------|
| 1️⃣    | ndarray creation              | The building block of all operations                     |
| 2️⃣    | Array indexing/slicing        | Crucial for data access, reshaping, selection            |
| 3️⃣    | Vectorized math ops           | Avoid for-loops, use array-level operations              |
| 4️⃣    | Broadcasting                  | The secret sauce behind implicit expansion               |
| 5️⃣    | Shape manipulation            | `.reshape`, `.ravel`, `.transpose`, `.axis` awareness    |
| 6️⃣    | Boolean filtering & masking   | Essential for conditional logic on data                  |
| 7️⃣    | Aggregations & reductions     | `.sum()`, `.mean()`, `.argmax()` etc.                    |
| 8️⃣    | Random number generation      | Monte Carlo, sampling, simulation                        |
| 9️⃣    | Linear algebra basics         | Matrix multiplication, inverse, dot product              |
| 🔟     | Performance tricks            | Memory layout, `astype()`, `np.vectorize`, views         |

---

## 🛠️ Practical Tasks

- ✅ Create arrays from lists, ranges, and random values  
- ✅ Index, slice, and reshape arrays  
- ✅ Perform arithmetic operations without loops  
- ✅ Apply conditionals and masking  
- ✅ Compute stats: mean, std, min/max per axis  
- ✅ Generate reproducible random numbers  
- ✅ Multiply matrices, solve systems of equations  
- ✅ Stack and concatenate arrays  
- ✅ Use NumPy for fast rolling window ops  
- ✅ Profile NumPy operations using `%timeit`

---

## 🧾 Cheat Sheets

### 📚 Creating Arrays

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.zeros((2, 3))
c = np.ones((3, 3)) * 7
d = np.arange(0, 10, 2)
e = np.linspace(0, 1, 5)
f = np.random.rand(3, 2)
````

### 🎯 Indexing & Slicing

```python
a = np.array([[1,2,3],[4,5,6]])
a[0,1]        # 2
a[:,1]        # column 1
a[1,:2]       # [4, 5]
```

### 💪 Vectorized Ops

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
a + b          # [5 7 9]
a * 2          # [2 4 6]
np.sqrt(a)     # [1. 1.41 1.73]
```

### 🧠 Broadcasting

```python
a = np.array([[1], [2], [3]])  # shape (3,1)
b = np.array([10, 20, 30])     # shape (3,)
a + b                          # shape (3,3) — auto-expanded
```

### 🔬 Boolean Filtering

```python
x = np.array([1, 2, 3, 4])
x[x % 2 == 0]  # [2, 4]
```

### 🧮 Aggregations

```python
x = np.array([[1, 2], [3, 4]])
x.sum()               # 10
x.mean(axis=0)        # [2, 3]
x.max(axis=1)         # [2, 4]
```

### 🎲 Random Generation

```python
np.random.seed(42)
np.random.randint(0, 100, size=(3, 3))
np.random.normal(0, 1, 1000)
```

### 🧱 Matrix Ops

```python
A = np.array([[1,2], [3,4]])
B = np.array([[2,0], [1,2]])
np.dot(A, B)
np.linalg.inv(A)
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                         |
| --------------- | ----------------------------------------------------------------- |
| 🥉 Beginner     | Create and reshape a 2D array, compute row/column-wise mean       |
| 🥈 Intermediate | Mask values > 50 in a random array and count how many remain      |
| 🥇 Advanced     | Implement matrix multiplication manually using broadcasting       |
| 🏆 Expert       | Build a Monte Carlo simulation using only NumPy (no Pandas/Loops) |

---

## 🎙️ Interview Q\&A

* **Q:** What is broadcasting in NumPy? Give an example.
* **Q:** How is NumPy faster than native Python lists?
* **Q:** What’s the difference between `.copy()` and `.view()`?
* **Q:** Why would you use `np.where()`?
* **Q:** How would you calculate the correlation matrix using NumPy only?

---

## 🛣️ Next Tech Stack Recommendations

* **Pandas** — Built on NumPy for labeled tabular data
* **SciPy** — Scientific computing (stats, optimization, FFT)
* **Numba** — Just-in-time compiler for blazing fast custom loops
* **CuPy** — GPU-powered NumPy for deep compute tasks
* **TensorFlow / PyTorch** — If you're jumping into deep learning

---

## 🧠 Pro Tips

* Prefer `.astype()` for type conversions (e.g., float32 → float64)
* Use `np.where()` for vectorized conditional logic
* Avoid Python for-loops — prefer `np.dot()`, `np.sum()` etc.
* Watch out for **mutable shared memory** in views
* Use `%timeit` in Jupyter to profile your code efficiently

---

## 🧬 Tactical Philosophy

> “NumPy is the grammar of fast numerical thinking in Python.”

🛠 Write once, vectorize forever
🚀 Embrace broadcasting — it’s magic with rules
🔬 Think in shapes, not just values
🧱 If you're not reshaping, you're probably copying too much

---
