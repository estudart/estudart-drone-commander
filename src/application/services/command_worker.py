from queue import Queue

from src.infrastructure.tello_adapter import TelloAdapter

class CommandWorker:
	def __init__(self, tello_adapter: TelloAdapter, command_queue: Queue):
		self.tello_adapter = tello_adapter
		self.command_queue = command_queue
		self.max_retries = 3
		self.running = False

	def take_off_retry(self):
		retries = 0
		is_take_off = self.tello_adapter.take_off()
		while not retries < self.max_retries:
			self.tello_adapter.take_off()
		print("Max retries for take off")

	def handle_stop(self):
		self.running = False
		self.tello_adapter.land()
		self.tello_adapter.stream_off()

	def handle_event(self, command: str, distance: int):
		if command == 'w':
			self.tello_adapter.move_forward(distance)
		elif command == 'a':
			self.tello_adapter.move_left(distance)
		elif command == 's':
			self.tello_adapter.move_back(distance)
		elif command == 'd':
			self.tello_adapter.move_right(distance)
		elif command == '+':
			self.tello_adapter.move_up(distance)
		elif command == '-':
			self.tello_adapter.move_down(distance)
		elif command == 'take_off':
			self.take_off_retry()
		elif command == 'rotate_right':
			self.tello_adapter.rotate_right(distance)
		elif command == 'rotate_left':
			self.tello_adapter.rotate_left(distance)
	
	def start_loop(self):
		self.running = True

		while self.running:
			command, distance = self.command_queue.get()
			self.handle_event(
				command=command,
				distance=distance
			)

			if command == 'del':
				print('landing drone')
				self.handle_stop()
