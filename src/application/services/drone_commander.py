from __future__ import annotations

from queue import Queue
import time
from typing import Optional, Tuple

import cv2
import pygame

from src.infrastructure.tello_adapter import TelloAdapter
from src.application.services.command_worker import CommandWorker
from src.application.services.speaking_service import SpeakingService
from src.application.services.logging_service import LoggingService

class DroneCommander:
	"""UI loop (pygame) + video loop (OpenCV) that enqueues flight commands."""

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
		pygame.init()
		self.running = False
		self.screen_width = 800
		self.screen_height = 600
		# pygame needs a display surface to reliably receive keyboard events
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

	def handle_keydown(self, event_key: int, distance: int = 60) -> None:
		"""Map keyboard keys to queued commands (distance in centimeters)."""
		if event_key == pygame.K_w:
			self.logging_service.info("Command: forward")
			self.command_queue.put(("w", distance))
			self.speaking_service.text_to_voice(f"You have moved forward {distance} centimeters")
		elif event_key == pygame.K_a:
			self.logging_service.info("Command: left")
			self.command_queue.put(("a", distance))
			self.speaking_service.text_to_voice(f"You have moved left {distance} centimeters")
		elif event_key == pygame.K_s:
			self.logging_service.info("Command: back")
			self.command_queue.put(("s", distance))
			self.speaking_service.text_to_voice(f"You have moved backward {distance} centimeters")
		elif event_key == pygame.K_d:
			self.logging_service.info("Command: right")
			self.command_queue.put(("d", distance))
			self.speaking_service.text_to_voice(f"You have moved right {distance} centimeters")
		elif event_key == pygame.K_UP:
			self.logging_service.info("Command: up")
			self.command_queue.put(("+", distance))
			self.speaking_service.text_to_voice(f"You have moved up {distance} centimeters")
		elif event_key == pygame.K_DOWN:
			self.logging_service.info("Command: down")
			self.command_queue.put(("-", distance))
			self.speaking_service.text_to_voice(f"You have moved down {distance} centimeters")
		elif event_key == pygame.K_r:
			self.logging_service.info("Command: rotate right")
			self.command_queue.put(("rotate_right", 90))
			self.speaking_service.text_to_voice("You have rotated right 90 degrees")
		elif event_key == pygame.K_l:
			self.logging_service.info("Command: rotate left")
			self.command_queue.put(("rotate_left", 90))
			self.speaking_service.text_to_voice("You have rotated left 90 degrees")

	def handle_stop(self) -> None:
		self.running = False
		self.logging_service.info("Stop pressed")
		self.command_queue.put(("del", None))
		self.speaking_service.text_to_voice("You have landed the drone")
		cv2.destroyAllWindows()

	def start_up_config(self) -> None:
		"""One-time startup: takeoff + enable video stream."""
		self.running = True
		pygame.display.set_caption("Drone Commander")

		time.sleep(4)
		self.command_queue.put(("take_off", None))
		time.sleep(2)
		self.tello_adapter.stream_off()
		time.sleep(2)
		self.tello_adapter.stream_on()
		time.sleep(2)

	def start_loop(self) -> None:
		while self.running:
			frame_read = self.tello_adapter.get_frame_read()
			frame = frame_read.frame

			cv2.imshow("Tello Camera", frame)
			# OpenCV needs this to update the window and process events
			cv2.waitKey(1)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					battery = self.tello_adapter.get_battery()
					self.logging_service.info(f"Battery: {battery}%")
					if event.key == pygame.K_0:
						self.handle_stop()
						break
					self.handle_keydown(event.key)