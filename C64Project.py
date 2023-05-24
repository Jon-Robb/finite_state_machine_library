from robot import Robot
from side_blinkers import SideBlinkers
from finite_state_machine import FiniteStateMachine
from state import MonitoredState, State
from assembling_functions import assemble_state_transitions_and_always_true_conditions, assemble_state_transitions_and_boolean_conditions,assemble_state_transitions_and_timed_conditions, assemble_state_transitions_and_remote_value_conditions
from state import RobotState, FSMState



class C64Project(FiniteStateMachine):            
    def __init__(self):
        self.robot = Robot()
        
        # 1- Create states
        self.robot_instantiation = RobotState(self.robot)
        self.robot_integrity = RobotState(self.robot)
        
        self.instantiation_failed = RobotState(self.robot)
        self.integrity_succeeded = RobotState(self.robot)
        self.integrity_failed = RobotState(self.robot)
        self.shut_down_robot = RobotState(self.robot)
        self.home = RobotState(self.robot)
        self.task_one_manual_control = FSMState(self.robot, self.robot.state_machines["manual_control"])
        self.task_two_distance_color = FSMState(self.robot, self.robot.state_machines["distance_color"])
        
        parametre = State.Parameters()
        parametre.terminal = True
        
        self.end = RobotState(robot = self.robot, parameters=parametre)
        
        # TODO : Keep working on the layout
        assemble_state_transitions_and_boolean_conditions(self.robot_instantiation, self.robot_integrity, self.robot.success_brain_implement, True)
        assemble_state_transitions_and_boolean_conditions(self.robot_instantiation, self.instantiation_failed, self.robot.success_brain_implement, False)
        assemble_state_transitions_and_boolean_conditions(self.robot_integrity, self.integrity_succeeded, self.robot.success_auxiliary_implement, True)
        assemble_state_transitions_and_boolean_conditions(self.robot_integrity, self.integrity_failed, self.robot.success_auxiliary_implement, False)
        assemble_state_transitions_and_always_true_conditions(self.instantiation_failed, self.end)

        assemble_state_transitions_and_timed_conditions(self.integrity_succeeded, self.home, 3.0)
        assemble_state_transitions_and_timed_conditions(self.instantiation_failed, self.shut_down_robot, 5.0)
        assemble_state_transitions_and_timed_conditions(self.shut_down_robot, self.end, 3.0)
        
        assemble_state_transitions_and_remote_value_conditions(self.home, self.task_one_manual_control, self.robot.remote, 6)
        assemble_state_transitions_and_remote_value_conditions(self.home, self.task_two_distance_color, self.robot.remote, 7)
        assemble_state_transitions_and_remote_value_conditions(self.task_one_manual_control, self.home, self.robot.remote, 3)
        assemble_state_transitions_and_remote_value_conditions(self.task_two_distance_color, self.home, self.robot.remote, 3)
        assemble_state_transitions_and_remote_value_conditions(self.home, self.shut_down_robot, self.robot.remote, 3, True)
        
        
        self.integrity_succeeded.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(0,255,0)))
        self.integrity_succeeded.add_entering_action(lambda: print('integrity succeeded'))
        self.integrity_succeeded.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.BOTH, begin_on = True, cycle_duration = 1.0, total_duration = 3.0))
        self.integrity_succeeded.add_exiting_action(lambda: self.robot.state_machines["eye_blinkers"].turn_off(SideBlinkers.Side.BOTH))

        self.integrity_failed.add_entering_action(lambda: print('integrity failed'))
        self.integrity_failed.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(255,0,0)))
        self.integrity_failed.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.BOTH, begin_on = True, cycle_duration = 0.5, total_duration = 5.0))
        self.integrity_failed.add_entering_action(lambda: self.robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.BOTH, begin_on = True, cycle_duration = 0.5, total_duration = 5.0))
        self.integrity_failed.add_exiting_action(lambda: self.robot.state_machines["led_blinkers"].turn_off(SideBlinkers.Side.BOTH))
        self.integrity_failed.add_exiting_action(lambda: self.robot.state_machines["eye_blinkers"].turn_off(SideBlinkers.Side.BOTH))
        
        self.shut_down_robot.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(255,255,0)))
        self.shut_down_robot.add_entering_action(lambda: print(f'Starting process to shut down'))
        self.shut_down_robot.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.BOTH, begin_on = True, cycle_duration = 0.75, total_duration = 3.0))
        self.end.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].turn_off(SideBlinkers.Side.BOTH))
        self.end.add_entering_action(lambda: print(f'The end', end="\r"))
        self.end.add_in_state_action(lambda: exit())
        
        self.home.add_entering_action(lambda: print('home'))
        self.home.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].change_eyes_colors(both_colors=(255,255,0)))
        self.home.add_entering_action(lambda: self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, begin_on = True, cycle_duration = 1.5))
        self.home.add_exiting_action(lambda: self.robot.state_machines["eye_blinkers"].turn_off(SideBlinkers.Side.BOTH))
        
        self.home.add_in_state_action(self.robot.track)
        self.task_one_manual_control.add_entering_action(self.enter_manual_control)
        self.task_one_manual_control.add_in_state_action(self.robot.track)
        self.task_two_distance_color.add_in_state_action(self.robot.track)
        self.shut_down_robot.add_in_state_action(self.robot.track)
        
        self.layout = FiniteStateMachine.Layout()
        self.layout.add_states([self.robot_instantiation,self.robot_integrity,self.instantiation_failed,self.integrity_succeeded,self.integrity_failed,self.shut_down_robot,self.home,self.end])
        self.layout.initial_state = self.robot_instantiation
        # app = FiniteStateMachine(layout=self.layout)
        # app.current_applicative_state = self.robot_instantiation
        
        super().__init__(layout=self.layout)
        self.current_applicative_state = self.robot_instantiation

        
    def enter_manual_control(self):
        self.robot.state_machines["eye_blinkers"].left_color = (255, 0, 0)
        self.robot.state_machines["eye_blinkers"].right_color = (0, 0, 255)
        self.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.RIGHT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)
        # self.robot.state_machines["eye_blinkers"].activate_gyros(cycle_duration = 0.5)

    def start(self):
        while True:
            self.track()
        
if __name__ == '__main__':
    c64_project = C64Project()
    
    # c64_project.robot.state_machines["led_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)
    # c64_project.robot.state_machines["eye_blinkers"].blink(SideBlinkers.Side.LEFT_RECIPROCAL, percent_on = 0.5, begin_on = True, cycle_duration = 0.5)

    c64_project.start()