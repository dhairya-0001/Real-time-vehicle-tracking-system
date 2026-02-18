from ultralytics import YOLO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_model():
    """
    Template for training/fine-tuning the YOLOv8n model.
    """
    # Load a model
    model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)

    # Train the model
    # data='coco128.yaml' is a placeholder. Replace with your custom dataset YAML.
    # epochs=100 is a standard starting point.
    # imgsz=640 is standard.
    try:
        logger.info("Starting training...")
        results = model.train(data='coco128.yaml', epochs=3, imgsz=640, device='cpu')
        logger.info("Training completed successfully.")
        
        # Save the model
        model.export(format='torchscript')
        logger.info("Model exported.")
        
    except Exception as e:
        logger.error(f"An error occurred during training: {e}")

if __name__ == '__main__':
    # This is a template. Check requirements and dataset before running.
    print("This is a training template. Please configure your dataset before running.")
    # train_model()
