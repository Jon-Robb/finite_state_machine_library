from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from Condition import Condition
if TYPE_CHECKING:
    from state import State

class Transition(ABC):
    def __init__(self, next_state:"State"=None) -> None:
        self.__next_state = next_state

    @property
    def next_state(self)->"State":
        return self.__next_state

    @property
    def is_valid(self)-> bool:
        return self.__next_state is not None
    
    @next_state.setter
    def next_state(self, state:"State")->None:
        if not isinstance(state, "State"):
            raise TypeError("Next state must be of type State")
        self.__next_state = state
    
    @property
    @abstractmethod    
    def is_transiting (self)->bool:
        raise NotImplementedError("is_transiting must be implemented")
    
    def _exec_transiting_action(self):
        self._do_transiting_action()
    
    def _do_transiting_action(self):
        pass

class ConditionalTransition(Transition):
    def __init__(self, condition:Condition=None) -> None:
        super().__init__(next_state)
        self.__condition = condition
        

class ActionTransition(ConditionalTransition):
    def __init__(self, next_state:"State"=None) -> None:
        super().__init__(next_state)
        self.__transiting_action = []
        
    def _do_transiting_action(self) -> None:
        pass
    
    def add_transiting_action(self, action:callable) -> None:
        if action() is not None:
            raise Exception("Callable must return None")
        self.__transiting_action.append(action)
        
        
class MonitoredTransition(ActionTransition):
    def __init__(self, next_state:"State"=None) -> None:
        super().__init__(next_state)
        
        self.__transit_count = 0
        self.__last_transit_time = 0
        self.custom = None
        
    @property
    def transit_count(self)->int:
        return self.__transit_count

    @property
    def last_transit_time(self)->float:
        return self.__last_transit_time
    
    def reset_transit_count(self):
        self.__transit_count = 0
        
    def reset_last_transit_time(self):
        self.__last_transit_time = 0
        
    def _exec_transiting_action(self):
        return super()._exec_transiting_action()
        