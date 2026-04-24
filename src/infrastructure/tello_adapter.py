from __future__ import annotations

import time
from typing import Optional

from djitellopy import Tello

from src.application.services.logging_service import LoggingService


class TelloAdapter:
    """Thin adapter around `djitellopy.Tello` to keep the rest of the app clean."""

    def __init__(self, logging_service: LoggingService) -> None:
        self.tello = Tello()
        self.logging_service = logging_service
        self._connect()

    def _connect(self) -> None:
        try:
            self.tello.connect()
        except Exception as err:
            self.logging_service.error("Failed to connect to Tello", err)
            raise

    def get_battery(self) -> int:
        return self.tello.get_battery()

    def stream_on(self) -> bool:
        try:
            self.tello.streamon()
            return True
        except Exception as err:
            self.logging_service.error("Failed to start video stream", err)
            return False

    def stream_off(self) -> bool:
        try:
            self.tello.streamoff()
            return True
        except Exception as err:
            self.logging_service.error("Failed to stop video stream", err)
            return False

    def get_frame_read(self):
        try:
            return self.tello.get_frame_read()
        except Exception as err:
            self.logging_service.error("Failed to read video frame", err)
            raise

    def take_off(self) -> bool:
        try:
            self.tello.takeoff()
            time.sleep(5)
            return True
        except Exception as err:
            self.logging_service.error("Takeoff failed", err)
            return False

    def land(self) -> bool:
        try:
            self.tello.land()
            return True
        except Exception as err:
            self.logging_service.error("Landing failed", err)
            return False

    def move_up(self, distance: int) -> bool:
        try:
            self.tello.move_up(distance)
            return True
        except Exception as err:
            self.logging_service.error(f"Move up failed (distance={distance})", err)
            return False

    def move_down(self, distance: int) -> bool:
        try:
            self.tello.move_down(distance)
            return True
        except Exception as err:
            self.logging_service.error(f"Move down failed (distance={distance})", err)
            return False

    def move_forward(self, distance: int) -> bool:
        try:
            self.tello.move_forward(distance)
            return True
        except Exception as err:
            self.logging_service.error(f"Move forward failed (distance={distance})", err)
            return False

    def move_back(self, distance: int) -> bool:
        try:
            self.tello.move_back(distance)
            return True
        except Exception as err:
            self.logging_service.error(f"Move back failed (distance={distance})", err)
            return False

    def move_left(self, distance: int) -> bool:
        try:
            self.tello.move_left(distance)
            return True
        except Exception as err:
            self.logging_service.error(f"Move left failed (distance={distance})", err)
            return False
    
    def move_right(self, distance: int) -> bool:
        try:
            self.tello.move_right(distance)
            return True
        except Exception as err:
            self.logging_service.error(f"Move right failed (distance={distance})", err)
            return False

    def rotate_right(self, degrees: int) -> bool:
        try:
            self.tello.rotate_clockwise(degrees)
            return True
        except Exception as err:
            self.logging_service.error(f"Rotate right failed (degrees={degrees})", err)
            return False

    def rotate_left(self, degrees: int) -> bool:
        try:
            self.tello.rotate_counter_clockwise(degrees)
            return True
        except Exception as err:
            self.logging_service.error(f"Rotate left failed (degrees={degrees})", err)
            return False