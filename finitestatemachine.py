from enum import Enum
from state import State
from transition import Transition



class FiniteStateMachine:
    
    class Layout:
        def __init__(self) -> None:
            self.__states = []
            self.__initial_state = None
        
        @property
        def initial_state(self) -> State:
            return self.__initial_state
        
        @initial_state.setter
        def initial_state(self, state:State) -> None:
            if not isinstance(state, State):
                raise TypeError("Initial state must be of type State")
            self.__initial_state = state
            
        @property
        def is_valid(self) -> bool:
            return all(self.__states) and self.initial_state

        
        def add_state(self, state:State):
            if not isinstance(state, State):
                raise TypeError("State must be of type State")
            self.__states.append(state)
            
        def add_states(self, states:list[State]):
            if not isinstance (states, list[State]):
                raise TypeError("States must be of type list of State")
            self.__states.extend(states)
       
    class OperationalState(Enum):
        UNITIALIZED = 0
        IDLE = 1
        RUNNING = 2
        TERMINAL_REACHED = 3
        
    def __init__(self, layout:"Layout", unitialized:bool = True) -> None:
        if not isinstance(layout, self.Layout):
            raise TypeError("Layout must be of type Layout")
        
        self.__layout = layout
        self.__current_applicative_state = None # Va venir de layout
        self.__current_operational_state = FiniteStateMachine.OperationalState.UNITIALIZED if unitialized else FiniteStateMachine.OperationalState.IDLE
        
    @property
    def current_operational_state(self) -> "State":
        return self.__current_operational_state
    
    @property
    def current_applicative_state(self) -> "OperationalState":
        return self.__current_applicative_state

    @current_operational_state.setter
    def current_operational_state(self, value:"State") ->None:
        if isinstance(value, State):
            self.__current_operational_state = value
        else:
            raise TypeError("value must be of type State")
            

    @current_applicative_state.setter
    def current_applicative_state(self, value:"OperationalState"):
        if isinstance(value, self.OperationalState):
            self.__current_applicative_state = value
        else:
            # raise TypeError("Veuillez insérer un objet de type OperationalState")
            raise TypeError("value must be of type OperationalState")

    def reset(self):
        pass

    def _transit_by(self, transition:Transition):
        pass

    def transit_to(self, state:State):
        pass
    
    def track(self)-> bool:
        pass
    
    def run(self, reset:bool = True, time_budget:float = None):
        print("Enweille roule mon esti!")
    
    def stop(self):
        pass
    
    
    
    



                
    
    
    
