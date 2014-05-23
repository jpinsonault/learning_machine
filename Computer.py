from collections import defaultdict
from six import string_types


class Computer(object):
    """An emulated computer with a simple instruction set"""
    def __init__(self):
        super(Computer, self).__init__()
        
        self.memory = defaultdict(int)

        self.program = []
        # Program counter
        self.pc = 0

    def load_program(self, program):
        self.program = program
        self.pc = 0

    def run_program(self):
        while self.pc < len(self.program):
            instruction, operands = self.program[self.pc]

            function = getattr(self, instruction)
            print("{}: {}".format(instruction, operands))
            function(*operands)

            self.pc += 1
            

    def dereference(self, variable):
        if isinstance(variable, string_types):
            return self.memory[variable]
        else:
            return variable

    def add(self, first, second, dest):
        first_ = self.dereference(first)
        second_ = self.dereference(second)

        self.memory[dest] = first_ + second_

    def move(self, source, dest):
        self.memory[dest] = self.dereference(source)

    def load(self, value, dest):
        self.memory[dest] = value

    def print_mem(self, location):
        print(self.memory[location])

    def print_string(self, location, length):
        pass