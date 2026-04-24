import time
from djitellopy import Tello


class TelloAdapter:
    def __init__(self):
        self.tello = Tello()
        self._connect()

    def _connect(self):
        try:
            self.tello.connect()
            return True
        except Exception as err:
            print(err)
            raise

    def get_battery(self) -> int:
        return self.tello.get_battery()

    def stream_on(self) -> bool:
        try:
            self.tello.streamon()
            return True
        except Exception as err:
            print(err)
            return False

    def stream_off(self) -> bool:
        try:
            self.tello.streamoff()
            return True
        except Exception as err:
            print(err)
            return False

    def get_frame_read(self):
        try:
            return self.tello.get_frame_read()
        except Exception as err:
            print(err)

    def take_off(self) -> bool:
        try:
            self.tello.takeoff()
            time.sleep(5)
            return True
        except Exception as err:
            print(err)
            return False

    def land(self) -> bool:
        try:
            self.tello.land()
            return True
        except Exception as err:
            print(err)
            return False

    def move_up(self, distance: int) -> bool:
        try:
            self.tello.move_up(distance)
            return True
        except Exception as err:
            print(err)
            return False

    def move_down(self, distance: int) -> bool:
        try:
            self.tello.move_down(distance)
            return True
        except Exception as err:
            print(err)
            return False

    def move_forward(self, distance: int) -> bool:
        try:
            self.tello.move_forward(distance)
            return True
        except Exception as err:
            print(err)
            return False

    def move_back(self, distance: int) -> bool:
        try:
            self.tello.move_back(distance)
            return True
        except Exception as err:
            print(err)
            return False

    def move_left(self, distance: int) -> bool:
        try:
            self.tello.move_left(distance)
            return True
        except Exception as err:
            print(err)
            return False
    
    def move_right(self, distance: int) -> bool:
        try:
            self.tello.move_right(distance)
            return True
        except Exception as err:
            print(err)
            return False

    def rotate_right(self, degrees: int):
        self.tello.rotate_clockwise(degrees)

    def rotate_left(self, degrees: int):
        self.tello.rotate_counter_clockwise(degrees)