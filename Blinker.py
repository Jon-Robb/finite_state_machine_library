
import time
from typing import Callable
from Condition import Condition, StateEntryDurationCondition, StateEntryCountCondition, AnyCondition, AlwaysTrueCondition
from finite_state_machine import FiniteStateMachine
from state import MonitoredState, State
from transition import ConditionalTransition, MonitoredTransition, Transition


def assemble_state_transitions_and_timed_conditions(starting_state: State, finishing_state: State, condition_duration:float=1.0 ) -> Condition :
    condition = StateEntryDurationCondition(condition_duration, starting_state)
    transition = MonitoredTransition(finishing_state, condition)
    starting_state.add_transition(transition)
    return condition 


class Blinker(FiniteStateMachine):
    
    StateGenerator = Callable[[], MonitoredState]
    
    def __init__(self, off_state_generator: StateGenerator, on_state_generator: StateGenerator):
        
        self.args_combinations = [
                                    {'end_off', 'total_duration', 'cycle_duration'},
                                    {'end_off', 'total_duration', 'n_cycles'},
                                    {'end_off', 'n_cycles', 'cycle_duration'}
                                    ]
        
        # self.off = assemble_state_transitions_and_conditions()
        # 1-Create states and their custom fields
        self.off = off_state_generator()
        self.off._FSM_BLINKER_ON_STATE = False
        self.off.add_in_state_action(lambda: print('In Blinker Off State'))
        
        self.on = on_state_generator()
        self.on._FSM_BLINKER_ON_STATE = True
        self.on.add_in_state_action(lambda: print('In Blinker On State'))

        self.blink_on = on_state_generator()
        self.blink_on._FSM_BLINKER_ON_STATE = True
        self.blink_on.add_in_state_action(lambda: print("Blink On"))

        self.blink_off = off_state_generator()
        self.blink_off._FSM_BLINKER_ON_STATE = False
        self.blink_off.add_in_state_action(lambda: print("Blink Off"))
        
        self.blink_begin = MonitoredState()
        self.blink_begin._FSM_BLINKER_ON_STATE = None
        
        self.blink_stop_begin = MonitoredState()
        self.blink_stop_begin._FSM_BLINKER_ON_STATE = None

        self.blink_stop_end = MonitoredState()
        self.blink_stop_end._FSM_BLINKER_ON_STATE = None
        
        self.off_duration = off_state_generator()
        self.off_duration._FSM_BLINKER_ON_STATE = False
        self.off_duration.add_in_state_action(lambda: print("In off duration"))
        
        self.on_duration = on_state_generator()
        self.on_duration._FSM_BLINKER_ON_STATE = True
        self.on_duration.add_in_state_action(lambda: print("In on duration"))
        
        self.blink_stop_off = off_state_generator()
        self.blink_stop_off._FSM_BLINKER_ON_STATE = False
        self.blink_stop_off.add_in_state_action(lambda: print("Blink Stop Off"))
        
        self.blink_stop_on = on_state_generator()
        self.blink_stop_on._FSM_BLINKER_ON_STATE = True
        self.blink_stop_on.add_in_state_action(lambda: print("Blink Stop On"))
        
      
        blink_stop_off_to_blink_stop_end_n_cycles_condition = StateEntryCountCondition(1.0, self.blink_stop_off)
        blink_stop_on_to_blink_stop_end_n_cycles_condition = StateEntryCountCondition(1.0, self.blink_stop_on)
        self.blink_stop_on_or_off_to_blink_stop_end_condition = AnyCondition()
        self.blink_stop_on_or_off_to_blink_stop_end_condition.add_condition(blink_stop_off_to_blink_stop_end_n_cycles_condition)
        self.blink_stop_on_or_off_to_blink_stop_end_condition.add_condition(blink_stop_on_to_blink_stop_end_n_cycles_condition)
        
        blink_stop_to_blink_stop_end_n_cycles = MonitoredTransition(self.blink_stop_end, self.blink_stop_on_or_off_to_blink_stop_end_condition)

        self.blink_stop_off.add_transition(blink_stop_to_blink_stop_end_n_cycles)
        self.blink_stop_on.add_transition(blink_stop_to_blink_stop_end_n_cycles)

    
        
        self.on_duration_condition = self.assemble_state_transitions_and_timed_conditions(self.on_duration, self.off_duration)
        self.off_duration_condition = self.assemble_state_transitions_and_timed_conditions(self.off_duration, self.on_duration)
    
        self.blink_off_condition = self.assemble_state_transitions_and_timed_conditions(self.blink_off, self.blink_on)
        self.blink_on_condition = self.assemble_state_transitions_and_timed_conditions(self.blink_on, self.blink_off)
    
        self.blink_stop_on_to_blink_stop_off_condition = self.assemble_state_transitions_and_timed_conditions(self.blink_stop_on, self.blink_stop_off)
        self.blink_stop_off_to_blink_stop_on_condition = self.assemble_state_transitions_and_timed_conditions(self.blink_stop_off, self.blink_stop_on)
        
        # self.blink_stop_on_or_off_to_blink_stop_end_condition = assemble_state_transitions_and_timed_conditions(self.blink_stop_off, self.blink_stop_end)
        # self.blink_stop_on_or_off_to_blink_stop_end_condition = assemble_state_transitions_and_timed_conditions(self.blink_stop_on, self.blink_stop_end)
        self.blink_stop_begin_total_duration_condition = self.assemble_state_transitions_and_timed_conditions(self.blink_stop_begin, self.blink_stop_end)


        # 5-Create layout
        layout = FiniteStateMachine.Layout()
    
        # 6-Add states to layout
        layout.initial_state = self.off
        layout.add_states([self.off, self.on, self.blink_begin, self.blink_on, self.blink_off, self.blink_stop_begin, self.blink_stop_end, self.blink_stop_off, self.blink_stop_on])
        
        # 7-Add the starting state
        self.current_state = layout.initial_state
        
        # Create FSM        
        super().__init__(layout=layout, unitialized=False)
        
    @property
    def is_on(self) -> bool:
        return self.current_state._FSM_BLINKER_ON_STATE is True
        
    @property
    def is_off(self) -> bool:
        return self.current_state._FSM_BLINKER_ON_STATE is False
    
    def turn_off(self, **kwargs):
        if kwargs.keys() == {'duration'}:
            self.off_duration_condition.duration = kwargs['duration']
            self.transit_to(self.off_duration)
        else:
            self.transit_to(self.off)
   
    def turn_on(self, **kwargs):
        if kwargs.keys() == {'duration'}:
            self.on_duration_condition.duration = kwargs['duration']
            self.transit_to(self.on_duration)
        else:
            self.transit_to(self.on)
       
    def blink(self, percent_on:float=0.5, begin_on:bool=True, **kwargs):
        
        # Arg checking and variable initialization
        if not isinstance(begin_on, bool):
            raise TypeError("begin_on must be a boolean")
        
        if percent_on < 0 or percent_on > 1:
            raise ValueError("percent_on must be between 0 and 1")
        
        if not isinstance(begin_on, bool):
            raise TypeError("begin_on must be a boolean")
        
        if kwargs.keys().__contains__('cycle_duration'):
            if kwargs['cycle_duration'] <= 0:
                raise ValueError("cycle_duration must be greater than zero")
            
        if kwargs.keys().__contains__('total_duration'):
            if kwargs['total_duration'] <= 0:
                raise ValueError("total_duration must be greater than zero")
            
        if kwargs.keys().__contains__('n_cycles'):
            if kwargs['n_cycles'] <= 0:
                raise ValueError("n_cycles must be greater than zero")
            
        if kwargs.keys().__contains__('end_off'):
            if not isinstance(kwargs['end_off'], bool):
                raise TypeError("end_off must be a boolean")
                                 
           
        # Overloads 
        if kwargs.keys() == {'cycle_duration'}:
            cycle_duration = kwargs['cycle_duration']

            self.blink_on_condition.duration = cycle_duration * percent_on
           
            self.blink_off_condition.duration = cycle_duration - self.blink_on_condition.duration
            
            if begin_on:
                self.transit_to(self.blink_on)
            else:
                self.transit_to(self.blink_off)
                
        elif kwargs.keys() in self.args_combinations:
            cycle_duration = None
            if kwargs.keys() == {'end_off', 'total_duration', 'cycle_duration'}:
                end_off, total_duration, cycle_duration = kwargs['end_off'], kwargs['total_duration'], kwargs['cycle_duration']
            elif kwargs.keys() == {'end_off', 'total_duration', 'n_cycles'}:
                end_off, total_duration, n_cycles = kwargs['end_off'], kwargs['total_duration'], kwargs['n_cycles']
                cycle_duration = total_duration / n_cycles
            elif kwargs.keys() == {'end_off', 'n_cycles', 'cycle_duration'}:
                end_off, n_cycles, cycle_duration = kwargs['end_off'], kwargs['n_cycles'], kwargs['cycle_duration']
                total_duration = n_cycles * cycle_duration
                
                
            self.blink_stop_on_to_blink_stop_off_condition.duration = cycle_duration * percent_on
            self.blink_stop_off_to_blink_stop_on_condition.duration = cycle_duration - self.blink_stop_on_to_blink_stop_off_condition.duration
            
            self.blink_stop_begin_total_duration_condition.duration = total_duration
            # TODO -> Demander au prof a propos de la logique du total duration 
            if begin_on:   
                self.blink_stop_begin.add_transition(ConditionalTransition(self.blink_stop_on, AlwaysTrueCondition()))
            else:
                self.blink_stop_begin.add_transition(ConditionalTransition(self.blink_stop_off, AlwaysTrueCondition()))
                
            if end_off:
                self.blink_stop_end.add_transition(ConditionalTransition(self.off, AlwaysTrueCondition()))
            else:
                self.blink_stop_end.add_transition(ConditionalTransition(self.on, AlwaysTrueCondition())) 
                
            self.transit_to(self.blink_stop_begin)

                    
        
if __name__ == "__main__":

    def off_state_generator():
        state = MonitoredState()
        state.add_in_state_action(lambda: print("Off"))
        return state
    
    def on_state_generator():
        state = MonitoredState()
        state.add_in_state_action(lambda: print("On"))
        return state
    
    blinker = Blinker(off_state_generator, on_state_generator)
    # blinker.blink(0.5, True, cycle_duration=1.0)
    blinker.blink( cycle_duration=10.0, percent_on=0.5, end_off=True, n_cycles=10)
    # blinker.turn_off(duration=2.0)
    for _ in range(10000000):
        blinker.track()
    
