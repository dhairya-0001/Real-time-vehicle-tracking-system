import cv2
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_logging():
    """Returns the logger instance."""
    return logger

def draw_bounding_boxes(frame, detections, class_names):
    """
    Draws bounding boxes and labels on the frame.
    detections: list of [x1, y1, x2, y2, conf, cls]
    class_names: dict mapping class_id to class_name
    """
    for x1, y1, x2, y2, conf, cls in detections:
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        label = f"{class_names.get(int(cls), 'Unknown')} {conf:.2f}"
        
        # Draw rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        
        # Draw label background
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(frame, (x1, y1 - 20), (x1 + w, y1), (0, 255, 255), -1)
        
        # Draw text
        cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    return frame

class FPSCounter:
    def __init__(self):
        self.prev_time = time.time()
        self.fps = 0

    def update(self):
        current_time = time.time()
        self.fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        return self.fps

def resize_frame(frame, width=640, height=480):
    """Resizes the frame to the specified dimensions."""
    return cv2.resize(frame, (width, height))
