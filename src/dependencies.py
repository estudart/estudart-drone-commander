from typing import Optional
from queue import Queue

from src.infrastructure.tello_adapter import TelloAdapter
from src.application.services.drone_commander import DroneCommander
from src.application.services.command_worker import CommandWorker
from src.application.services.speaking_service import SpeakingService

_tello_adapter: Optional[TelloAdapter] = None
_drone_commander: Optional[DroneCommander] = None
_command_worker: Optional[CommandWorker] = None
_speaking_service: Optional[SpeakingService] = None
_queue: Queue = None

def get_command_queue() -> Queue:
	global _queue
	if not _queue:
		_queue = Queue()
	return _queue

def get_speaking_service() -> SpeakingService:
	global _speaking_service
	if not _speaking_service:
		_speaking_service = SpeakingService()
	return _speaking_service

def get_tello_adapter() -> TelloAdapter:
	global _tello_adapter
	if not _tello_adapter:
		_tello_adapter = TelloAdapter()
	return _tello_adapter

def get_drone_commander() -> DroneCommander:
	global _drone_commander
	if not _drone_commander:
		tello_adapter = get_tello_adapter()
		speaking_service = get_speaking_service()
		command_worker = get_command_worker()
		command_queue = get_command_queue()

		_drone_commander = DroneCommander(
			tello_adapter=tello_adapter,
			speaking_service=speaking_service,
			command_worker=command_worker,
			command_queue=command_queue
		)
	return _drone_commander

def get_command_worker() -> CommandWorker:
	global _command_worker
	if not _command_worker:
		tello_adapter = get_tello_adapter()
		command_queue = get_command_queue()

		_command_worker = CommandWorker(
			tello_adapter=tello_adapter,
			command_queue=command_queue
		)
	return _command_worker
