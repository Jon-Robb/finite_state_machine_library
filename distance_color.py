
from finite_state_machine import FiniteStateMachine
from state import MonitoredState, RobotState
from functools import partial
from side_blinkers import SideBlinkers
from Condition import RemoteValueCondition
from transition import ConditionalTransition
from assembling_functions import assemble_state_transitions_and_between_condition

class DistanceColor(FiniteStateMachine):
    def __init__(self, robot) -> None:
        self.min_distance = RobotState(robot)
        self.min_medium_distance = RobotState(robot)
        self.medium_distance = RobotState(robot)
        self.max_medium_distance = RobotState(robot)
        self.max_distance = RobotState(robot)
        self.robot = robot
        
        assemble_state_transitions_and_between_condition(self.min_medium_distance, self.min_distance, 0, 10, robot.distance)
       
        assemble_state_transitions_and_between_condition(self.min_distance, self.min_medium_distance, 10, 20, robot.distance)
        assemble_state_transitions_and_between_condition(self.medium_distance, self.min_medium_distance, 10, 20, robot.distance)
       
        assemble_state_transitions_and_between_condition(self.min_medium_distance, self.medium_distance, 20, 30, robot.distance)
        assemble_state_transitions_and_between_condition(self.max_medium_distance, self.medium_distance, 20, 30, robot.distance)
        
        assemble_state_transitions_and_between_condition(self.medium_distance, self.max_medium_distance, 30, 40, robot.distance)
        assemble_state_transitions_and_between_condition(self.max_distance, self.max_medium_distance, 30, 40, robot.distance)
        
        assemble_state_transitions_and_between_condition(self.max_medium_distance, self.max_distance, 40, 50, robot.distance)

        self.min_distance.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(255,0,0)))
        self.min_distance.add_in_state_action(lambda: self.robot.state_machines["eye_blinkers"].turn_on(SideBlinkers.Side.BOTH)) 
        self.min_distance.add_in_state_action(lambda: print(f'La distance est de {self.robot.distance.read()}', end='\r'))
        
        self.min_medium_distance.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(120,0,0)))
        self.min_medium_distance.add_in_state_action(lambda: self.robot.state_machines["eye_blinkers"].turn_on(SideBlinkers.Side.BOTH))
        self.min_medium_distance.add_in_state_action(lambda: print(f'La distance est de {self.robot.distance.read()}', end='\r'))
        
        self.medium_distance.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(255,0,255)))
        self.medium_distance.add_in_state_action(lambda: self.robot.state_machines["eye_blinkers"].turn_on(SideBlinkers.Side.BOTH))
        self.medium_distance.add_in_state_action(lambda: print(f'La distance est de {self.robot.distance.read()}', end='\r'))
        
        self.max_medium_distance.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(0,0,120)))
        self.max_medium_distance.add_in_state_action(lambda: self.robot.state_machines["eye_blinkers"].turn_on(SideBlinkers.Side.BOTH))
        self.max_medium_distance.add_in_state_action(lambda: print(f'La distance est de {self.robot.distance.read()}', end='\r'))
        
        self.max_distance.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(0,0,255)))
        self.max_distance.add_in_state_action(lambda: self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.BOTH, begin_on = True, cycle_duration = 0.1))
        self.max_distance.add_in_state_action(lambda: print(f'La distance est de {self.robot.distance.read()} ', end='\r'))
        
        layout = FiniteStateMachine.Layout()
        layout.initial_state = self.min_distance
        layout.add_states([self.min_distance, self.min_medium_distance, self.medium_distance, self.max_medium_distance, self.max_distance])
        super().__init__(layout, unitialized=False)        