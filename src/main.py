from __future__ import annotations

from threading import Thread

from src.dependencies import get_drone_commander, get_command_worker

if __name__ == '__main__':
	# Start the command consumer on a background thread, and keep the UI/video loop
	# on the main thread.
	drone_commander = get_drone_commander()
	command_worker = get_command_worker()

	drone_commander.start_up_config()

	commander_thread = Thread(target=command_worker.start_loop)
	commander_thread.start()

	drone_commander.start_loop()

	commander_thread.join()
