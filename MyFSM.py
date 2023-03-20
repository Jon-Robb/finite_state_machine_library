from finite_state_machine import FiniteStateMachine
from finite_state_machine import State
from transition import Transition
class TransitionSubClass(Transition):
    def __init__(self, next_state: "State" = None) -> None:
        super().__init__(next_state)
        self.count = 0 
    
    @property
    def is_transiting(self) -> bool:
        self.count += 1
        return self.count % 2 == 1

class MyFSM(FiniteStateMachine):
    def __init__(self):
        
        state1 = State()
        state2 = State()
        state3 = State()
        state4 = State()
        
        transition1 = TransitionSubClass(state2)
        transition2 = TransitionSubClass(state3)
        transition3 = TransitionSubClass(state4)
        transition4 = TransitionSubClass(state1)
        
        state1.add_transition(transition1)
        state2.add_transition(transition2)
        state3.add_transition(transition3)
        state4.add_transition(transition4)
        
        layout = FiniteStateMachine.Layout()
        
        layout.initial_state = state1
        
        layout.add_states([layout.initial_state, state2, state3, state4])
        
        super().__init__(layout)
        