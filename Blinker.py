
import time
from typing import Callable
from Condition import AlwaysTrueCondition, StateEntryDurationCondition
from finite_state_machine import FiniteStateMachine
from state import MonitoredState


class Blinker(FiniteStateMachine):
    
    StateGenerator = Callable[[], MonitoredState]
    
    def __init__(self, off_state_generator: StateGenerator, on_state_generator: StateGenerator) -> None:
        
        
        # Create states and their custom fields
        self.off = off_state_generator()
        self.off._FSM_BLINKER_ON_STATE = False
        
        self._do_in_state_action = lambda: ...
        
        self.on = on_state_generator()
        self.on._FSM_BLINKER_ON_STATE = True
        
        self.blink_begin = MonitoredState()
        self.blink_begin._FSM_BLINKER_ON_STATE = None
        
        # Create conditions
        #always_true = AlwaysTrueCondition(inverse=True)
        
        # Create transitions
        
        
        # Add transitions to states
        
        
        # Create layout
        layout = FiniteStateMachine.Layout()
    
        # Add states to layout
        layout.initial_state = self.off
        layout.add_states([self.off, self.on])    
        
        # Create FSM        
        super().__init__(layout=layout, unitialized=False)
        
    @property
    def is_on(self) -> bool:
        return self.current_state._FSM_BLINKER_ON_STATE is True
        
    
    @property
    def is_off(self) -> bool:
        return self.current_state._FSM_BLINKER_ON_STATE is False
    
    def turn_off(self):
       self.current_state = self.off
   
    def turn_on(self):
       self.current_state = self.on
       
    def blink(self, cycle_duration:float = 1.0, percent_on:float = 0.5, begin_on: bool = True):
        if cycle_duration <= 0:
            raise ValueError("cycle_duration must be greater than zero")
        if percent_on < 0 or percent_on > 1:
            raise ValueError("percent_on must be between 0 and 1")
        
        if begin_on:
            self.turn_on()
        else:
            self.turn_off()
            
        on_duration = cycle_duration * percent_on
        off_duration = cycle_duration - on_duration
        
        # blink until condition is reached or interrupted
        while self.current_state._FSM_BLINKER_ON_STATE is True:
            time.sleep(on_duration)
            self.turn_off()
            time.sleep(off_duration)
            self.turn_on()
        
        
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
    blinker.start()
    
    blinker.current_state = blinker.on
    start_time = time.perf_counter()
    
    while True == True:
        time.sleep(1)
        blinker.off
        time.sleep(1)
        blinker.on
    
    
    
   