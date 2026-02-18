import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Current working directory: {os.getcwd()}")
print(f"System path: {sys.path}")

try:
    import cv2
    print("OpenCV imported successfully.")
except ImportError as e:
    print(f"Error importing OpenCV: {e}")

try:
    import torch
    print(f"Torch imported successfully. Version: {torch.__version__}")
except ImportError as e:
    print(f"Error importing Torch: {e}")

try:
    import ultralytics
    print(f"Ultralytics imported successfully. Version: {ultralytics.__version__}")
except ImportError as e:
    print(f"Error importing Ultralytics: {e}")

try:
    from fastapi import FastAPI
    print("FastAPI imported successfully.")
except ImportError as e:
    print(f"Error importing FastAPI: {e}")

try:
    import uvicorn
    print("Uvicorn imported successfully.")
except ImportError as e:
    print(f"Error importing Uvicorn: {e}")

print("Verification complete.")
