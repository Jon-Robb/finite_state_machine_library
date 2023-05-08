from side_blinkers import SideBlinkers
from state import MonitoredState
from Blinker import Blinker
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from robot import Robot
class EyeBlinkers(SideBlinkers):
    def __init__(self, robot: Robot, left_color:tuple, right_color:tuple) -> None:
        
        if not isinstance(left_color, tuple) or not isinstance(right_color, tuple):
            raise TypeError("left_color and right_color must be tuples")
        
        if len(left_color) != 3 or len(right_color) != 3:
            raise ValueError("left_color and right_color must be tuples of length 3")
        
        self.__left_color = left_color
        self.__right_color = right_color
    
        def left_off_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: self.robot.left_eye.off())
            
        def right_off_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: self.robot.right_eye.off())   
            
        def left_on_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: self.robot.left_eye.color(self.__left_color))
        
        def right_on_state_generator(self):
            state = MonitoredState()
            state.add_in_state_action(lambda: self.robot.right_eye.color(self.__right_color)) 
                
        super.__init__(left_off_state_generator, left_on_state_generator, right_off_state_generator, right_on_state_generator)
       
    @property
    def left_color(self) -> tuple:
        return self.__left_color
    @property
    def right_color(self) -> tuple:
        return self.__right_color
    
    @left_color.setter 
    def left_color(self, color: tuple) -> None:
        self.__left_color = color
        
    @right_color.setter 
    def right_color(self, color: tuple) -> None:
        self.__right_color = color
        
    def change_eye_colors(self, left_color:tuple=None, right_color:tuple=None, both_colors: tuple=None ) -> None:
        if left_color is None and right_color is None or both_colors is None:
            raise ValueError("Must provide at least one color")
        