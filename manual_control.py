from finite_state_machine import FiniteStateMachine
from state import MonitoredState, RobotState
from functools import partial
from side_blinkers import SideBlinkers
from Condition import RemoteValueCondition
from transition import ConditionalTransition

    

class ManualControl(FiniteStateMachine):
    def __init__(self, robot):
        
        # création des states
        self.forward = RobotState(robot)
        self.backward = RobotState(robot)
        self.rotate_left = RobotState(robot)
        self.rotate_right = RobotState(robot)
        self.stop = RobotState(robot)
        
        
        def shut_down_robot(robot):
            robot.state_machines["led_blinkers"].turn_off(SideBlinkers.Side.BOTH)
            robot.brain.stop()
        
        # création des actions de states
        self.forward.add_in_state_action(lambda: robot.brain.forward())
        self.forward.add_entering_action(lambda: robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.BOTH, percent_on = 0.25, cycle_duration = 1.0))
        self.backward.add_in_state_action(lambda: robot.brain.backward())
        self.backward.add_entering_action(lambda: robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.BOTH, percent_on = 0.75, cycle_duration = 1.0))
        
        self.rotate_left.add_in_state_action(lambda: robot.brain.left())
        self.rotate_left.add_entering_action(lambda: robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.LEFT, percent_on = 0.50, cycle_duration = 1.0))

        self.rotate_right.add_in_state_action(lambda: robot.brain.right())
        self.rotate_right.add_entering_action(lambda: robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.RIGHT, percent_on = 0.50, cycle_duration = 1.0))

        self.stop.add_entering_action(partial(shut_down_robot, robot))
        

        # Création des conditions
        stop_to_forward_condition = RemoteValueCondition(robot.remote, 1)
        stop_to_backward_condition = RemoteValueCondition(robot.remote, 5)
        stop_to_right_condition = RemoteValueCondition(robot.remote, 4)
        stop_to_left_condition = RemoteValueCondition(robot.remote, 2)
        forward_to_stop_condition = RemoteValueCondition(robot.remote, 1, True)
        backward_to_stop_condition = RemoteValueCondition(robot.remote, 5, True)
        right_to_stop_condition = RemoteValueCondition(robot.remote, 4, True)
        left_to_stop_condition = RemoteValueCondition(robot.remote, 2, True)
        
        # Créations des Transitions
        stop_to_forward_transition = ConditionalTransition(self.forward, stop_to_forward_condition)
        stop_to_backward_transition = ConditionalTransition(self.backward, stop_to_backward_condition)
        stop_to_right_transition = ConditionalTransition(self.rotate_right, stop_to_right_condition)
        stop_to_left_transition = ConditionalTransition(self.rotate_left, stop_to_left_condition)
        forward_to_stop_transition = ConditionalTransition(self.stop, forward_to_stop_condition)
        backward_to_stop_transition = ConditionalTransition(self.stop, backward_to_stop_condition)
        right_to_stop_transition = ConditionalTransition(self.stop, right_to_stop_condition)
        left_to_stop_transition = ConditionalTransition(self.stop, left_to_stop_condition)
        
        
        # Ajout des transitions
        self.stop.add_transition(stop_to_forward_transition)
        self.stop.add_transition(stop_to_backward_transition)
        self.stop.add_transition(stop_to_left_transition)
        self.stop.add_transition(stop_to_right_transition)
        self.forward.add_transition(forward_to_stop_transition)
        self.backward.add_transition(backward_to_stop_transition)
        self.rotate_left.add_transition(left_to_stop_transition)
        self.rotate_right.add_transition(right_to_stop_transition)
        
    
        
        layout = FiniteStateMachine.Layout()
        layout.initial_state = self.stop
        layout.add_states([self.forward, self.backward, self.rotate_left, self.rotate_right, self.stop])
        
        # Create fsm
        super().__init__(layout=layout, unitialized=False)
