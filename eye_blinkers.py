from side_blinkers import SideBlinkers
from state import MonitoredState
from Blinker import Blinker
from typing import TYPE_CHECKING
from functools import partial
from color import Color
import time
import math

class EyeBlinkers(SideBlinkers):
    def __init__(self, robot, left_color:tuple, right_color:tuple) -> None:
        
        if not isinstance(left_color, tuple) or not isinstance(right_color, tuple):
            raise TypeError("left_color and right_color must be tuples")
        
        if len(left_color) != 3 or len(right_color) != 3:
            raise ValueError("left_color and right_color must be tuples of length 3")
        
        self.__left_color = Color(left_color)
        self.__right_color = Color(right_color)
        self.__robot = robot
    
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
            def open_left_eye():

                robot.open_left_eye()
                
            state.add_entering_action(open_left_eye)
            return state
        
        def right_on_state_generator(self):
            state = MonitoredState()
            def open_right_eye():

                robot.open_right_eye()
                
            state.add_entering_action(open_right_eye) 
            return state
                
        super().__init__(left_off_state_generator, left_on_state_generator, right_off_state_generator, right_on_state_generator)
        
        
    def activate_gyros(self, cycle_duration:float):
        time_start = time.perf_counter()
        time_counter = 0

        while time_counter < cycle_duration:
            time_counter = time.perf_counter() - time_start
            sin_time = (math.sin(time_counter * math.tau) * 0.5) + 0.5
            color1 = self.right_color.blend(self.right_color.color_tuple, sin_time)
            self.left_color = color1
            color2 = self.left_color.blend(self.right_color.color_tuple, sin_time)
            self.right_color = color2
       
    @property
    def left_color(self) -> tuple:
        return self.__left_color
    
    @property
    def right_color(self) -> tuple:
        return self.__right_color
    
    @left_color.setter 
    def left_color(self, color: tuple) -> None:
        self.__left_color.color_tuple = color
        self.__robot.set_left_eye_color(color)
        self.__robot.open_left_eye()
        
    @right_color.setter 
    def right_color(self, color: tuple) -> None:
        self.__right_color.color_tuple = color
        self.__robot.set_right_eye_color(color)
        self.__robot.open_right_eye()
        
    def change_eyes_colors(self, both_colors: tuple=None ) -> None:
        if both_colors is None:
            raise ValueError("Must provide at least one color")

        if not isinstance(both_colors, tuple) :
            raise TypeError("left_color and right_color must be tuples")
    
        if len(both_colors) != 3:
            raise ValueError("left_color and right_color must be tuples of length 3")
        
        self.right_color = both_colors
        self.left_color = both_colors
