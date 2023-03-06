from typing import TYPE_CHECKING
#if TYPE_CHECKING:
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
        Returns whether this state is valid or not, i.e., whether it has at least one transition and all transitions are valid.

        Returns:
        --------
        bool:
            Whether this state is valid or not.
        """
        return self.__transitions and all(transition.is_valid for transition in self.__transitions)
    
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
        if not isinstance(transition, Transition):
            raise TypeError("transition must be of type Transition")
        self.__transitions.append(transition)
        
        
    def _exec_entering_action(self) -> None:
        """
        Executes the entering action for this state.
        """
        self._do_entering_action()        
        print("_exec_entering_action")

    def _exec_in_state_action(self) -> None:
        """
        Executes the in-state action for this state.
        """
        self._do_in_state_action()
        print("_exec_in_state_action")
    
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
        print("_do_exiting_action")





# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from transition import Transition


# class State:

#     class Parameters:
#         def __init__(self) -> None:
#             self.terminal = False
#             self.do_in_state_action_when_entering = False
#             self.do_in_state_action_when_exiting = False

#     def __init__(self, parameters:Parameters=Parameters()) -> None:
#         pass

#         self.__parameters = parameters
#         self.__transition = []

#     @property
#     def is_valid(self) -> bool:
#         all_transitions_are_valid = True
#         for transition in self.__transition:
#             if not transition.is_valid():
#                 all_transitions_are_valid = False
#                 break
#         return self.__transition and all_transitions_are_valid
    
#     @property
#     def is_terminal(self) -> bool:
#         return self.__parameters.terminal

#     @property
#     def is_transiting(self)->"Transition":
#         pass

#     def add_transition(self, transition:"Transition")->None:
#         if not isinstance(transition, Transition):
#             raise TypeError("transition must be of type Transition")
#         self.__transition.append(transition)
        
        
#     def _exec_entering_action(self):
#         print("_exec_entering_action")

#     def _exec_in_state_action(self):
#         print("_exec_in_state_action")
    
#     def _exec_exiting_action(self):
#         print("_exec_exiting_action")
    
#     def _do_entering_action(self):
#         print("_do_entering_action")

#     def _do_in_state_action(self):
#         print("_do_in_state_action")

#     def _do_exiting_action(self):
#         print("_do_exiting_action")


    