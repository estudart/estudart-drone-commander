from __future__ import annotations

from queue import Queue
from typing import Optional, Tuple

from src.infrastructure.tello_adapter import TelloAdapter
from src.application.services.logging_service import LoggingService

class CommandWorker:
	"""Consumes commands from a queue and forwards them to the drone adapter."""

	def __init__(
		self,
		tello_adapter: TelloAdapter,
		logging_service: LoggingService,
		command_queue: Queue[Tuple[str, Optional[int]]],
	) -> None:
		self.tello_adapter = tello_adapter
		self.logging_service = logging_service
		self.command_queue = command_queue
		self.max_retries = 3
		self.running = False

	def take_off_retry(self) -> None:
		"""Attempt takeoff a few times (Tello can be flaky right after connect)."""
		retries = 0
		while retries < self.max_retries:
			if self.tello_adapter.take_off():
				self.logging_service.info("Takeoff successful")
				return
			retries += 1
		self.logging_service.error("Max retries for take off")

	def handle_stop(self) -> None:
		self.running = False
		self.tello_adapter.land()
		self.tello_adapter.stream_off()

	def handle_event(self, command: str, distance: Optional[int]) -> None:
		if command == 'w':
			self.tello_adapter.move_forward(distance or 0)
		elif command == 'a':
			self.tello_adapter.move_left(distance or 0)
		elif command == 's':
			self.tello_adapter.move_back(distance or 0)
		elif command == 'd':
			self.tello_adapter.move_right(distance or 0)
		elif command == '+':
			self.tello_adapter.move_up(distance or 0)
		elif command == '-':
			self.tello_adapter.move_down(distance or 0)
		elif command == 'take_off':
			self.take_off_retry()
		elif command == 'rotate_right':
			self.tello_adapter.rotate_right(distance or 0)
		elif command == 'rotate_left':
			self.tello_adapter.rotate_left(distance or 0)
	
	def start_loop(self) -> None:
		self.running = True

		while self.running:
			command, distance = self.command_queue.get()
			self.handle_event(command=command, distance=distance)

			if command == 'del':
				self.logging_service.info("Landing drone")
				self.handle_stop()
