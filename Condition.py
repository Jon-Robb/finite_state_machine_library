from abc import ABC, abstractmethod

class Condition(ABC):
    def __init__(self, inverse=False):
        self.inverse = inverse
    
    @abstractmethod
    def _compare(self) -> bool:
        raise NotImplementedError("compare() not implemented")
    
    def __bool__(self) -> bool:
        return self._compare() ^ self.inverse
