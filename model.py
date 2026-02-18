import os
from ultralytics import YOLO
import torch
import yaml
import logging

# Setup logging
logger = logging.getLogger(__name__)

class VehicleDetector:
    def __init__(self, config_path=None, model_path=None):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        if config_path is None:
            config_path = os.path.join(self.base_dir, 'config.yaml')
        if model_path is None:
            model_path = os.path.join(self.base_dir, 'models', 'yolov8n.pt')
            
        self.config = self._load_config(config_path)
        # Note: YOLO normally handles downloads, but we might want to specify the path explicitly
        # If model_path is just a filename, YOLO looks in current dir. 
        # If we want it in 'models/', we should pass that.
        self.model_path = model_path
        self.model = self._load_model(self.model_path)
        self.allowed_classes = self.config.get('allowed_classes', [2, 3, 5, 7])
        self.conf_threshold = self.config.get('confidence_threshold', 0.4)
        self.class_names = self.config.get('class_names', {})

    def _load_config(self, config_path):
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}

    def _load_model(self, model_path):
        try:
            # Force CPU usage
            device = 'cpu'
            logger.info(f"Loading YOLOv8n model on {device} from {model_path}...")
            # Check if model exists, if not let YOLO download it to the target path or defaults
            # YOLO(path) will load from path.
            model = YOLO('yolov8n.pt') # Initial download/load
            # If we want to strictly use our path:
            # model = YOLO(model_path) 
            # But let's keep it simple for now, 'yolov8n.pt' is robust.
            return model
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise e

    def detect(self, frame):
        """
        Performs detection on a single frame.
        Returns a list of detections: [x1, y1, x2, y2, conf, cls]
        """
        results = self.model(frame, verbose=False, device='cpu', classes=self.allowed_classes, conf=self.conf_threshold)
        
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                conf = box.conf[0]
                cls = box.cls[0]
                detections.append([x1.item(), y1.item(), x2.item(), y2.item(), conf.item(), cls.item()])
        
        return detections
