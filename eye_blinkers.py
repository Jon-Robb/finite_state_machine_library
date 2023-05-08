from side_blinkers import SideBlinkers
from Blinker import Blinker
from robot import Robot

class EyeBlinkers(SideBlinkers):
    def __init__(self, left_off_state_generator: Blinker.StateGenerator, left_on_state_generator: Blinker.StateGenerator, right_off_state_generator: Blinker.StateGenerator, right_on_state_generator: Blinker.StateGenerator, robot: Robot) -> None:
        super.__init__(left_off_state_generator, left_on_state_generator, right_off_state_generator, right_on_state_generator)
        self.robot = robot
    
    