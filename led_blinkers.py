from side_blinkers import SideBlinkers

class LedBlinkers(SideBlinkers):
    def __init__(self, robot) -> None:
        self.robot = robot
    
    