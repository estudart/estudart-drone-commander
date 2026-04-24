from queue import Queue
import sys
import time

import pygame
import cv2

from src.infrastructure.tello_adapter import TelloAdapter
from src.application.services.command_worker import CommandWorker
from src.application.services.speaking_service import SpeakingService

class DroneCommander:
	def __init__(
		self, 
		tello_adapter: TelloAdapter,
		speaking_service: SpeakingService,
		command_worker: CommandWorker,
		command_queue: Queue
	):
		self.tello_adapter = tello_adapter
		self.speaking_service = speaking_service
		self.command_worker = command_worker
		self.command_queue = command_queue
		pygame.init()
		self.running = False
		self.screen_width = 800
		self.screen_height = 600

	def handle_keydown(self, event_key, distance: int = 20):
		if event_key == pygame.K_w:
			print('w')
			self.command_queue.put(("w", 20))
			self.speaking_service.text_to_voice("You have moved forward")
		if event_key == pygame.K_a:
			print('a')
			self.command_queue.put(("a", 20))
			self.speaking_service.text_to_voice("You have moved left")
		elif event_key == pygame.K_s:
			print('s')
			self.command_queue.put(("s", 20))
			self.speaking_service.text_to_voice("You have moved backward")
		elif event_key == pygame.K_d:
			print('d')
			self.command_queue.put(("d", 20))
			self.speaking_service.text_to_voice("You have moved right")
		elif event_key == pygame.K_UP:
			print('+')
			self.command_queue.put(("+", 20))
			self.speaking_service.text_to_voice("You have moved up")
		elif event_key == pygame.K_DOWN:
			print('-')
			self.command_queue.put(("-", 20))
			self.speaking_service.text_to_voice("You have moved down")
		elif event_key == pygame.K_r:
			print('r')
			self.command_queue.put(("rotate_right", 180))
			self.speaking_service.text_to_voice("You have rotated right 180 degrees")
		elif event_key == pygame.K_l:
			print('l')
			self.command_queue.put(("rotate_left", 180))
			self.speaking_service.text_to_voice("You have rotated left 180 degrees")

	def handle_stop(self):
		self.running = False
		print("You have pressed 'del'")
		self.command_queue.put(("del", None))
		cv2.destroyAllWindows()

	def start_up_config(self):
		self.running = True
		pygame.display.set_caption("Drone Commander")

		time.sleep(4)
		self.command_queue.put(("take_off", None))
		time.sleep(2)
		self.tello_adapter.stream_off()
		time.sleep(2)
		self.tello_adapter.stream_on()
		time.sleep(2)

	def start_loop(self):
		while self.running:
			frame_read = self.tello_adapter.get_frame_read()
			frame = frame_read.frame

			cv2.imshow("Tello Camera", frame)
			cv2.waitKey(1)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					battery = self.tello_adapter.get_battery()
					print(f"battery: {battery}%")
					if event.key == pygame.K_0:
						self.handle_stop()
						break
					self.handle_keydown(event.key)