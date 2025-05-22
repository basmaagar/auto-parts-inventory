import sys
try:
    import weasyprint
    print("WeasyPrint is installed and importable.")
except ImportError:
    print("WeasyPrint is NOT installed or not importable.")
print("Python executable:", sys.executable)
print("Python version:", sys.version)
