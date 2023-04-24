
import time
from typing import Callable
from Condition import AlwaysTrueCondition, StateEntryDurationCondition
from finite_state_machine import FiniteStateMachine
from state import MonitoredState
from transition import MonitoredTransition


class Blinker(FiniteStateMachine):
    
    StateGenerator = Callable[[], MonitoredState]
    
    def __init__(self, off_state_generator: StateGenerator, on_state_generator: StateGenerator) -> None:
        
        
        # Create states and their custom fields
        self.off = off_state_generator()
        self.off._FSM_BLINKER_ON_STATE = False
        self.off._do_in_state_action = lambda: print('In Blinker Off State')
        
        self.on = on_state_generator()
        self.on._FSM_BLINKER_ON_STATE = True
        self.on._do_in_state_action = lambda: print('In Blinker On State')
        
        self.blink_on = on_state_generator()
        self.blink_on._FSM_BLINKER_ON_STATE = True
        self.blink_on._do_in_state_action = lambda: print("Blink On")

        self.blink_off = off_state_generator()
        self.blink_off._FSM_BLINKER_ON_STATE = False
        self.blink_off._do_in_state_action = lambda: print("Blink Off")
        
        self.blink_begin = on_state_generator()
        self.blink_begin._FSM_BLINKER_ON_STATE = None
        
        # Create conditions
        self.blink_on_condition = StateEntryDurationCondition(1.0, self.blink_on)
        self.blink_off_condition = StateEntryDurationCondition(1.0, self.blink_off)
    
        # Create transitions
        blink_on_to_blink_off = MonitoredTransition(self.blink_off, self.blink_on_condition)
        blink_off_to_blink_on = MonitoredTransition(self.blink_on, self.blink_off_condition)
        
        # Add transitions to states
        self.blink_on.add_transition(blink_on_to_blink_off)
        self.blink_off.add_transition(blink_off_to_blink_on)
        
        # Create layout
        layout = FiniteStateMachine.Layout()
    
        # Add states to layout
        layout.initial_state = self.off
        layout.add_states([self.off, self.on, self.blink_begin, self.blink_on, self.blink_off])
        
        # Add the starting state
        self.current_state = layout.initial_state
        
        # Create FSM        
        super().__init__(layout=layout, unitialized=False)
        
    @property
    def is_on(self) -> bool:
        return self.current_state._FSM_BLINKER_ON_STATE is True
        
    
    @property
    def is_off(self) -> bool:
        return self.current_state._FSM_BLINKER_ON_STATE is False
    
    def turn_off(self):
        self.transit_to(self.off)
    #    self.current_state = self.off
   
    def turn_on(self):
       self.transit_to(self.on)
       
    def blink(self, cycle_duration:float = 1.0, percent_on:float = 0.5, begin_on: bool = True):
        if cycle_duration <= 0:
            raise ValueError("cycle_duration must be greater than zero")
        if percent_on < 0 or percent_on > 1:
            raise ValueError("percent_on must be between 0 and 1")
        
        self.blink_on_condition.duration = cycle_duration * percent_on
        self.blink_off_condition.duration = cycle_duration - self.blink_on_condition.duration
        
        if begin_on:
            self.transit_to(self.blink_on)
        else:
            self.transit_to(self.blink_off)

        
if __name__ == "__main__":
    
    def off_state_generator():
        state = MonitoredState()
        state.add_entering_action(lambda: print("Off"))
        return state
    
    def on_state_generator():
        state = MonitoredState()
        state.add_entering_action(lambda: print("On"))   
        return state
    
    blinker = Blinker(off_state_generator, on_state_generator)
    blinker.blink(1.0, 0.9, True)
    for _ in range(2346346364):
        blinker.track()
    
   