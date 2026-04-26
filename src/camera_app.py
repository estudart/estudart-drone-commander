from __future__ import annotations

from threading import Thread

from src.dependencies import get_threat_detector

if __name__ == '__main__':
	threat_detector = get_threat_detector()
	threat_detector.start_loop()
