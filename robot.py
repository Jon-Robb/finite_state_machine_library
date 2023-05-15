from side_blinkers import SideBlinkers
import easygopigo3 as gpg
from eye_blinkers import EyeBlinkers
from led_blinkers import LedBlinkers
from manual_control import ManualControl

class Robot:
    def __init__(self) -> None:
        self.brain = gpg.EasyGoPiGo3()
        
        remote_control_port = 'AD1'
        
        self.remote = self.brain.init_remote(port=remote_control_port)
        self.remote_input = None
        self.state_machines = {}
        
        self.state_machines["led_blinkers"] = LedBlinkers(self.brain)
        self.state_machines["eye_blinkers"] = EyeBlinkers(self.brain, (255,0,0), (0,0,255))
        self.state_machines["manual_control"] = ManualControl(self)
        
    def start(self):
        while True:
            self.remote_input = self.remote.read()
            for state_machine in self.state_machines.values():
                state_machine.track()
        
        
if __name__ == '__main__':
    robot = Robot()

    # robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)
    # robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.RIGHT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)
    # robot.state_machines["manual_control"].current_applicative_state._do_entering_action()

    robot.start()