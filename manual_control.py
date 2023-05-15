from finite_state_machine import FiniteStateMachine
from state import MonitoredState, RobotState
from functools import partial
from side_blinkers import SideBlinkers

    

class ManualControl(FiniteStateMachine):
    def __init__(self, robot):
        
        # création des states
        self.forward = RobotState(robot)
        self.backward = RobotState(robot)
        self.rotate_left = RobotState(robot)
        self.rotate_right = RobotState(robot)
        self.stop = RobotState(robot)
        
        
        
        # création des actions de states
        self.forward.add_in_state_action(lambda: robot.brain.forward())
        self.forward.add_entering_action(lambda: robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.BOTH, percent_on = 0.25, cycle_duration = 1.0))
        
        self.backward.add_in_state_action(lambda: robot.brain.backward())
        self.backward.add_entering_action(lambda: robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.BOTH, percent_on = 0.75, cycle_duration = 1.0))
        
        self.rotate_left.add_in_state_action(lambda: robot.brain.left())
        self.rotate_left.add_entering_action(lambda: robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.LEFT, percent_on = 0.50, cycle_duration = 1.0))

        self.rotate_right.add_in_state_action(lambda: robot.brain.right())
        self.rotate_right.add_entering_action(lambda: robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.RIGHT, percent_on = 0.50, cycle_duration = 1.0))

        
        def shut_down_robot(robot):
            robot.brain.close_eyes()
            robot.brain.blinker_off(0)
            robot.brain.blinker_off(1)
            robot.brain.stop()
        self.stop.add_entering_action(partial(shut_down_robot, robot))


        
        
        layout = FiniteStateMachine.Layout()
        layout.initial_state = self.stop
        layout.add_states([self.forward, self.backward, self.rotate_left, self.rotate_right, self.stop])
        
        # Create fsm
        super().__init__(layout=layout, unitialized=False)
