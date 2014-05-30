import random


instructions = {
    "inc":          ["register"],
    "dec":          ["register"],
    "clear":        ["register"],
    "add":          ["any", "any", "register"],
    "multiply":     ["any", "any", "register"],
    "divide":       ["any", "any", "register"],
    "shift_left":   ["register"],
    "shift_right":  ["register"],
    "bit_or":       ["register", "any"],
    "bit_and":      ["register", "any"],
    "complement":   ["register"],
    "bit_xor":      ["register", "any"],
    "nop":          [],
    "move":         ["register", "register"],
    "load":         ["int", "register"],
    "push":         ["any"],
    "pop":          ["register"],
    "jump":         ["any"],
    "jump_if_pos":  ["register", "any"],
    "jump_if_neg":  ["register", "any"],
    "jump_if_eq":   ["register", "any", "any"],
    "print_mem":    ["register"],
    # "print_string": ["register", "any"],
}




class Generator(object):
    """Generators random instructions

        Ideas:
            Generator instructions that have a probability of using
            addresses already used by the program
    """

    MAX_REGISTER = 5
    MAX_INT = 10

    def __init__(self, program=None):
        super(Generator, self).__init__()
        self.program = program

    def random(self):
        """Generate random instruction"""
        instruction, operand_templates = random.choice(instructions.items())

        operands = [self._random_operand(template) for template in operand_templates]

        return [instruction, operands]

    def _random_operand(self, template):
        templates = {
            "register": self._random_register,
            "int": self._random_int,
            "any": self._random_any
        }

        return templates[template]()

    def _random_register(self):
        return str(random.randint(0, self.MAX_REGISTER))

    def _random_int(self):
        return random.randint(-self.MAX_INT, self.MAX_INT)

    def _random_any(self):
        return random.choice([self._random_register, self._random_int])()
