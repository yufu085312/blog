import sys
import os
print(f"Python version: {sys.version}")
print(f"Executable: {sys.executable}")
print(f"Path: {sys.path}")
print(f"Current dir: {os.getcwd()}")
try:
    import google
    print("google module found")
except ImportError:
    print("google module NOT found")
