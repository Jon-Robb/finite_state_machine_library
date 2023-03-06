from enum import Enum
from state import State
from transition import Transition

class FiniteStateMachine:
    """
    A class for modeling a finite state machine.

    Attributes:
    -----------
    layout : Layout
        The layout of the finite state machine, containing the states and initial state.
    uninitialized : bool, optional
        Whether the operational state of the finite state machine should start as uninitialized (True, default) or idle (False).

    Methods:
    --------
    current_operational_state() -> State:
        Returns the current operational state of the finite state machine.
    current_applicative_state() -> OperationalState:
        Returns the current applicative state of the finite state machine.
    current_operational_state(value: State) -> None:
        Sets the current operational state of the finite state machine to the given value.
    current_applicative_state(value: OperationalState) -> None:
        Sets the current applicative state of the finite state machine to the given value.
    reset() -> None:
        Resets the finite state machine.
    transit_to(state: State) -> None:
        Transitions the finite state machine to the given state.
    track() -> bool:
        Tracks the current state of the finite state machine.
    run(reset: bool = True, time_budget: float = None) -> None:
        Runs the finite state machine, optionally resetting it first and limiting the time budget for running.
    stop() -> None:
        Stops the finite state machine.

    Nested Classes:
    ---------------
    Layout:
        A class for defining the layout of the finite state machine.
    OperationalState (Enum):
        An enum class for defining the operational states of the finite state machine.
    """
    class Layout:
        """
        A class for defining the layout of the finite state machine.

        Attributes:
        -----------
        states : list[State]
            The list of states in the finite state machine.
        initial_state : State
            The initial state of the finite state machine.

        Methods:
        --------
        initial_state() -> State:
            Returns the initial state of the finite state machine.
        initial_state(state: State) -> None:
            Sets the initial state of the finite state machine to the given state.
        is_valid() -> bool:
            Returns True if the layout is valid, i.e. it contains all states and an initial state.
        add_state(state: State) -> None:
            Adds the given state to the list of states in the finite state machine.
        add_states(states: list[State]) -> None:
            Adds the given list of states to the list of states in the finite state machine.
        """
        def __init__(self) -> None:
            self.__states = []
            self.__initial_state = None
        
        @property
        def initial_state(self) -> State:
            """
            Returns the initial state of the finite state machine.
            """
            return self.__initial_state
        
        
        @initial_state.setter
        def initial_state(self, state:State) -> None:
            """
            Sets the initial state of the finite state machine to the given state.

            Parameters:
            -----------
            state : State
                The state to set as the initial state of the finite state machine.

            Raises:
            -------
            TypeError:
                If the given state is not of type State.
            """
            if not isinstance(state, State):
                raise TypeError("Initial state must be of type State")
            self.__initial_state = state
            
        @property
        def is_valid(self) -> bool:
            """
            Returns True if the layout is valid, i.e. it contains all states and an initial state.
            """
            return all(state.is_valid for state in self.__states) and self.__initial_state

    
        def add_state(self, state:State) -> None:
            """
            Adds the given state to the list of states in the finite state machine.

            Parameters:
            -----------
            state : State
                The state to add to the list of states in the finite state machine.

            Raises:
            -------
            TypeError:
                If the given state is not of type State.
            """
            if not isinstance(state, State):
                raise TypeError("State must be of type State")
            self.__states.append(state)
            
        def add_states(self, states:list[State]) -> None:
            """
            Adds the given list of states to the list of states in the finite state machine.

            Parameters:
            -----------
            states : list[State]
                The list of states to add to the list of states in the finite state machine.

            Raises:
            -------
            TypeError:
                If the given list of states is not of type list of State.
            """
            if not isinstance(states, list):
                raise TypeError("States must be of list of State objects")
            
            elif not all(isinstance(state, State) for state in states):
                raise TypeError("States must be of list of State objects")
            
            self.__states.extend(states)
   
    class OperationalState(Enum):
        """
        An enum class for defining the operational states of the finite state machine.

        Enum values:
        ------------
        UNITIALIZED = 0
            The operational state is uninitialized.
        IDLE = 1
            The operational state is idle.
        RUNNING = 2
            The operational state is running.
        TERMINAL_REACHED = 3
            The operational state has reached a terminal state.
        """
        UNITIALIZED = 0
        IDLE = 1
        RUNNING = 2
        TERMINAL_REACHED = 3
        
    def __init__(self, layout:Layout, unitialized:bool = True) -> None:
        """
        Initializes the FiniteStateMachine object.

        Parameters:
        -----------
        layout : Layout
            The layout of the finite state machine, containing the states and initial state.
        unitialized : bool, optional
            Whether the operational state of the finite state machine should start as uninitialized (True, default) or idle (False).

        Raises:
        -------
        TypeError:
            If the given layout is not of type Layout.
        """
        if not isinstance(layout, self.Layout):
            raise TypeError("Layout must be of type Layout")
        elif layout.is_valid is not True:
            raise Exception("Layout must be valid")
        
        self.__layout = layout
        self.__current_applicative_state = layout.initial_state
        self.__current_operational_state = FiniteStateMachine.OperationalState.UNITIALIZED if unitialized else FiniteStateMachine.OperationalState.IDLE
        
    @property
    def current_operational_state(self) -> "OperationalState":
        """
        Returns the current operational state of the finite state machine.
        """
        return self.__current_operational_state

    @property
    def current_applicative_state(self) -> State:
        """
        Returns the current applicative state of the finite state machine.
        """
        return self.__current_applicative_state

    @current_operational_state.setter
    def current_operational_state(self, value:"OperationalState") ->None:
        """
        Sets the current operational state of the finite state machine to the given value.

        Parameters:
        -----------
        value : OperationalState
            The state to set as the current applicative state of the finite state machine.
        

        Raises:
        -------
        TypeError:
            If the given value is not of type State.
        """
        if isinstance(value, self.OperationalState):
            self.__current_operational_state = value
        else:
            raise TypeError("value must be of type State")
            

    @current_applicative_state.setter
    def current_applicative_state(self, value:State):
        """Sets the current applicative state of the finite state machine to the given value.
        
        Parameters:
        -----------
        value : State
            The state to set as the current operational state of the finite state machine.

        Raises:
        -------
        TypeError:
            If the given value is not of type OperationalState.
        """
        if isinstance(value, State):
            self.__current_applicative_state = value
        else:
            raise TypeError("value must be of type OperationalState")

    def reset(self):
        """
        Resets the finite state machine.
        """
        self.__current_operational_state = self.OperationalState.IDLE
        pass

    def _transit_by(self, transition:Transition):
        """
        Transitions the finite state machine by the given transition.

        Parameters:
        -----------
        transition : Transition
            The transition by which to transition the finite state machine.
        """
        self.current_applicative_state._exec_exiting_action()
        transition._exec_transiting_action()
        self.current_applicative_state._exec_entering_action()

    def transit_to(self, state:State):
        """
        Transitions the finite state machine to the given state.

        Parameters:
        -----------
        state : State
            The state to transition to.

        Raises:
        -------
        TypeError:
            If the given state is not of type State.
        """
        pass

    def track(self)-> bool:
        """
        Tracks the current state of the finite state machine.

        Returns:
        --------
        bool:
            Whether the current state is a terminal state or not.
        """
        use_transition = self.__current_applicative_state.is_transiting
        if isinstance(use_transition, Transition):
            self._transit_by(use_transition)
            
        else:
            self.current_applicative_state._exec_in_state_action()
        
        next_state_valid = self.__current_applicative_state.is_valid
        if not next_state_valid:
            self.__current_operational_state = self.OperationalState.TERMINAL_REACHED
        return next_state_valid

    def run(self, reset:bool = True, time_budget:float = None):
        """
        Runs the finite state machine, optionally resetting it first and limiting the time budget for running.

        Parameters:
        -----------
        reset : bool, optional
            Whether to reset the finite state machine before running (True, default) or not (False).
        time_budget : float, optional
            The maximum time (in seconds) for which to run the finite state machine. If None (default), there is no time limit.
        """
        print("Enweille roule mon esti!")

    def stop(self):
        """
        Stops the finite state machine.
        """
        pass