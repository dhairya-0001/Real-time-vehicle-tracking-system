from fastapi import APIRouter, Request, File, UploadFile, BackgroundTasks
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import sys
import os
import shutil
from project.inference import InferenceEngine
from project.utils import setup_logging

logger = setup_logging()

router = APIRouter()

# Fix paths
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(backend_dir)
templates_dir = os.path.join(project_dir, "frontend", "templates")
uploads_dir = os.path.join(project_dir, "uploads")

templates = Jinja2Templates(directory=templates_dir)

# Global variable to store latest stats (simplified for demo)
latest_stats = {"fps": 0, "total": 0, "counts": {}}

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def generate_frames(source=0):
    global latest_stats
    engine = InferenceEngine(source=source)
    for frame_bytes, stats in engine.run():
        latest_stats = stats
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@router.get("/video_feed")
async def video_feed():
    # Default to webcam
    return StreamingResponse(generate_frames(source=0), media_type="multipart/x-mixed-replace; boundary=frame")

@router.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    # Ensure uploads dir exists
    os.makedirs(uploads_dir, exist_ok=True)
    
    file_location = os.path.join(uploads_dir, file.filename)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    # Process uploaded video (simplified: separate endpoint or just return path)
    # For a real app, we might return a stream ID or similar. 
    # Here, we'll just redirect the feed source or similar.
    # Limitation: video_feed is currently hardcoded to webcam 0. 
    # To support upload, we could store the path and use it in a parameterized feed endpoint.
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@router.get("/video_feed_file")
async def video_feed_file(filename: str):
    file_path = os.path.join(uploads_dir, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return StreamingResponse(generate_frames(source=file_path), media_type="multipart/x-mixed-replace; boundary=frame")

@router.get("/stats")
async def get_stats():
    global latest_stats
    return latest_stats

@router.get("/health")
async def health():
    return {"status": "healthy"}
