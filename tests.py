import unittest
from Computer import Computer


class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.computer = Computer()

    def test_load(self):
        self.computer.load_program([['load', [2, '1']]])
        self.computer.run_program()

        self.failUnless(self.computer.memory['1'].value == 2)

    def test_move(self):
        self.computer.load_program([
            ['load', [2, '1']],
            ['move', ['1', '2']]
        ])
        self.computer.run_program()

        self.failUnless(self.computer.memory['2'].value == 2)

    def test_dec(self):
        self.computer.load_program([
            ['load', [2, '1']],
            ['dec', ['1']],
            ['dec', ['1']],
            ['dec', ['1']],
        ])
        self.computer.run_program()

        self.failUnless(self.computer.memory['1'].value == -1)

    def test_inc(self):
        self.computer.load_program([
            ['load', [2, '1']],
            ['inc', ['1']],
            ['inc', ['1']],
            ['inc', ['1']],
        ])
        self.computer.run_program()

        self.failUnless(self.computer.memory['1'].value == 5)

    def test_clear(self):
        self.computer.load_program([
            ['load', [2, '1']],
            ['clear', ['1']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['1'].value, 0)

    def test_add(self):
        self.computer.load_program([
            ['load', [2, '1']],
            ['add', [1, '1', '2']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['2'].value, 3)
        self.failUnlessEqual(self.computer.memory['1'].value, 2)

    def test_multiply(self):
        self.computer.load_program([
            ['load', [2, '1']],
            ['multiply', [3, '1', '2']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['2'].value, 6)
        self.failUnlessEqual(self.computer.memory['1'].value, 2)

    def test_divide_no_remainder(self):
        self.computer.load_program([
            ['load', [6, '1']],
            ['divide', ['1', 2, '2']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['2'].value, 3)
        self.failUnlessEqual(self.computer.memory['1'].value, 6)

    def test_divide_with_remainder(self):
        self.computer.load_program([
            ['load', [7, '1']],
            ['divide', ['1', 2, '2']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['2'].value, 3)
        self.failUnlessEqual(self.computer.memory['1'].value, 7)

    def test_shift_left(self):
        self.computer.load_program([
            ['load', [6, '1']],
            ['shift_left', ['1']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['1'].value, 12)

    def test_shift_right(self):
        self.computer.load_program([
            ['load', [6, '1']],
            ['shift_right', ['1']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['1'].value, 3)

    def test_bit_or(self):
        self.computer.load_program([
            ['load', [0b010101, '1']],
            ['load', [0b011111, '2']],
            ['bit_or', ['1', '2']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['1'].value, 0b011111)

    def test_bit_and(self):
        self.computer.load_program([
            ['load', [0b010101, '1']],
            ['load', [0b011111, '2']],
            ['bit_and', ['1', '2']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['1'].value, 0b010101)

    def test_complement(self):
        self.computer.load_program([
            ['load', [0b010101, '1']],
            ['complement', ['1']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['1'].value, ~0b010101)

    def test_bit_xor(self):
        self.computer.load_program([
            ['load', [0b010101, '1']],
            ['load', [0b011111, '2']],
            ['bit_xor', ['1', '2']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['1'].value, 0b010101 ^ 0b011111)

    def test_jump(self):
        self.computer.load_program([
            ['jump', [2]],
            ['load', [1, '2']], # Should never run
            ['load', [2, '3']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['3'].value, 2)
        self.failIfEqual(self.computer.memory['2'].value, 1)

    def test_jump_if_neg_on_negative(self):
        self.computer.load_program([
            ['load', [-1, '1']],
            ['jump_if_neg', ['1', 2]],
            ['load', [1, '2']], # Should never run
            ['load', [2, '3']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['3'].value, 2)
        self.failIfEqual(self.computer.memory['2'].value, 1)

    def test_jump_if_neg_on_positive(self):
        self.computer.load_program([
            ['load', [5, '1']],
            ['jump_if_neg', ['1', 2]],
            ['load', [1, '2']], # Should run
            ['load', [2, '3']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['3'].value, 2)
        self.failUnlessEqual(self.computer.memory['2'].value, 1)

    def test_jump_if_pos_on_positive(self):
        self.computer.load_program([
            ['load', [5, '1']],
            ['jump_if_pos', ['1', 2]],
            ['load', [1, '2']], # Should never run
            ['load', [2, '3']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['3'].value, 2)
        self.failIfEqual(self.computer.memory['2'].value, 1)

    def test_jump_if_pos_on_negative(self):
        self.computer.load_program([
            ['load', [-1, '1']],
            ['jump_if_pos', ['1', 2]],
            ['load', [1, '2']], # Should run
            ['load', [2, '3']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['3'].value, 2)
        self.failUnlessEqual(self.computer.memory['2'].value, 1)

    def test_jump_if_eq_on_equal(self):
        self.computer.load_program([
            ['load', [5, '1']],
            ['load', [5, '2']],
            ['jump_if_eq', ['1', '2', 2]],
            ['load', [1, '3']], # Should never run
            ['load', [2, '4']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['4'].value, 2)
        self.failIfEqual(self.computer.memory['3'].value, 1)

    def test_jump_if_eq_on_not_equal(self):
        self.computer.load_program([
            ['load', [5, '1']],
            ['load', [4, '2']],
            ['jump_if_eq', ['1', '2', 2]],
            ['load', [1, '3']], # Should run
            ['load', [2, '4']],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['4'].value, 2)
        self.failUnlessEqual(self.computer.memory['3'].value, 1)

    def test_push(self):
        self.computer.load_program([
            ['load', [5, '1']],
            ['push', ['1']],
            ['push', [1]],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.stack[0], 5)
        self.failUnlessEqual(self.computer.stack[1], 1)        


    def test_pop_with_non_empty_stack(self):
        self.computer.load_program([
            ['load', [5, '1']],
            ['push', ['1']],
            ['push', [1]],
            ['pop', "3"],
            ['pop', "4"],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['4'].value, 5)
        self.failUnlessEqual(self.computer.memory['3'].value, 1)

    def test_pop_with_empty_stack(self):
        self.computer.load_program([
            ['pop', "3"],
            ['pop', "4"],
        ])
        self.computer.run_program()

        self.failUnlessEqual(self.computer.memory['4'].value, 0)
        self.failUnlessEqual(self.computer.memory['3'].value, 0)       



class TestProgramCounter(unittest.TestCase):
    def setUp(self):
        self.computer = Computer()

    def test_pc_ends_with_correct_value(self):
        self.computer.load_program([
            ['load', [-1, '1']],
            ['jump_if_pos', ['1', 2]],
            ['load', [1, '2']], # Should run
            ['load', [2, '3']],
        ])

        self.computer.run_program()

        self.failUnlessEqual(self.computer.pc, 4)


class TestInputLoading(unittest.TestCase):
    def setUp(self):
        self.computer = Computer()

    def test_inputs_loaded(self):
        self.computer.load_program([
            ['load', [-1, '1']],
            ['jump_if_pos', ['1', 2]],
            ['load', [1, '2']], # Should run
            ['load', [2, '3']],
        ], [5, 4, 3, 2, 1])

        self.failUnlessEqual(self.computer.memory["0"].value, 5)
        self.failUnlessEqual(self.computer.memory["4"].value, 1)


class TestOutputQueue(unittest.TestCase):
    def setUp(self):
        self.computer = Computer()

    def test_queue_has_correct_values(self):
        self.computer.load_program([
            ['print_mem', ['0']],
            ['print_char', ['0']],
        ], [33])

        self.computer.run_program()

        self.failUnlessEqual(self.computer.output_queue[0], 33)
        self.failUnlessEqual(self.computer.output_queue[1], '!')


if __name__ == '__main__':
    unittest.main()