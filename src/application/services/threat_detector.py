import threading
import time
from pathlib import Path
from urllib.request import urlretrieve

import cv2
from ultralytics import YOLO

from src.application.services.logging_service import LoggingService
from src.infrastructure.camera_adapter import CameraAdapter
from src.infrastructure.redis_adapter import RedisAdapter

class ThreatDetector:
    def __init__(
        self, 
        camera_adapter: CameraAdapter,
        redis_adapter: RedisAdapter,
        logging_service: LoggingService,
        confidence_threshold: float = 0.60,
        threat_labels: tuple[str, ...] = ("Knife", "gun"),
        model_path: str = "weights/weapon-detection-yolov8n-v2-best.pt",
        imgsz: int = 960,
    ) -> None:
        self._camera_adapter = camera_adapter
        self._redis_adapter = redis_adapter
        self._logging_service = logging_service
        self._is_active = True
        self._frame = None
        self._lock = threading.Lock()
        self._confidence_threshold = confidence_threshold
        self._threat_labels = {str(x).strip().lower() for x in threat_labels}
        model_local_path = Path(model_path)
        if not model_local_path.exists():
            model_local_path.parent.mkdir(parents=True, exist_ok=True)
            url = (
                "https://huggingface.co/SyncRobotic/weapon-detection-yolov8n-v2"
                "/resolve/main/weights/best.pt"
            )
            self._logging_service.info(f"Downloading weapon model to {model_local_path} ...")
            urlretrieve(url, model_local_path)
            self._logging_service.info("Download complete.")

        self._model = YOLO(str(model_local_path))
        self._imgsz = imgsz
    
    def handle_stop(self):
        self._is_active = False

    def handle_threat_detection(self):
        self._logging_service.info("Threat detected")
        self._redis_adapter.publish(
            channel="threat",
            message="knife threat was detected"
        )

    def is_threat(self, frame) -> bool:
        results = self._model(frame, verbose=False, imgsz=self._imgsz, conf=self._confidence_threshold)

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = str(self._model.names[cls_id]).strip().lower()
                self._logging_service.info(label)
                confidence = float(box.conf[0])
                if label in self._threat_labels and confidence >= self._confidence_threshold:
                    return True

        return False

    def _camera_loop(self):
        while self._is_active:
            frame = self._camera_adapter.get_frame()

            with self._lock:
                self._frame = frame

    def _detection_loop(self):
        while self._is_active:
            if self._frame is None:
                time.sleep(0.01)
                continue

            with self._lock:
                frame = self._frame.copy()
            
            if self.is_threat(frame):
                self.handle_threat_detection()

            time.sleep(0.05)

    def start_loop(self):
        threading.Thread(target=self._camera_loop, daemon=True).start()
        threading.Thread(target=self._detection_loop, daemon=True).start()

        while self._is_active:
            if self._frame is None:
                time.sleep(0.01)
                continue

            with self._lock:
                frame = self._frame.copy()

            key = self._camera_adapter.show_image(
                window_name="Camera Window",
                frame=frame,
            )
            # Quit/stop keys (when the OpenCV window is focused).
            if key in (ord("0"), ord("q")):
                self.handle_stop()
                cv2.destroyAllWindows()