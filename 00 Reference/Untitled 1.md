# Ensure both project root (for `src.*`) and backend/ (for `routers.*`) are importable

print(sys.path)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

_BACKEND_DIR = Path(__file__).resolve().parent

for p in (str(_PROJECT_ROOT), str(_BACKEND_DIR)):

    if p not in sys.path:

        sys.path.insert(0, p)