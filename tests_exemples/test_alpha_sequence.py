import unittest
from alpha_sequence import AlphaSequence

class TestAlphaSequence(unittest.TestCase):

    def test_constructor(self):
        seq = AlphaSequence(5, 2, maximum_value=15, is_cyclic=True,
                            generate_first=True, prefix='SEQ_', suffix='_ID', padding_size=3, padding_char='0',
                            conversion_chars='0123456789ABCDEF')
        self.assertEqual(seq.initial_value, 5)
        self.assertEqual(seq.increment_by, 2)
        self.assertEqual(seq.maximum_value, 15)
        self.assertTrue(seq.is_cyclic)
        self.assertTrue(seq.current_value == seq.initial_value)
        # self.assertTrue(str(seq) == 'SEQ_005_ID')
        # self.assertTruel(len(seq) == 10)

    def test_constructor_invalid_inputs(self):
        with self.assertRaises(TypeError):
            AlphaSequence('invalid', 1)
        with self.assertRaises(TypeError):
            AlphaSequence(1, 'invalid')
        with self.assertRaises(TypeError):
            AlphaSequence(1, 0)
        with self.assertRaises(TypeError):
            AlphaSequence(1, 1, maximum_value='invalid')
        with self.assertRaises(ValueError):
            AlphaSequence(1, 1, maximum_value=1)
        with self.assertRaises(ValueError):
            AlphaSequence(1, 1, maximum_value=0)
        with self.assertRaises(ValueError):
            AlphaSequence(2, -1, maximum_value=3)
        with self.assertRaises(TypeError):
            AlphaSequence(1, 1, is_cyclic='invalid')
        with self.assertRaises(ValueError):
            AlphaSequence(1, 1, is_cyclic=True)
        with self.assertRaises(TypeError):
            AlphaSequence(1, 1, generate_first='invalid')
        with self.assertRaises(TypeError):
            AlphaSequence(1, 1, prefix=1)
        with self.assertRaises(TypeError):
            AlphaSequence(1, 1, suffix=1)
        with self.assertRaises(TypeError):
            AlphaSequence(1, 1, padding_size='invalid')
        with self.assertRaises(ValueError):
            AlphaSequence(1, 1, padding_size=-1)
        with self.assertRaises(TypeError):
            AlphaSequence(1, 1, padding_char=12)
        with self.assertRaises(ValueError):
            AlphaSequence(1, 1, padding_char='invalid')
        with self.assertRaises(TypeError):
            AlphaSequence(1, 1, conversion_chars=123)
        with self.assertRaises(TypeError):
            AlphaSequence(1, 1, conversion_chars=[1, 2, 3])
        with self.assertRaises(ValueError):
            AlphaSequence(1, 1, conversion_chars='AABB')

    def test_current_value_before_next_value(self):
        seq = AlphaSequence(1, 1)
        with self.assertRaises(AlphaSequence.ASException):
            seq.current_value

    def test_current_formatted_value_before_next_value(self):
        seq = AlphaSequence(1, 1)
        with self.assertRaises(AlphaSequence.ASException):
            seq.current_formatted_value

    def test_next_value(self):
        seq = AlphaSequence(5, 2, generate_first=True)
        self.assertEqual(seq.next_value, 7)
        self.assertEqual(seq.next_value, 9)
        self.assertEqual(seq.current_value, 9)

    def test_next_formatted_value(self):
        seq = AlphaSequence(1, 1, prefix='SEQ_', suffix='_ID', padding_size=3, padding_char='0', conversion_chars='0123456789ABCDEF')
        self.assertEqual(seq.next_formatted_value, 'SEQ_001_ID')
        self.assertEqual(seq.next_formatted_value, 'SEQ_002_ID')
        self.assertEqual(seq.current_formatted_value, 'SEQ_002_ID')
        
    def test_increment_by_non_integer(self):
        with self.assertRaises(TypeError):
            AlphaSequence(0, 1.5)
            
    def test_invalid_initial_value(self):
        with self.assertRaises(TypeError):
            AlphaSequence('abc', 1)

    def test_maximum_value_non_integer(self):
        with self.assertRaises(TypeError):
            AlphaSequence(0, 1, maximum_value=3.14)

    def test_prefix_suffix_non_string(self):
        with self.assertRaises(TypeError):
            AlphaSequence(0, 1, prefix=123, suffix=456)
            
    def test_padding_char_invalid(self):
        with self.assertRaises(ValueError):
            AlphaSequence(0, 1, padding_char='ab')
            
    def test_conversion_chars_not_string(self):
        with self.assertRaises(TypeError):
            AlphaSequence(0, 1, conversion_chars=[0, 1, 2, 3])

    def test_cyclic_sequence_large_values(self):
        seq = AlphaSequence(1000000, 1000000, maximum_value=3000000, is_cyclic=True)
        self.assertEqual(seq.next_formatted_value, '1000000')
        self.assertEqual(seq.next_formatted_value, '2000000')
        self.assertEqual(seq.next_formatted_value, '3000000')
        self.assertEqual(seq.next_formatted_value, '1000000') # Should cycle back to initial value
    
    def test_sequence_initial_values(self):
        seq = AlphaSequence()
        self.assertEqual(seq.next_value, 0)
        self.assertEqual(seq.next_value, 1)
        self.assertEqual(seq.current_value, 1)
        self.assertEqual(seq.next_formatted_value, '2')
        self.assertEqual(seq.next_formatted_value, '3')
        self.assertEqual(seq.current_formatted_value, '3')

        seq = AlphaSequence(100)
        self.assertEqual(seq.next_value, 100)
        self.assertEqual(seq.next_value, 101)
        self.assertEqual(seq.current_value, 101)
        self.assertEqual(seq.next_formatted_value, '102')
        self.assertEqual(seq.next_formatted_value, '103')
        self.assertEqual(seq.current_formatted_value, '103')

        seq = AlphaSequence(-100)
        self.assertEqual(seq.next_value, -100)
        self.assertEqual(seq.next_value, -99)
        self.assertEqual(seq.current_value, -99)
        self.assertEqual(seq.next_formatted_value, '-98')
        self.assertEqual(seq.next_formatted_value, '-97')
        self.assertEqual(seq.current_formatted_value, '-97')

    def test_increment(self):
        seq = AlphaSequence(0, 2)
        self.assertEqual(seq.next_value, 0)
        self.assertEqual(seq.next_value, 2)
        self.assertEqual(seq.current_value, 2)
        self.assertEqual(seq.next_formatted_value, '4')
        self.assertEqual(seq.next_formatted_value, '6')
        self.assertEqual(seq.current_formatted_value, '6')

        seq = AlphaSequence(100, 100)
        self.assertEqual(seq.next_value, 100)
        self.assertEqual(seq.next_value, 200)
        self.assertEqual(seq.current_value, 200)
        self.assertEqual(seq.next_formatted_value, '300')
        self.assertEqual(seq.next_formatted_value, '400')
        self.assertEqual(seq.current_formatted_value, '400')

        seq = AlphaSequence(1000, -1000)
        self.assertEqual(seq.next_value, 1000)
        self.assertEqual(seq.next_value, 0)
        self.assertEqual(seq.current_value, 0)
        self.assertEqual(seq.next_formatted_value, '-1000')
        self.assertEqual(seq.next_formatted_value, '-2000')
        self.assertEqual(seq.current_formatted_value, '-2000')

    def test_maximum_value_is_cyclic(self):
        seq = AlphaSequence(0, 2, 5)
        self.assertEqual(seq.next_value, 0)
        self.assertEqual(seq.next_value, 2)
        self.assertEqual(seq.next_value, 4)
        
        with self.assertRaises(AlphaSequence.ASException):
            seq.next_value

        seq = AlphaSequence(0, 2, 6, False)
        self.assertEqual(seq.next_value, 0)
        self.assertEqual(seq.next_value, 2)
        self.assertEqual(seq.next_value, 4)
        self.assertEqual(seq.next_value, 6)
        with self.assertRaises(AlphaSequence.ASException):
            seq.next_value

        seq = AlphaSequence(0, 2, 6, True)
        self.assertEqual(seq.next_value, 0)
        self.assertEqual(seq.next_value, 2)
        self.assertEqual(seq.next_value, 4)
        self.assertEqual(seq.next_value, 6)
        self.assertEqual(seq.next_value, 0)
        self.assertEqual(seq.next_value, 2)

        seq = AlphaSequence(1000, -3, 990, True, generate_first=True)
        self.assertEqual(seq.current_value, 1000)
        self.assertEqual(seq.next_value, 997)
        self.assertEqual(seq.next_formatted_value, '994')
        self.assertEqual(seq.next_value, 991)
        self.assertEqual(seq.next_formatted_value, '1000')
        self.assertEqual(seq.next_formatted_value, '007')

    def test_formatted(self):
        seq = AlphaSequence(0, -100, prefix='Sequence(', suffix=')', padding_size=10, padding_char=' ', conversion_chars='0123456789')
        self.assertEqual(seq.next_formatted_value, 'Sequence(         0)')
        self.assertEqual(seq.next_formatted_value, 'Sequence(      -100)')
        self.assertEqual(seq.next_formatted_value, 'Sequence(      -200)')
        self.assertEqual(seq.next_formatted_value, 'Sequence(      -300)')
        self.assertEqual(seq.next_formatted_value, 'Sequence(      -400)')

        seq = AlphaSequence(0, 2, prefix='Sequence<', suffix='>', padding_size=5, padding_char='~', conversion_chars='01234')
        self.assertEqual(seq.next_formatted_value, 'Sequence<~~~~0>')
        self.assertEqual(seq.next_formatted_value, 'Sequence<~~~~2>')
        self.assertEqual(seq.next_formatted_value, 'Sequence<~~~~4>')
        self.assertEqual(seq.next_formatted_value, 'Sequence<~~~11>')
        self.assertEqual(seq.next_formatted_value, 'Sequence<~~~13>')
        self.assertEqual(seq.next_formatted_value, 'Sequence<~~~20>')
        
        seq = AlphaSequence(0, 3, prefix='Sequence_', suffix='_|', padding_size=5, padding_char='-', conversion_chars='┘┌┐└')
        self.assertEqual(seq.next_formatted_value, 'Sequence_----┘_|')
        self.assertEqual(seq.next_formatted_value, 'Sequence_----└_|')
        self.assertEqual(seq.next_formatted_value, 'Sequence_---┌┐_|')
        self.assertEqual(seq.next_formatted_value, 'Sequence_---┐┌_|')
        self.assertEqual(seq.next_formatted_value, 'Sequence_---└┘_|')
        
        seq = AlphaSequence(0, 1, prefix='-> ', suffix=' <-', padding_size=0, padding_char=' ', conversion_chars='▁▂▃▄▅▆▇█')
        self.assertEqual(seq.next_formatted_value, '-> ▁ <-')
        self.assertEqual(seq.next_formatted_value, '-> ▂ <-')
        self.assertEqual(seq.next_formatted_value, '-> ▃ <-')
        self.assertEqual(seq.next_formatted_value, '-> ▄ <-')
        self.assertEqual(seq.next_formatted_value, '-> ▅ <-')


if __name__ == '__main__':
    unittest.main()
