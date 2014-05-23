from collections import defaultdict
from six import string_types
from TypeChecking import accepts


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
        try:
            while self.pc < len(self.program):
                instruction, operands = self.program[self.pc]

                function = getattr(self, instruction)
                # print("{}: {}".format(instruction, operands))
                function(*operands)

                self.pc += 1
        except IndexError, e:
            print("Jumped out of program")
        
            
    def dereference(self, variable):
        if isinstance(variable, string_types):
            return self.memory[variable]
        else:
            return variable

    @accepts("register")
    def inc(self, location):
        self.memory[location] = self.dereference(location) + 1

    @accepts("register")
    def dec(self, location):
        self.memory[location] = self.dereference(location) - 1

    @accepts("register")
    def clear(self, location):
        self.memory[location] = 0

    @accepts("any", "any", "register")
    def add(self, first, second, dest):
        first_ = self.dereference(first)
        second_ = self.dereference(second)

        self.memory[dest] = first_ + second_

    @accepts("any", "any", "register")
    def multiply(self, first, second, dest):
        first_ = self.dereference(first)
        second_ = self.dereference(second)

        self.memory[dest] = first_ * second_

    @accepts("any", "any", "register")
    def divide(self, first, second, dest):
        first_ = self.dereference(first)
        second_ = self.dereference(second)

        self.memory[dest] = first_ / second_

    def nop(self):
        pass

    @accepts("register", "register")
    def move(self, source, dest):
        self.memory[dest] = self.dereference(source)

    @accepts("int", "register")
    def load(self, value, dest):
        self.memory[dest] = value

    @accepts("any")
    def jump(self, distance):
        distance_ = self.dereference(distance)
        
        # -1 becuase the pc will increment after this instruction anyways
        self.pc += (distance_ - 1)
        if self.pc < 0 or self.pc > len(self.program):
            raise IndexError

    @accepts("register", "any")
    def jump_if_zero(self, location, distance):
        distance_ = self.dereference(distance)
        if self.dereference(location) == 0:
            self.jump(distance_)

    @accepts("register", "any")
    def jump_if_pos(self, location, distance):
        distance_ = self.dereference(distance)
        if self.dereference(location) >= 0:
            self.jump(distance_)

    @accepts("register", "any")
    def jump_if_neg(self, location, distance):
        distance_ = self.dereference(distance)
        if self.dereference(location) < 0:
            self.jump(distance_)

    @accepts("register")
    def print_mem(self, location):
        print(self.memory[location])

    @accepts("register", "any")
    def print_string(self, location, length):
        pass