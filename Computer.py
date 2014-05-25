from collections import defaultdict
from six import string_types
from TypeChecking import accepts


class Computer(object):
    """An emulated computer with a simple instruction set"""
    def __init__(self):
        super(Computer, self).__init__()
        
        self.memory = defaultdict(lambda: MemoryLocation())

        self.program = []
        # Program counter
        self.pc = 0
        self.status = {}

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
            return self.memory[variable].value
        else:
            return variable

    def set_status(self, **kwargs):
        for arg, value in kwargs.items():
            self.status[arg] = value

    @accepts("register")
    def inc(self, location):
        self.memory[location].value = self.dereference(location) + 1

    @accepts("register")
    def dec(self, location):
        self.memory[location].value = self.dereference(location) - 1

    @accepts("register")
    def clear(self, location):
        self.memory[location].value = 0

    @accepts("any", "any", "register")
    def add(self, first, second, dest):
        first_ = self.dereference(first)
        second_ = self.dereference(second)

        self.memory[dest].value = first_ + second_

    @accepts("any", "any", "register")
    def multiply(self, first, second, dest):
        first_ = self.dereference(first)
        second_ = self.dereference(second)

        self.memory[dest].value = first_ * second_

    @accepts("any", "any", "register")
    def divide(self, first, second, dest):
        first_ = self.dereference(first)
        second_ = self.dereference(second)

        self.memory[dest].value = first_ / second_

    @accepts("register")
    def shift_left(self, location):
        self.memory[location].value <<= 1

    @accepts("register")
    def shift_right(self, location):
        self.memory[location].value >>= 1

    def nop(self):
        pass

    @accepts("register", "register")
    def move(self, source, dest):
        self.memory[dest].value = self.dereference(source)

    @accepts("int", "register")
    def load(self, value, dest):
        self.memory[dest].value = value

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
        if self.dereference(location) > 0:
            self.jump(distance_)

    @accepts("register", "any")
    def jump_if_neg(self, location, distance):
        distance_ = self.dereference(distance)
        if self.dereference(location) < 0:
            self.jump(distance_)

    @accepts("register")
    def print_mem(self, location):
        """Prints the memory location as an int"""
        print(self.memory[location].value)

    @accepts("register")
    def print_char(self, location):
        """Chops off all by the first 8 bits and prints it as a char"""
        value = self.memory[location].value
        print(chr(value & 0b11111111))

    @accepts("register", "any")
    def print_string(self, location, length):
        pass


class MemoryLocation(object):
    """Handles storing and operating on memory registers

        Memory can store one 32bit number
        If treated as a byte, the 8 low order bits are used
    """

    # 32bit max/min numbers
    MAX_INT = 2147483647
    MIN_INT = -2147483648

    def __init__(self, value=0):
        super(MemoryLocation, self).__init__()
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        # Make sure it doesn't go over or under the max/min values
        self._value = min(self._value, self.MAX_INT)
        self._value = max(self._value, self.MIN_INT)

    def as_byte(self):
        pass

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
