instructions = {
    "inc":          ["register"],
    "dec":          ["register"],
    "clear":        ["register"],
    "add":          ["any", "any", "register"],
    "multiply":     ["any", "any", "register"],
    "divide":       ["any", "any", "register"],
    "nop":          [],
    "move":         ["register", "register"],
    "load":         ["int", "register"],
    "jump":         ["any"],
    "jump_if_zero": ["register", "any"],
    "jump_if_pos":  ["register", "any"],
    "jump_if_neg":  ["register", "any"],
    "print_mem":    ["register"],
    "print_string": ["register", "any"],
}


class Generator(object):
    """Generators random instructions

        Ideas:
            Generator instructions that have a probability of using
            addresses already used by the program
    """
    def __init__(self, program=None):
        super(Generator, self).__init__()
        self.program = program

    def random(self):
        """Generate random instruction"""

