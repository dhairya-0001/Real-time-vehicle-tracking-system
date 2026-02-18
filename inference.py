import cv2
import time
from project.model import VehicleDetector
from project.utils import draw_bounding_boxes, FPSCounter, resize_frame, setup_logging
import yaml

logger = setup_logging()

class InferenceEngine:
    def __init__(self, source=0, config_path='config.yaml'):
        self.detector = VehicleDetector(config_path=config_path)
        self.source = source
        self.config = self.detector.config
        self.frame_width = self.config.get('frame_width', 640)
        self.frame_height = self.config.get('frame_height', 480)
        self.frame_skip = self.config.get('frame_skip', 2)
        self.class_names = self.detector.class_names

    def run(self):
        """
        Generator function that yields processed frames and stats.
        Useful for streaming to the frontend.
        """
        cap = cv2.VideoCapture(self.source)
        
        if not cap.isOpened():
            logger.error(f"Could not open video source: {self.source}")
            return

        fps_counter = FPSCounter()
        frame_count = 0
        
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = resize_frame(frame, width=self.frame_width, height=self.frame_height)
            
            # Frame skipping logic
            if frame_count % self.frame_skip == 0:
                detections = self.detector.detect(frame)
            
            # Draw results (persist detections from previous frame if skipped? 
            # For simplicity, we only draw on processed frames, or we'd need to cache detections)
            # To avoid flickering, we should ideally simply not update detections but still draw them.
            # But here, we'll just draw the fresh detections and for skipped frames, 
            # we might return the raw frame or the last processed frame.
            # A common simple optimization is to just not run detection but still output the frame.
            # If we want visual persistence, we need to cache `detections`.
            
            # Let's cache detections for smoother output
            if frame_count % self.frame_skip == 0:
                self.last_detections = detections
            else:
                detections = getattr(self, 'last_detections', [])

            processed_frame = draw_bounding_boxes(frame, detections, self.class_names)
            
            fps = fps_counter.update()
            
            # Overlay FPS
            cv2.putText(processed_frame, f"FPS: {fps:.1f}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Yield frame (encoded) and stats
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()
            
            # Calculate stats
            vehicle_count = len(detections)
            class_counts = {}
            for *_, _, cls in detections:
                class_name = self.class_names.get(int(cls), 'Unknown')
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
            
            yield frame_bytes, {'fps': fps, 'total': vehicle_count, 'counts': class_counts}

            frame_count += 1

        cap.release()
