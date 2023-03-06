import unittest
from state import State

def main(self):
    state = State()
    self.assertFalse(state.is_valid())

if __name__ == '__main__':
    unittest.main()