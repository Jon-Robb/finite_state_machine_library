from side_blinkers import SideBlinkers
from Blinker import Blinker
from state import MonitoredState


class LedBlinkers(SideBlinkers):
    def __init__(self, robot) -> None:
        self.robot = robot
                
        def left_off_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: robot.led_off(1))
            return state
            
        def right_off_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: robot.led_off(0))   
            return state

            
        def left_on_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: robot.led_on(1))
            return state
        
        def right_on_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: robot.led_on(0)) 
            return state
        
        super().__init__(left_off_state_generator, left_on_state_generator, right_off_state_generator, right_on_state_generator)
    