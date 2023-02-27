from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from transition import Transition


class State:

    class Parameters:
        def __init__(self) -> None:
            self.terminal = False
            self.do_in_state_action_when_entering = False
            self.do_in_state_action_when_exiting = False

    def __init__(self, parameters:Parameters=Parameters()) -> None:
        pass

        self.__parameters = parameters
        self.__transition = []

    @property
    def is_valid(self) -> bool:
        all_transitions_are_valid = True
        for transition in self.__transition:
            if not transition.is_valid():
                all_transitions_are_valid = False
                break
        return len(self.__transition) > 0 and all_transitions_are_valid
    
    @property
    def is_terminal(self) -> bool:
        return self.__parameters.terminal

    @property
    def is_transiting(self)->"Transition":
        pass

    def add_transition(self, transition:"Transition")->None:
        if not isinstance(transition, Transition):
            raise TypeError("transition must be of type Transition")
        self.__transition.append(transition)
        
        
    def _exec_entering_action(self):
        print("_exec_entering_action")

    def _exec_in_state_action(self):
        print("_exec_in_state_action")
    
    def _exec_exiting_action(self):
        print("_exec_exiting_action")
    
    def _do_entering_action(self):
        print("_do_entering_action")

    def _do_in_state_action(self):
        print("_do_in_state_action")

    def _do_exiting_action(self):
        print("_do_exiting_action")


    