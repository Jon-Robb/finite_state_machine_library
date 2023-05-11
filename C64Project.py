from robot import Robot
from side_blinkers import SideBlinkers
from finite_state_machine import FiniteStateMachine

class C64Project:
    def __init__(self):
        
        
        app = FiniteStateMachine()
        self.robot = Robot()
        
    def start(self):
        self.robot.start()
        print("100%!")
        
if __name__ == '__main__':
    c64_project = C64Project()
    
    c64_project.robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)
    c64_project.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)

    c64_project.start()