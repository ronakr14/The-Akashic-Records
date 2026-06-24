---
type: concept
---

```table-of-contents
```

### 🔹 Example 1: Basic Breakpoint Debugging ([[python]])

1. Create a Python file `main.py`:

   ```python
   def add_numbers(a, b):
       return a + b

   def main():
       x = 5
       y = "10"   # 👈 bug: string instead of int
       result = add_numbers(x, y)
       print("Result:", result)

   if __name__ == "__main__":
       main()
   ```

2. In VS Code:

   * Open `main.py`
   * Click in the **gutter** (left of line numbers) next to `result = add_numbers(x, y)` → sets a **breakpoint** (red dot).
   * Hit **F5** (Run → Start Debugging).
   * Execution will stop at the breakpoint, letting you inspect variables in the **Variables panel**.

---

### 🔹 Example 2: Conditional Breakpoint

Let’s say you’re looping and only want to pause when a certain condition is true.

```python
for i in range(10):
    print("Loop:", i)
```

* Set a breakpoint on `print("Loop:", i)`.
* Right-click the red dot → **Edit Breakpoint** → enter `i == 5`.
* Debug → it will only stop when `i` equals 5.

---

### 🔹 Example 3: Logpoints (no `print()` clutter)

Instead of editing your code, you can add runtime logs.

```python
names = ["Ronak", "Alex", "Sam"]
for n in names:
    print("Processing", n)
```

* Set a **logpoint** (Shift+Click in gutter instead of normal click).
* Enter:

  ```
  Current name = {n}
  ```
* When debugging, VS Code will log this in the debug console **without changing your code**.

---

### 🔹 Example 4: Launch Config (`.vscode/launch.json`)

Sometimes you want custom run/debug configs (e.g., run a script with args).

1. In VS Code → Run & Debug → **create a launch.json**.
2. Add:

   ```json
   {
     "version": "0.2.0",
     "configurations": [
       {
         "name": "Debug with args",
         "type": "python",
         "request": "launch",
         "program": "${file}",
         "args": ["--mode", "test"]
       }
     ]
   }
   ```
3. Now when you debug, it will run `python main.py --mode test`.

---

### 🔹 Example 5: Attach to Running Process

If you already have a Python script running:

1. Run with debug flag:

   ```bash
   python -m debugpy --listen 5678 --wait-for-client main.py
   ```
2. In VS Code → Run → Attach to Python, with:

   ```json
   {
     "name": "Attach",
     "type": "python",
     "request": "attach",
     "connect": { "host": "localhost", "port": 5678 }
   }
   ```
3. Start debugging → VS Code will attach to the live process.
