from abc import ABC, abstractmethod

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
        pass
        
        
class NoneCondition(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
        
    def _compare(self)->bool:
        pass

class AnyCondition(ManyConditions):
    def __init__(self, inverse: bool = False):
        super().__init__(inverse)
        
    def _compare(self)->bool:
        pass






class AlwaysTrueCondition(Condition):
    def __init__(self, inverse:bool=False):
        super().__init__(inverse)
        
    def _compare(self) -> bool:
        return super()._compare()





 