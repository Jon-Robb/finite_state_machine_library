from Blinker import Blinker
from enum import Enum

from state import MonitoredState

class SideBlinkers:
    
    class Side(Enum):
        LEFT = 0
        RIGHT = 1
        BOTH = 2
        LEFT_RECIPROCAL = 3
        RIGHT_RECIPROCAL = 4

    def __init__(self, left_off_state_generator: Blinker.StateGenerator, left_on_state_generator: Blinker.StateGenerator, right_off_state_generator: Blinker.StateGenerator, right_on_state_generator: Blinker.StateGenerator):
        self.left_blinker = Blinker(left_off_state_generator, left_on_state_generator)
        self.right_blinker = Blinker(right_off_state_generator, right_on_state_generator)
    
    def is_off(self, side: Side):
        if side == self.Side.LEFT:
            return self.left_blinker.is_off()
        elif side == self.Side.RIGHT:
            return self.right_blinker.is_off()
        elif side == self.Side.BOTH:
            return self.left_blinker.is_off() and self.right_blinker.is_off()
        else:
            raise Exception('Side must be LEFT or RIGHT')
        
    def is_on(self, side: Side):
        if side == self.Side.LEFT:
            return self.left_blinker.is_on()
        elif side == self.Side.RIGHT:
            return self.right_blinker.is_on()
        elif side == self.Side.BOTH:
            return self.left_blinker.is_on() and self.right_blinker.is_on()
        else:
            raise Exception('Side must be LEFT or RIGHT')
        
    def turn_on(self, side: Side):
        if side == self.Side.LEFT:
            self.left_blinker.turn_on()
        elif side == self.Side.RIGHT:
            self.right_blinker.turn_on()
        elif side == self.Side.BOTH:
            self.left_blinker.turn_on()
            self.right_blinker.turn_on()
        elif side == self.Side.LEFT_RECIPROCAL:
            self.left_blinker.turn_on()
            self.right_blinker.turn_off()
        elif side == self.Side.RIGHT_RECIPROCAL:
            self.left_blinker.turn_off()
            self.right_blinker.turn_on()
        else:
            raise Exception("Side must be LEFT, RIGHT, LEFT_RECIPROCAL, or RIGHT_RECIPROCAL")
        
    def turn_off(self, side: Side, **kwargs):
        if side == self.Side.LEFT:
            self.left_blinker.turn_off(**kwargs)
        elif side == self.Side.RIGHT:
            self.right_blinker.turn_off(**kwargs)
        elif side == self.Side.BOTH:
            self.left_blinker.turn_off(**kwargs)
            self.right_blinker.turn_off(**kwargs)
        elif side == self.Side.LEFT_RECIPROCAL:
            self.left_blinker.turn_off(**kwargs)
            self.right_blinker.turn_on(**kwargs)
        elif side == self.Side.RIGHT_RECIPROCAL:
            self.left_blinker.turn_on(**kwargs)
            self.right_blinker.turn_off(**kwargs)
        else:
            raise Exception("Side must be LEFT, RIGHT, LEFT_RECIPROCAL, or RIGHT_RECIPROCAL")
        
    def blink(self, side: Side, **kwargs):
        if side == self.Side.LEFT:
            self.left_blinker.blink(**kwargs)
        elif side == self.Side.RIGHT:
            self.right_blinker.blink(**kwargs)
        elif side == self.Side.BOTH:
            self.left_blinker.blink(**kwargs)
            self.right_blinker.blink(**kwargs)
        elif side == self.Side.LEFT_RECIPROCAL:
            self.left_blinker.blink(**kwargs)
            kwargs.set("begin_on", not kwargs.get("begin_on"))
            self.right_blinker.blink(**kwargs)
        elif side == self.Side.RIGHT_RECIPROCAL:
            self.right_blinker.blink(**kwargs)
            kwargs.set("begin_on", not kwargs.get("begin_on"))
            self.left_blinker.blink(**kwargs)
        else:
            raise Exception("Side must be LEFT, RIGHT, LEFT_RECIPROCAL, or RIGHT_RECIPROCAL")
        

    def track(self):
        self.left_blinker.track()
        self.right_blinker.track()
        
if __name__ == "__main__":
    

    def off_state_generator_left():
        state = MonitoredState()
        state.add_in_state_action(lambda: print("OFF state LEFT"))
        return state
        
    def on_state_generator_left():
        state = MonitoredState()
        state.add_in_state_action(lambda: print("ON state LEFT"))
        return state


    def off_state_generator_right():
        state = MonitoredState()
        state.add_in_state_action(lambda: print("OFF state right"))
        return state
        
    def on_state_generator_right():
        state = MonitoredState()
        state.add_in_state_action(lambda: print("ON state right"))
        return state

    side_blinkers = SideBlinkers(off_state_generator_left, on_state_generator_left, off_state_generator_right, on_state_generator_right)
    
    side_blinkers.turn_on(SideBlinkers.Side.LEFT)
    side_blinkers.turn_off(SideBlinkers.Side.RIGHT)
    
    side_blinkers.blink(SideBlinkers.Side.LEFT, begin_on=True, n_cycles=5, cycle_duration=0.5, percent_on=0.3)
    side_blinkers.blink(SideBlinkers.Side.RIGHT, begin_on=True, n_cycles=10, total_duration=10.0, percent_on=0.7)
    
    for _ in range(1000000):
        side_blinkers.track()
