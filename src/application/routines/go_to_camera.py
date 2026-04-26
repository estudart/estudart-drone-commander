import time

from src.infrastructure.tello_adapter import TelloAdapter

def routine_room(tello_adapter: TelloAdapter) -> None:
    time.sleep(2)
    tello_adapter.take_off()
    time.sleep(2)
    tello_adapter.move_up(distance=60)
    time.sleep(3)
    tello_adapter.move_left(distance=60)
    time.sleep(3)
    tello_adapter.move_right(distance=60)
    time.sleep(3)
    tello_adapter.move_down(distance=60)
    time.sleep(3)
    tello_adapter.rotate_left(degrees=90)
    time.sleep(2)
    tello_adapter.rotate_right(degrees=90)
    time.sleep(2)
    tello_adapter.land()