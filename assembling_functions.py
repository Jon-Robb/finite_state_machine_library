from Condition import Condition, StateEntryDurationCondition, ValueCondition, AlwaysTrueCondition, RemoteValueCondition, BetweenConditionRangeFinder
from finite_state_machine import FiniteStateMachine
from state import MonitoredState, State
from transition import ConditionalTransition, MonitoredTransition, Transition

def assemble_state_transitions_and_timed_conditions(starting_state: State, finishing_state: State, condition_duration:float=1.0 ) -> Condition :
    condition = StateEntryDurationCondition(condition_duration, starting_state)
    transition = MonitoredTransition(finishing_state, condition)
    starting_state.add_transition(transition)
    return condition 

def assemble_state_transitions_and_boolean_conditions(starting_state: State, finishing_state: State, start_value:bool, wanted_value_condition=True) -> Condition :
    condition = ValueCondition(start_value, wanted_value_condition)
    transition = MonitoredTransition(finishing_state, condition)
    starting_state.add_transition(transition)
    return condition

def assemble_state_transitions_and_always_true_conditions(starting_state: State, finishing_state: State) -> Condition :
    condition = AlwaysTrueCondition()
    transition = MonitoredTransition(finishing_state, condition)
    starting_state.add_transition(transition)
    return condition

def assemble_state_transitions_and_remote_value_conditions(starting_state: State, finishing_state, remote, remote_input:int, single_input=False) -> Condition:
    condition = RemoteValueCondition(remote, remote_input, single_input=single_input)
    transition = MonitoredTransition(finishing_state, condition)
    starting_state.add_transition(transition)
    return condition

def assemble_state_transitions_and_between_condition(starting_state: State, finishing_state:State, min_value:int, max_value:int, range_finder):
    condition = BetweenConditionRangeFinder(range_finder,min_value, max_value )
    transition = MonitoredTransition(finishing_state, condition)
    starting_state.add_transition(transition)
    return condition