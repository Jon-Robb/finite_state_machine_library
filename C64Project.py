from robot import Robot
from side_blinkers import SideBlinkers
from finite_state_machine import FiniteStateMachine
from state import MonitoredState, State
from assembling_functions import assemble_state_transitions_and_always_true_conditions, assemble_state_transitions_and_boolean_conditions,assemble_state_transitions_and_timed_conditions

class C64Project:
    
        
            
    def __init__(self):
        self.robot = Robot()
        
        # 1- Create states
        self.robot_instantiation = MonitoredState()
        self.robot_integrity = MonitoredState(self.robot)
        
        self.instantiation_failed = MonitoredState(self.robot)
        self.integrity_succeeded = MonitoredState(self.robot)
        self.integrity_failed = MonitoredState(self.robot)
        self.shut_down_robot = MonitoredState(self.robot)
        self.home = self.RobotState(self.robot)
        
        self.end = MonitoredState(robot = self.robot, parameters=State.Parameters(terminal=True))
        
        # TODO : Keep working on the layout
        assemble_state_transitions_and_boolean_conditions(self.robot_instantiation, self.robot_integrity, self.robot.success_brain_implement, True)
        assemble_state_transitions_and_boolean_conditions(self.robot_instantiation, self.instantiation_failed, self.robot.success_brain_implement, False)
        assemble_state_transitions_and_boolean_conditions(self.robot_integrity, self.integrity_succeeded, self.robot.success_auxiliary_implement, True)
        assemble_state_transitions_and_boolean_conditions(self.robot_integrity, self.integrity_failed, self.robot.success_auxiliary_implement, False)
        assemble_state_transitions_and_always_true_conditions(self.instantiation_failed, self.end)

        condtion_to_home = assemble_state_transitions_and_timed_conditions(self.integrity_succeeded, self.home, 3.0)
        condition_to_start_shut_down = assemble_state_transitions_and_timed_conditions(self.instantiation_failed, self.shut_down_robot, 5.0)
        contidion_shut_down = assemble_state_transitions_and_timed_conditions(self.shut_down_robot, self.end, 3.0)
        
        self.integrity_succeeded.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(0,255,0)))
        self.integrity_succeeded.add_in_state_action(lambda: self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.BOTH, begin_on = True, cycle_duration = 1.0, total_duration = 3.0))
        self.integrity_succeeded.add_exiting_action(lambda: self.robot.state_machines["eye_blinkers"].turn_off(SideBlinkers.Side.BOTH))
        
        self.integrity_failed.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(255,0,0)))
        self.integrity_failed.add_in_state_action(lambda: self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.BOTH, begin_on = True, cycle_duration = 0.5, total_duration = 5.0))
        self.integrity_failed.add_in_state_action(lambda: self.robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.BOTH, begin_on = True, cycle_duration = 0.5, total_duration = 5.0))
        self.integrity_failed.add_exiting_action(lambda: self.robot.state_machines["led_blinkers"].turn_off(SideBlinkers.Side.BOTH))
        self.integrity_failed.add_exiting_action(lambda: self.robot.state_machines["eye_blinkers"].turn_off(SideBlinkers.Side.BOTH))
        
        
        self.shut_down_robot.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(255,255,0)))
        self.shut_down_robot.add_in_state_action(lambda: self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.BOTH, begin_on = True, cycle_duration = 0.75, total_duration = 3.0))
        self.shut_down_robot.add_in_state_action(lambda: self.robot.state_machines["led_blinkers"].blink(lambda: print(f'Starting process to shut down', end="\r")))
        self.shut_down_robot.add_exiting_action(lambda: self.robot.state_machines["eye_blinkers"].turn_off(SideBlinkers.Side.BOTH))
        self.end.add_in_state_action(lambda: print(f'The end', end="\r"))
        
        self.home.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(255,255,0)))
        self.home.add_in_state_action(lambda: self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, begin_on = True, cycle_duration = 1.5))
        
        self.layout = FiniteStateMachine.Layout()
        self.layout.add_states([self.robot_instantiation,self.robot_integrity,self.instantiation_failed,self.integrity_succeeded,self.integrity_failed,self.shut_down_robot,self.home,self.end])
        self.layout.initial_state = self.robot_instantiation
        app = FiniteStateMachine(layout=self.layout)
        app.current_applicative_state = self.robot_instantiation
        
    def start(self):
            self.robot.track()
        
if __name__ == '__main__':
    c64_project = C64Project()
    
    c64_project.robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)
    c64_project.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)

    c64_project.start()