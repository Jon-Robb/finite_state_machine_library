from eye_blinkers import EyeBlinkers
from led_blinkers import LedBlinkers
from easygopigo3 import EasyGoPiGo3



class Robot:
    def __init__(self, ledBlinker:LedBlinkers, eyesBlinker:EyeBlinkers) -> None:
        self.ledBlinker = LedBlinkers(self)
        self.eyesBlinker = EyeBlinkers(self)
        self.robot = GoPiGo3()