from __future__ import annotations
import threading

from queue import Queue
import time
from typing import Optional, Tuple

import cv2

from src.infrastructure.tello_adapter import TelloAdapter
from src.infrastructure.redis_adapter import RedisAdapter
from src.application.services.speaking_service import SpeakingService
from src.application.services.logging_service import LoggingService

from src.application.routines.go_to_camera import routine_room

class DroneRoutine:
	"""Video loop (OpenCV) that enqueues flight commands."""

	def __init__(
		self, 
		tello_adapter: TelloAdapter,
		speaking_service: SpeakingService,
		logging_service: LoggingService,
		redis_adapter: RedisAdapter,
	) -> None:
		self.tello_adapter = tello_adapter
		self._redis_adapter = redis_adapter
		self.speaking_service = speaking_service
		self.logging_service = logging_service
		self.running = False

	def show_image(self, window_name: str, frame) -> None:
		cv2.imshow(window_name, frame)

	def handle_stop(self) -> None:
		self.running = False
		self.logging_service.info("Stop pressed")
		self.speaking_service.text_to_voice("You have landed the drone")
		cv2.destroyAllWindows()

	def start_up_config(self) -> None:
		"""One-time startup: enable video stream."""
		self.running = True
		time.sleep(2)
		self.tello_adapter.stream_off()
		time.sleep(2)
		self.tello_adapter.stream_on()
		time.sleep(2)

	def consume_events(self) -> None:
		for event in self._redis_adapter.consume("threat"):
			if not self.running:
				return
			if str(event).strip().lower() == "knife threat was detected":
				self.logging_service.info("Threat event received. Running routine.")
				routine_room(tello_adapter=self.tello_adapter)

	def start_loop(self) -> None:
		threading.Thread(target=self.consume_events, daemon=True).start()
		self.start_up_config()

		while self.running:
			frame_read = self.tello_adapter.get_frame_read()
			drone_frame = frame_read.frame
			key = self.show_image(
				window_name="Tello Camera", 
				frame=drone_frame
			)

			if key in (ord("0"), ord("q")):
				self.handle_stop()
			
			cv_key = cv2.waitKey(1) & 0xFF