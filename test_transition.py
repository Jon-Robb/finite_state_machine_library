import unittest
from transition import Transition

def main(self):
    transition = Transition()
    self.assertFalse(transition.is_valid())

if __name__ == '__main__':
    unittest.main()