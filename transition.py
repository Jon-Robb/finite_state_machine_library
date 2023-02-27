from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from state import State

class Transition:
    def __init__(self, next_state:"State"=None) -> None:
        self.__next_state = next_state

    @property
    def next_state(self)->"State":
        return self.__next_state

    @property
    def is_valid(self)-> bool:
        return self.next_state.is_valid
    
    @next_state.setter
    def next_state(self, state:"State")->None:
        if not isinstance(state, "State"):
            raise TypeError("Next state must be of type State")
        self.__next_state = state
        
    @property
    def is_transiting (self)->bool:
        return self.next_state.is_transiting
    
    def _exec_transiting_action(self):
        print("Transition._exec_transiting_action")
    
    def _do_transiting_action(self):
        print("Transition._do_transiting_action")