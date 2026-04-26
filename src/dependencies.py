from __future__ import annotations

from queue import Queue
from typing import Optional, Tuple

from src.infrastructure.tello_adapter import TelloAdapter
from src.infrastructure.camera_adapter import CameraAdapter
from src.application.services.threat_detector import ThreatDetector
from src.application.services.drone_routine import DroneRoutine
from src.application.services.speaking_service import SpeakingService
from src.application.services.logging_service import LoggingService
from src.infrastructure.redis_adapter import RedisAdapter

_tello_adapter: Optional[TelloAdapter] = None
_camera_adapter: Optional[CameraAdapter] = None
_threat_detector: Optional[ThreatDetector] = None
_drone_routine: Optional[DroneRoutine] = None
_speaking_service: Optional[SpeakingService] = None
_redis_adapter: Optional[RedisAdapter] = None
_logging_service: Optional[LoggingService] = None
_queue: Optional[Queue[Tuple[str, Optional[int]]]] = None
_drone_commander = None
_command_worker = None

def get_command_queue() -> Queue[Tuple[str, Optional[int]]]:
	global _queue
	if not _queue:
		_queue = Queue()
	return _queue

def get_logging_service() -> LoggingService:
	global _logging_service
	if not _logging_service:
		_logging_service = LoggingService()
	return _logging_service

def get_speaking_service() -> SpeakingService:
	global _speaking_service
	if not _speaking_service:
		_speaking_service = SpeakingService()
	return _speaking_service

def get_tello_adapter() -> TelloAdapter:
	global _tello_adapter
	if not _tello_adapter:
		logging_service = get_logging_service()
		_tello_adapter = TelloAdapter(logging_service=logging_service)
	return _tello_adapter

def get_camera_adapter() -> CameraAdapter:
	global _camera_adapter
	if not _camera_adapter:
		logging_service = get_logging_service()
		_camera_adapter = CameraAdapter(logging_service=logging_service)
	return _camera_adapter

def get_drone_routine() -> DroneRoutine:
	global _drone_routine
	if not _drone_routine:
		tello_adapter = get_tello_adapter()
		speaking_service = get_speaking_service()
		logging_service = get_logging_service()
		redis_adapter = get_redis_adapter()

		_drone_routine = DroneRoutine(
			tello_adapter=tello_adapter,
			speaking_service=speaking_service,
			logging_service=logging_service,
			redis_adapter=redis_adapter,
		)
	return _drone_routine

# Legacy factories kept for backwards-compat; lazy import avoids loading unused modules.
def get_command_worker():
	from src.application.services.command_worker import CommandWorker  # local import

	global _command_worker
	if _command_worker is None:
		tello_adapter = get_tello_adapter()
		logging_service = get_logging_service()
		command_queue = get_command_queue()
		_command_worker = CommandWorker(
			tello_adapter=tello_adapter,
			logging_service=logging_service,
			command_queue=command_queue,
		)
	return _command_worker

def get_drone_commander():
	from src.application.services.drone_commander import DroneCommander  # local import

	global _drone_commander
	if _drone_commander is None:
		tello_adapter = get_tello_adapter()
		speaking_service = get_speaking_service()
		logging_service = get_logging_service()
		command_worker = get_command_worker()
		command_queue = get_command_queue()
		_drone_commander = DroneCommander(
			tello_adapter=tello_adapter,
			speaking_service=speaking_service,
			logging_service=logging_service,
			command_worker=command_worker,
			command_queue=command_queue,
		)
	return _drone_commander

def get_threat_detector() -> ThreatDetector:
	global _threat_detector
	if not _threat_detector:
		camera_adapter = get_camera_adapter()
		redis_adapter = get_redis_adapter()
		logging_service = get_logging_service()

		_threat_detector = ThreatDetector(
			camera_adapter=camera_adapter,
			redis_adapter=redis_adapter,
			logging_service=logging_service
		)
	return _threat_detector

def get_redis_adapter() -> RedisAdapter:
	global _redis_adapter
	if not _redis_adapter:
		_redis_adapter = RedisAdapter()
	return _redis_adapter
