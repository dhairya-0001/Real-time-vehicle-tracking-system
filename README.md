# EdgeDrive Vision – Real-Time Vehicle Detection System

EdgeDrive Vision is a lightweight, CPU-optimized automotive computer vision system designed to detect vehicles (Cars, Trucks, Buses, Motorcycles) in real-time. It runs efficiently on low-end hardware without requiring a GPU.

## 🎯 Features

- **Real-Time Detection**: Detects multiple vehicle classes using YOLOv8n.
- **CPU Optimized**: Runs smoothly on non-GPU systems with frame skipping and resizing.
- **Web Interface**: Clean, dark-themed dashboard to view live feed and stats.
- **Video Upload**: Support for processing uploaded video files.
- **Adjustable Settings**: Configurable confidence threshold and performance modes.

## 🏗️ System Architecture

- **AI Engine**: PyTorch + YOLOv8n (Ultralytics)
- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Tailwind CSS)
- **Processing**: OpenCV for frame manipulation

## 📂 Folder Structure

```
project/
├── train.py          # Training template
├── model.py          # YOLOv8n model wrapper
├── inference.py      # Core detection logic
├── utils.py          # Helper functions
├── config.yaml       # Configuration settings
├── requirements.txt  # Project dependencies
├── backend/
│   ├── main.py       # FastAPI app entry point
│   └── routes.py     # API routes
├── frontend/
│   ├── templates/    # HTML templates
│   └── static/       # CSS/JS assets
├── uploads/          # Uploaded videos
└── outputs/          # Processed outputs
```

## 🚀 Installation & Setup

1.  **Clone the repository** (or navigate to the project directory).
2.  **Install dependencies**:
    ```bash
    pip install -r project/requirements.txt
    ```
    *Note: If you have issues installing `ultralytics` or `torch`, ensure you have a compatible Python version (3.8+).*

## ⚡ How to Run

1.  **Navigate to the project root**:
    ```bash
    cd "c:/Projects/Real time vehicle tracking system"
    ```

2.  **Start the server**:
    ```bash
    uvicorn project.backend.main:app --reload
    ```

3.  **Access the Dashboard**:
    Open your browser and go to: `http://127.0.0.1:8000`

## ⚙️ Configuration

Edit `project/config.yaml` to adjust settings:

-   `confidence_threshold`: Minimum confidence for detection (default: 0.4).
-   `frame_width` / `frame_height`: Resolution for inference (default: 640x480).
-   `frame_skip`: Process every Nth frame to save CPU (default: 2).

## 📊 Performance Notes

-   **CPU Usage**: Optimized by resizing frames and skipping inference on alternating frames.
-   **Model**: Uses `yolov8n.pt` (nano) for fastest inference speed.

## 📜 License

This project is for educational and portfolio purposes.
