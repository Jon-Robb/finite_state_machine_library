from side_blinkers import SideBlinkers
import easygopigo3 as gpg
from eye_blinkers import EyeBlinkers
from led_blinkers import LedBlinkers
from manual_control import ManualControl
from distance_color import DistanceColor
from finite_state_machine import FiniteStateMachine


class Robot:
    def __init__(self):
      
        self.success_brain_implement = None
        self.success_auxiliary_implement = None
        remote_control_port = 'AD1'
        distance_finder_port = 'I2C'
    
        self.remote_input = None
        self.state_machines = {}
        self.active_state_machine = None
        
        
        try:
            self.brain = gpg.EasyGoPiGo3()
            self.state_machines["led_blinkers"] = LedBlinkers(self.brain)
            self.state_machines["eye_blinkers"] = EyeBlinkers(self.brain, (255,0,0), (0,255,0))
            self.success_brain_implement = True
        except Exception as e:
            print("Failed to instantiate from the GoPiGo3 library")
            print(e)
            self.success_brain_implement = False
        
        
        try:
            self.remote = self.brain.init_remote(port=remote_control_port)
            self.distance = self.brain.init_distance_sensor(port=distance_finder_port)
            
            self.state_machines["manual_control"] = ManualControl(self)
            self.state_machines["distance_color"] = DistanceColor(self)
            
            self.success_auxiliary_implement = True
        except Exception as e:
            self.success_auxiliary_implement = False
            print("Failed to instantiate from the Remote Control library and etc. ")
            print(e)
        
    # def start(self):
    #     while True:
    #         self.remote_input = self.remote.read()
    #         for state_machine in self.state_machines.values():
    #             state_machine.track()
        
    def track(self):
        # while True:
        self.remote_input = self.remote.read()
        for state_machine in self.state_machines.values():
            if state_machine in [self.state_machines["led_blinkers"], self.state_machines["eye_blinkers"]]or state_machine == self.active_state_machine:
                state_machine.track()
    
if __name__ == '__main__':
    robot = Robot()

    # robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)
    # robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.RIGHT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)
    # robot.state_machines["manual_control"].current_applicative_state._do_entering_action()

    robot.start()