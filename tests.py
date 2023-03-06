import unittest
from finite_state_machine import FiniteStateMachine, State, Transition
# from transition import Transition
class TestFiniteStateMachine(unittest.TestCase):
    pass
    # def test_finite_state_machine_is_invalid_with_no_states(self):
    #     # Test that a finite state machine with no states is not valid

    #     fsm = FiniteStateMachine()
    #     self.assertFalse(fsm.is_valid)
    
class TestState(unittest.TestCase):
    
    def test_state_is_valid_with_no_transitions(self):
        # test that a state with no transitions is not valid
        state = State()
        self.assertFalse(state.is_valid)
        
        
    def test_state_is_valid_with_valid_transitions(self):
        # Test that a state with valid transitions is valid
        state1 = State()
        state2 = State()
        transition = Transition(state2)
        state1.add_transition(transition)
        self.assertTrue(state1.is_valid)
        self.assertFalse(state2.is_valid)
        
    def test_state_is_valid_with_invalid_transitions(self):
        # Test that a state with invalid transitions is not valid
        state1 = State()
        state2 = State()
        transition = Transition()
        state1.add_transition(transition)
        self.assertFalse(state1.is_valid)
        self.assertFalse(state2.is_valid)
        
        
class TestTransition(unittest.TestCase):
    
    def test_transition_is_valid_with_valid_states(self):
        # Test that a transition with valid states is valid
        state1 = State()
        transition1 = Transition(state1)
        self.assertTrue(transition1.is_valid)
    
    def test_transition_is_invalid_with_no_state(self):
        # Test that a transition with no states is not valid
        transition2 = Transition()
        self.assertFalse(transition2.is_valid)
    
    def test_is_valid_with_no_states(self):
        # Test that a transition with invalid states is invalid
        transition = Transition()  # Invalid transition
        self.assertFalse(transition.is_valid)


if __name__ == '__main__':
    unittest.main()