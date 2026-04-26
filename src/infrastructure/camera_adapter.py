import cv2

from src.application.services.logging_service import LoggingService

class CameraAdapter:
    def __init__(self, logging_service: LoggingService):
        self.cap = cv2.VideoCapture(0)
        self.logging_service = logging_service

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Error: Can't receive frame. Exiting...")
        return frame
    
    def show_image(self, window_name: str, frame) -> int:
        cv2.imshow(window_name, frame)
        # Needed for window refresh + keyboard events.
        return cv2.waitKey(1) & 0xFF