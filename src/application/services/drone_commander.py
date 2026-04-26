from __future__ import annotations

from queue import Queue
import time
from typing import Optional, Tuple

import cv2

from src.infrastructure.tello_adapter import TelloAdapter
from src.application.services.command_worker import CommandWorker
from src.application.services.speaking_service import SpeakingService
from src.application.services.logging_service import LoggingService

class DroneCommander:
	"""Video loop (OpenCV) that enqueues flight commands."""

	def __init__(
		self, 
		tello_adapter: TelloAdapter,
		speaking_service: SpeakingService,
		logging_service: LoggingService,
		command_worker: CommandWorker,
		command_queue: Queue[Tuple[str, Optional[int]]],
	) -> None:
		self.tello_adapter = tello_adapter
		self.speaking_service = speaking_service
		self.logging_service = logging_service
		self.command_worker = command_worker
		self.command_queue = command_queue
		self.running = False

	def _enqueue_move(self, command: str, distance: int = 60) -> None:
		self.command_queue.put((command, distance))

	def _enqueue_simple(self, command: str) -> None:
		self.command_queue.put((command, None))

	def handle_stop(self) -> None:
		self.running = False
		self.logging_service.info("Stop pressed")
		self._enqueue_simple("del")
		self.speaking_service.text_to_voice("You have landed the drone")
		cv2.destroyAllWindows()

	def start_up_config(self) -> None:
		"""One-time startup: takeoff + enable video stream."""
		self.running = True

		time.sleep(4)
		self._enqueue_simple("take_off")
		time.sleep(2)
		self.tello_adapter.stream_off()
		time.sleep(2)
		self.tello_adapter.stream_on()
		time.sleep(2)

	def _process_cv2_key(self, cv_key: int) -> None:
		"""
		Handle keyboard input via OpenCV windows.

		We intentionally avoid arrow keys because keycodes vary by OS/backend.
		"""
		if cv_key < 0:
			return

		# Normalize to lowercase ASCII when possible.
		if 65 <= cv_key <= 90:
			cv_key = cv_key + 32

		if cv_key == ord("0"):
			self.handle_stop()
			return

		# Movement
		if cv_key == ord("w"):
			self.logging_service.info("Command: forward")
			self._enqueue_move("w")
			self.speaking_service.text_to_voice("You have moved forward 60 centimeters")
		elif cv_key == ord("a"):
			self.logging_service.info("Command: left")
			self._enqueue_move("a")
			self.speaking_service.text_to_voice("You have moved left 60 centimeters")
		elif cv_key == ord("s"):
			self.logging_service.info("Command: back")
			self._enqueue_move("s")
			self.speaking_service.text_to_voice("You have moved backward 60 centimeters")
		elif cv_key == ord("d"):
			self.logging_service.info("Command: right")
			self._enqueue_move("d")
			self.speaking_service.text_to_voice("You have moved right 60 centimeters")
		elif cv_key in (ord("i"), ord("+")):
			self.logging_service.info("Command: up")
			self._enqueue_move("+")
			self.speaking_service.text_to_voice("You have moved up 60 centimeters")
		elif cv_key in (ord("k"), ord("-")):
			self.logging_service.info("Command: down")
			self._enqueue_move("-")
			self.speaking_service.text_to_voice("You have moved down 60 centimeters")

		# Rotation (support both r/l and q/e to match common layouts)
		elif cv_key in (ord("r"), ord("e")):
			self.logging_service.info("Command: rotate right")
			self.command_queue.put(("rotate_right", 90))
			self.speaking_service.text_to_voice("You have rotated right 90 degrees")
		elif cv_key in (ord("l"), ord("q")):
			self.logging_service.info("Command: rotate left")
			self.command_queue.put(("rotate_left", 90))
			self.speaking_service.text_to_voice("You have rotated left 90 degrees")

		# Optional manual takeoff (useful if you disable auto-takeoff later)
		elif cv_key == ord("t"):
			self.logging_service.info("Command: takeoff")
			self._enqueue_simple("take_off")

	def start_loop(self) -> None:
		while self.running:
			frame_read = self.tello_adapter.get_frame_read()
			drone_frame = frame_read.frame
			self.show_image(
				window_name="Tello Camera", 
				frame=drone_frame
			)

			cv_key = cv2.waitKey(1) & 0xFF
			self._process_cv2_key(cv_key)