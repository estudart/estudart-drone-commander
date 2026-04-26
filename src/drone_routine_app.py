from __future__ import annotations

from threading import Thread

from src.dependencies import get_drone_routine

if __name__ == '__main__':
	drone_routine = get_drone_routine()
	drone_routine.start_loop()
