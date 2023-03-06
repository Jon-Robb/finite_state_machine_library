import unittest
from finite_state_machine import FiniteStateMachine, State, Transition
# from transition import Transition

class TestState(unittest.TestCase):
    
    def test_is_valid_with_no_transitions(self):
        # test that a state with no transitions is not valid
        state = State()
        self.assertFalse(state.is_valid)
        
        
    def test_is_valid_with_valid_transitions(self):
        # Test that a state with valid transitions is valid
        state1 = State()
        state2 = State()
        transition = Transition(state2)
        state1.add_transition(transition)
        self.assertTrue(state1.is_valid)
        self.assertFalse(state2.is_valid)
        
    def test_is_valid_with_invalid_transitions(self):
        # Test that a state with invalid transitions is not valid
        state1 = State()
        state2 = State()
        transition = Transition()
        state1.add_transition(transition)
        self.assertFalse(state1.is_valid)
        self.assertFalse(state2.is_valid)
        
        
        
class TestTransition(unittest.TestCase):
    
    def test_is_valid_with_valid_states(self):
        # Test that a transition with valid states is valid
        state1 = State()
        transition = Transition(state1)
        self.assertTrue(transition.is_valid)
    

if __name__ == '__main__':
    unittest.main()