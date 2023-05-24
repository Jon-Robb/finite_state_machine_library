
#if TYPE_CHECKING:
import time
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from transition import Transition


class State:
    """
    A class for defining a state in a finite state machine.

    Methods:
    --------
    add_transition(transition: Transition) -> None:
        Adds the given transition to the list of transitions for this state.

    _exec_entering_action() -> None:
        Executes the entering action for this state.

    _exec_in_state_action() -> None:
        Executes the in-state action for this state.

    _exec_exiting_action() -> None:
        Executes the exiting action for this state.

    _do_entering_action() -> None:
        Does the entering action for this state.

    _do_in_state_action() -> None:
        Does the in-state action for this state.

    _do_exiting_action() -> None:
        Does the exiting action for this state.
    """
    class Parameters:
        """
        A class for defining the parameters of a state in a finite state machine.
        """
        def __init__(self) -> None:
            """
            Initializes the Parameters object.
            """
            self.terminal = False
            self.do_in_state_action_when_entering = False
            self.do_in_state_action_when_exiting = False

    def __init__(self, parameters: Parameters = Parameters()) -> None:
        """
        Initializes the State object.

        Parameters:
        -----------
        parameters : Parameters, optional
            The parameters for this state, by default an empty Parameters object.
        """
        self.__parameters = parameters
        self.__transitions = []

    @property
    def is_valid(self) -> bool:
        """
        Returns whether this state is valid or not, i.e., whether it has at least one transition, and all transitions are valid.

        Returns:
        --------
        bool:
            Whether this state is valid or not.
        """
        return all(transition.is_valid for transition in self.__transitions) if self.__transitions else True
    
    @property
    def is_terminal(self) -> bool:
        """
        Returns whether this state is a terminal state or not.

        Returns:
        --------
        bool:
            Whether this state is a terminal state or not.
        """
        return self.__parameters.terminal

    @property
    def is_transiting(self) -> "Transition":
        """
        Returns the current transition for this state, if any.

        Returns:
        --------
        Transition:
            The current transition for this state, or None if there is no current transition.
        """
        next_transition = next((transition for transition in self.__transitions if transition.is_transiting), None)
        return next((transition for transition in self.__transitions if transition.is_transiting), None)

    def add_transition(self, transition: "Transition") -> None:
        """
        Adds the given transition to the list of transitions for this state.

        Parameters:
        -----------
        transition : Transition
            The transition to add to the list of transitions for this state.

        Raises:
        -------
        TypeError:
            If the given transition is not of type Transition.
        """
        # if  type(transition) is not Transition:
        # if not isinstance(transition, "Transition"):
        #     raise TypeError("transition must be of type Transition")
        self.__transitions.append(transition)
        
        
    def _exec_entering_action(self) -> None:
        """
        Executes the entering action for this state.
        """
        self._do_entering_action()        
        if self.__parameters.do_in_state_action_when_entering:
            self._exec_in_state_action()
        # print("_exec_entering_action")

    def _exec_in_state_action(self) -> None:
        """
        Executes the in-state action for this state.
        """
        self._do_in_state_action()
        # print("_exec_in_state_action")
    
    def _exec_exiting_action(self) -> None:
        """
        Executes the exiting action for this state.
        """
        if self.__parameters.do_in_state_action_when_exiting:
            self._exec_in_state_action()
            
        self._do_exiting_action()

    def _do_entering_action(self) -> None:
        """
        Does the entering action for this state.
        """
        raise NotImplementedError("_do_entering_action must be implemented.")

    def _do_in_state_action(self) -> None:
        """
        Does the in-state action for this state.
        """
        raise NotImplementedError("_do_in_state_action must be implemented.")

    def _do_exiting_action(self) -> None:
        """
        Does the exiting action for this state.
        """
        raise NotImplementedError("_do_exiting_action must be implemented.")
        # print("_do_exiting_action")




class ActionState(State):
    
    Action = Callable[[], None]
    
    def __init__(self, parameters: "State.Parameters" = State.Parameters()) -> None:
        super().__init__(parameters)
        self.__entering_actions = []
        self.__in_state_actions = []
        self.__exiting_actions = []
        
    def _do_entering_action(self) -> None:
        for action in self.__entering_actions:
            action()
    
    def _do_in_state_action(self) -> None:
        for action in self.__in_state_actions:
            action()
    
    def _do_exiting_action(self) -> None:
        for action in self.__exiting_actions:
            action()
        
    def add_entering_action(self, action: Action) -> None:    
        if not callable(action):
            raise TypeError("action must be callable")    
        self.__entering_actions.append(action)
        
    def add_in_state_action(self, action: Action) -> None:
        if not callable(action):
            raise TypeError("action must be callable")  
        self.__in_state_actions.append(action)
        
    def add_exiting_action(self, action: Action) -> None:
        if not callable(action):
            raise TypeError("action must be callable")
        self.__exiting_actions.append(action)
        
        
        
        
class MonitoredState(ActionState):
    def __init__(self, parameters: "State.Parameters" = State.Parameters()) -> None:
        super().__init__(parameters)
        self.__counter_last_entry = 0
        self.__counter_last_exit = 0
        self.__entry_count = 0 
        self.custom_value = any 
        
    @property
    def entry_count(self) -> int:
        return self.__entry_count
    @property
    def last_entry_time(self)->float:
        return self.__counter_last_entry
    @property
    def last_exit_time(self)->float:
        return self.__counter_last_exit
    
    def reset_entry_count(self):
        self.__entry_count = 0
        
    def reset_last_times(self):
        self.__counter_last_entry = 0
        self.__counter_last_exit = 0
        
    def _exec_entering_action(self) -> None:
        self.__counter_last_entry = time.perf_counter()
        self.__entry_count += 1
        super()._exec_entering_action()
   
    def _exec_exiting_action(self) -> None:
        super()._exec_exiting_action()
        self.__counter_last_exit = time.perf_counter()
        
class RobotState(MonitoredState):
    def __init__(self, robot, parameters=State.Parameters()) -> None:
        super().__init__(parameters)
        self.robot = robot
        
        
class FSMState(RobotState):
    def __init__(self, robot, fsm, parameters=State.Parameters()) -> None:
        super().__init__(robot, parameters)
        self.fsm = fsm
        
        def change_active():
            if self.robot.active_state_machine is self.fsm: 
                self.robot.active_state_machine = None
            else:
                self.robot.active_state_machine = self.fsm
        
        self.add_entering_action(change_active)
        self.add_exiting_action(change_active)
        self.add_entering_action(lambda: print(f"Entré dans le finite state machine {self.robot.active_state_machine} "))

        
        
        