from collections import defaultdict
from six import string_types
from TypeChecking import accepts


class Computer(object):
    """An emulated computer with a simple instruction set"""
    def __init__(self):
        super(Computer, self).__init__()
        
        self.reset_computer()

    def load_program(self, program, inputs=[]):
        self.reset_computer()
        self.program = program

        self.load_inputs(inputs)

    def load_inputs(self, inputs):
        for index, value in enumerate(inputs):
            self.memory[str(index)].value = value

    def reset_computer(self):
        self.program = []
        self.pc = 0
        self.stack = []
        self.status = {}
        self.memory = defaultdict(lambda: MemoryLocation())
        self.output_queue = []

    def run_program(self):
        try:
            while self.pc < len(self.program):
                instruction, operands = self.program[self.pc]

                function = getattr(self, instruction)
                # print("{}: {}".format(instruction, operands))
                function(*operands)

                self.pc += 1
        except JumpedOutException, e:
            print("Jumped out of program")
            
    def dereference(self, variable):
        if isinstance(variable, string_types):
            return self.memory[variable].value
        else:
            return variable

    def set_status(self, **kwargs):
        pass

    def output(self, value):
        self.output_queue.append(value)

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

    @accepts("register", "any")
    def bit_or(self, location, mask):
        mask_ = self.dereference(mask)
        self.memory[location].value |= mask_

    @accepts("register", "any")
    def bit_and(self, location, mask):
        mask_ = self.dereference(mask)
        self.memory[location].value &= mask_

    @accepts("register")
    def complement(self, location):
        self.memory[location].value = ~self.memory[location].value

    @accepts("register", "any")
    def bit_xor(self, location, mask):
        mask_ = self.dereference(mask)
        self.memory[location].value ^= mask_

    def nop(self):
        pass

    @accepts("register", "register")
    def move(self, source, dest):
        self.memory[dest].value = self.dereference(source)

    @accepts("int", "register")
    def load(self, value, dest):
        self.memory[dest].value = value

    @accepts("any")
    def push(self, value):
        value_ = self.dereference(value)

        self.stack.append(value_)

    @accepts("register")
    def pop(self, dest):
        try:
            value = self.stack.pop()
        except IndexError, e:
            value = 0

        self.memory[dest].value = value


    @accepts("any")
    def jump(self, distance):
        distance_ = self.dereference(distance)
        
        # -1 becuase the pc will increment after this instruction anyways
        self.pc += (distance_ - 1)
        if self.pc < 0 or self.pc > len(self.program):
            raise JumpedOutException

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

    @accepts("register", "any", "any")
    def jump_if_eq(self, first, second, distance):
        first_ = self.dereference(first)
        second_ = self.dereference(second)

        distance_ = self.dereference(distance)
        if first_ == second_:
            self.jump(distance_)

    @accepts("register")
    def print_mem(self, location):
        """Prints the memory location as an int"""
        self.output(self.memory[location].value)

    @accepts("register")
    def print_char(self, location):
        """Chops off all by the first 8 bits and prints it as a char"""
        value = self.memory[location].value
        self.output(chr(value & 0b11111111))

    @accepts("register", "any")
    def print_string(self, location, length):
        length_ = self.dereference(length)
        location_int = int(location)
        output_string = []
        for index in xrange(location_int, location_int + length_):
            print(self.memory[str(index)])
            output_string.append(chr(self.memory[str(index)].value))

        self.output("".join(output_string))
        # self.output("".join([chr(self.memory[str(index)]) for index in xrange(location_int, location_int + length_)]))


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
        return "MemoryLocation(value={})".format(self.value)

class JumpedOutException(Exception):
    """Exception for when execution jumps out of the program memory"""
    def __init__(self, error_string):
        super(JumpedOutException, self).__init__(error_string)
        self.error_string = error_string
        