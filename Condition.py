import time
from abc import ABC, abstractmethod

from state import MonitoredState

class Condition(ABC):
    def __init__(self, inverse:bool=False):
        self.inverse = inverse
    
    @abstractmethod
    def _compare(self) -> bool:
        raise NotImplementedError("compare() not implemented")
    
    def __bool__(self) -> bool:
        return self._compare() ^ self.inverse


class ManyConditions(Condition):
    def __init__(self, inverse:bool=False):
        super().__init__(inverse)
        self._conditions = []

    def add_condition(self, condition:Condition):
        self._conditions.append(condition)

    def add_conditions(self, conditions):
        for condition in conditions:
            self._conditions.append(condition)
        
class AllCondition(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)

    def _compare(self)->bool:
        return all(bool(condition) for condition in self._conditions)
        
class NoneCondition(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
        
    def _compare(self)->bool:
        return not any(bool(condition) for condition in self._conditions)

class AnyCondition(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
        
    def _compare(self)->bool:
        return any(bool(condition) for condition in self._conditions)

class AlwaysTrueCondition(Condition):
    def __init__(self, inverse:bool=False):
        super().__init__(inverse)
        
    def _compare(self) -> bool:
        return True

class ValueCondition(Condition):
    def __init__(self, initial_value: any, expected_value: any, inverse:bool=False):
        super().__init__(inverse)
        self.value = initial_value
        self.expected_value = expected_value

    def _compare(self) -> bool:
        return self.value == self.expected_value

class TimedCondition(Condition):
    def __init__(self, duration:float, time_reference:float=None, inverse:bool=False):
        super().__init__(inverse)
        self.__counter_duration = duration
        self.__counter_reference = time_reference if time_reference is not None else time.perf_counter()
        
    def _compare(self) -> bool:
        return  time.perf_counter() - self.__counter_reference  >= self.__counter_duration 

    @property
    def duration(self)->float:
        return self.__counter_duration

    @duration.setter
    def duration(self, duration:float)->None:
        self.__counter_duration = duration

    def reset(self) -> None:
        self.__counter_reference = time.perf_counter()


class MonitoredStateCondition(Condition):
    def __init__(self, monitored_state:"MonitoredState", inverse:bool=False):
        super().__init__(inverse)
        self._monitored_state = monitored_state

    @property
    def monitored_state(self)->"MonitoredState":
        return self._monitored_state
    
    
    @monitored_state.setter
    def monitored_state(self, monitored_state:"MonitoredState")->None:
        if not isinstance(monitored_state, MonitoredState):
            raise TypeError("monitored_state must be of type MonitoredState")
        self._monitored_state = monitored_state
    

class StateEntryDurationCondition(MonitoredStateCondition):
    def __init__(self, duration:float, monitored_state:"MonitoredState", inverse:bool=False):
        super().__init__(monitored_state, inverse)
        if not isinstance(duration, float):
            raise TypeError("duration must be of type float")
        self.__duration = duration
        
    @property
    def duration(self)->float:
        return self.__duration
    
    @duration.setter
    def duration(self, duration:float)->None:
        if not isinstance(duration, float):
            raise TypeError("duration must be of type float")
        self.__duration = duration
        
    def _compare(self)->bool:
        return time.perf_counter() - self.monitored_state.last_entry_time >= self.duration    


class StateEntryCountCondition(MonitoredStateCondition):
    def __init__(self, expected_count:int, monitored_state:"MonitoredState", auto_reset:bool = True, inverse:bool=False):
        super().__init__(monitored_state, inverse)
    
        self.__ref_count = expected_count
        self.__expected_count = expected_count
        self.__auto_reset = auto_reset
        
        @property
        def expected_count(self)->int:
            return self.__expected_count
        
        @expected_count.setter
        def expected_count(self, expected_count:int)->None:
            if not isinstance(expected_count, int):
                raise TypeError("expected_count must be of type int")
            self.__expected_count = expected_count
            
        
    def _compare(self)->bool:
        if self.monitored_state.entry_count >= self.__ref_count:
            if self.__auto_reset:
                self.reset_count()
            return True
        return False


    def reset_count(self):
        self.__ref_count += self.__expected_count
   
   
class StateValueCondition(MonitoredStateCondition):
    def __init__(self, expected_value: any, monitored_state:"MonitoredState", inverse:bool=False):
        super().__init__(monitored_state, inverse)
        self.expected_value = expected_value
        
    def _compare(self)->bool:
        return self.monitored_state.value == self.expected_value
    
class RemoteValueCondition(Condition):
    def __init__(self, remote, expected_input, inverse=False):
        super().__init__(inverse=inverse)
        self.remote = remote
        self.expected_input = expected_input
        self.last_input = None
        
    def _compare(self) -> bool:
        current_input = self.remote.read()
        # if self.last_input != current_input:
        print(current_input)
            # self.last_input = current_input
        return current_input == self.expected_input
        # return False