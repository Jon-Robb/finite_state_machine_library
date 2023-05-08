from side_blinkers import SideBlinkers
from Blinker import Blinker
from state import MonitoredState
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from robot import Robot

class LedBlinkers(SideBlinkers):
    def __init__(self, robot: Robot) -> None:
        self.robot = robot
                
        def left_off_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: self.robot.left_eye.off())
            
        def right_off_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: self.robot.right_eye.off())   
            
        def left_on_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: self.robot.left_eye.on())
        
        def right_on_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: self.robot.right_eye.on()) 
                
        super.__init__(left_off_state_generator, left_on_state_generator, right_off_state_generator, right_on_state_generator)
    