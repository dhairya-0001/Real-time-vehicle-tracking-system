import uvicorn
import os

if __name__ == "__main__":
    # Ensure we are in the correct directory (project root)
    # This script is expected to be in the root of "Real time vehicle tracking system"
    print("Starting EdgeDrive Vision Server...")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
