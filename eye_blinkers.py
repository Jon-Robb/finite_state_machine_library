from side_blinkers import SideBlinkers
from state import MonitoredState
from Blinker import Blinker
from typing import TYPE_CHECKING
from functools import partial
from color import Color

class EyeBlinkers(SideBlinkers):
    def __init__(self, robot, left_color:tuple, right_color:tuple) -> None:
        
        if not isinstance(left_color, tuple) or not isinstance(right_color, tuple):
            raise TypeError("left_color and right_color must be tuples")
        
        if len(left_color) != 3 or len(right_color) != 3:
            raise ValueError("left_color and right_color must be tuples of length 3")
        
        self.__left_color = Color(left_color[0], left_color[1], left_color[2])
        self.__right_color = Color(right_color[0], right_color[1], right_color[2])
    
        def left_off_state_generator(self):
            state = MonitoredState()
        
            state.add_entering_action(lambda: robot.close_left_eye())
            return state
            
        def right_off_state_generator(self):
            state = MonitoredState()
            state.add_entering_action(lambda: robot.close_right_eye())   
            return state

            
        def left_on_state_generator(self):
            state = MonitoredState()
            def open_left_eye(color):
                robot.set_left_eye_color(Color(color[0], color[1], color[2]))
                robot.open_left_eye()
                
            state.add_entering_action(partial(open_left_eye, left_color))
            return state
        
        def right_on_state_generator(self):
            state = MonitoredState()
            def open_right_eye(color):
                robot.set_right_eye_color(right_color((color[0], color[1], color[2])))
                robot.open_right_eye()
                
            state.add_entering_action(partial(open_right_eye, right_color)) 
            return state
                
        super().__init__(left_off_state_generator, left_on_state_generator, right_off_state_generator, right_on_state_generator)
       
    @property
    def left_color(self) -> tuple:
        return self.__left_color
    @property
    def right_color(self) -> tuple:
        return self.__right_color
    
    @left_color.setter 
    def left_color(self, color: tuple) -> None:
        self.__left_color(color[0], color[1], color[2])
        
    @right_color.setter 
    def right_color(self, color: tuple) -> None:
        self.__right_color(color[0], color[1], color[2])
        
    def change_eyes_colors(self, both_colors: tuple=None ) -> None:
        if both_colors is None:
            raise ValueError("Must provide at least one color")

        if not isinstance(both_colors, tuple) :
            raise TypeError("left_color and right_color must be tuples")
    
        if len(both_colors) != 3:
            raise ValueError("left_color and right_color must be tuples of length 3")
        
        self.right_color(both_colors[0], both_colors[1], both_colors[2])
        self.left_color(both_colors[0], both_colors[1], both_colors[2])