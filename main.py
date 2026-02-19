from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Remove sys.path hacking and use package imports
# Ensure you run with: uvicorn project.backend.main:app

from project.backend.routes import router

app = FastAPI(title="EdgeDrive Vision")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
# Use absolute path relative to this file
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(backend_dir)
static_dir = os.path.join(project_dir, "frontend", "static")
templates_dir = os.path.join(project_dir, "frontend", "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates
templates = Jinja2Templates(directory=templates_dir)

# Include routes
app.include_router(router)


