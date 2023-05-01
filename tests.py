import unittest
import MyFSM
from finite_state_machine import FiniteStateMachine, State, Transition
import Blinker
# from transition import Transition
class TestState(unittest.TestCase):
    
    def test_state_is_valid_with_no_transitions(self):
        # test that a state with no transitions is not valid
        state = State()
        self.assertFalse(state.is_valid)
        
        
    def test_state_is_valid_with_valid_transitions(self):
        # Test that a state with valid transitions is valid
        state1 = State()
        state2 = State()
        transition = TransitionSubClass(state2)
        state1.add_transition(transition)
        self.assertTrue(state1.is_valid)
        self.assertFalse(state2.is_valid)
        
    def test_state_is_invalid_with_invalid_transitions(self):
        # Test that a state with invalid transitions is not valid
        state1 = State()
        state2 = State()
        transition = TransitionSubClass()
        state1.add_transition(transition)
        self.assertFalse(state1.is_valid)
        self.assertFalse(state2.is_valid)
        
class TransitionSubClass(Transition):
    def __init__(self, next_state: "State" = None) -> None:
        super().__init__(next_state)
        self.count = 0 
    
    @property
    def is_transiting(self) -> bool:
        self.count += 1
        return self.count % 2 == 1
           
class TestTransition(unittest.TestCase):
    
    def test_transition_is_valid_with_valid_states(self):
        # Test that a transition with valid states is valid
        state1 = State()
        transition1 = TransitionSubClass(state1)
        self.assertTrue(transition1.is_valid)
    
    def test_transition_is_invalid_with_no_state(self):
        # Test that a transition with no states is not valid
        transition2 = TransitionSubClass()
        self.assertFalse(transition2.is_valid)
        
    def test_transition_is_transiting(self):
        # Test that a transition is transiting correctly
        transition = TransitionSubClass()
        for _ in range(1000):
            self.assertTrue(transition.is_transiting)
            self.assertFalse(transition.is_transiting)
        

class TestLayout(unittest.TestCase):
    def test_layout_initial_state(self):
        # Test that the initial state is set and retrieve correctly
        layout = FiniteStateMachine.Layout()
        state1 = State()
        state2 = State()
        layout.initial_state = state1
        self.assertEqual(layout.initial_state, state1)
        self.assertNotEqual(layout.initial_state, state2)
        
    def test_layout_add_state(self):
        # Test that a state can be added to the layout
        layout = FiniteStateMachine.Layout()
        state1 = State()
        layout.add_state(state1)
        self.assertIn(state1, layout._Layout__states)
        
    def test_layout_add_states(self):
        # Test that multiple states can be added to the layout
        layout = FiniteStateMachine.Layout()
        state1 = State()
        state2 = State()
        state3 = State()
        layout.add_states([state1, state2, state3])
        self.assertIn(state1, layout._Layout__states)
        self.assertIn(state2, layout._Layout__states)
        self.assertIn(state3, layout._Layout__states)
        
    def test_layout_is_valid(self):
        # Test that a layout with an initial state is valid
        layout = FiniteStateMachine.Layout()
        state1 = State()
        layout.initial_state = state1
        layout.initial_state.add_transition(TransitionSubClass(state1))
        layout.add_state(layout.initial_state)
        self.assertTrue(layout.is_valid)
        list = []
        for _ in range(1000):
            state = State()
            state.add_transition(TransitionSubClass(state))
            list.append(state)
        layout.add_states(list)
        self.assertTrue(layout.is_valid)
        
    def test_layout_is_invalid_without_initial_state(self):
        # Test that a layout without an initial state is not valid
        layout = FiniteStateMachine.Layout()
        self.assertFalse(layout.is_valid)
        list = []
        for _ in range(1000):
            state = State()
            state.add_transition(TransitionSubClass(state))
            list.append(state)
        layout.add_states(list)
        self.assertFalse(layout.is_valid)
    
        
class TestMyFSM(unittest.TestCase):
    
    def __init__(self):
        super().__init__()
        self.fsm = MyFSM.MyFSM()
    
    def test_fsm_layout_is_valid(self):
        self.assertTrue(self.fsm._FiniteStateMachine__layout.is_valid)

    def test_applitative_state_is_equal_to_initial_state(self):
        self.assertEqual(self.fsm.current_applicative_state, self.fsm._FiniteStateMachine__layout._Layout__initial_state)


    
if __name__ == '__main__':
    
    unittest.main()