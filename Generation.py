from Computer import Computer
from InstructionGenerator import Generator
import threading


TIMEOUT = .02


class Generation(object):

    STARTING_SIZE = 10

    """A generation of programs"""
    def __init__(self, pop_size, inputs=[]):
        super(Generation, self).__init__()
        self.pop_size = pop_size
        self.inputs = inputs

        self.program_results = []
        self.generate_programs()

        self.generation_number = 0

    def run_all(self):
        for program in self.program_results:
            program.run_program()

        self.generation_number += 1

    def generate_programs(self):
        generator = Generator()

        self.program_results = [ProgramResult(generator.random_program(self.STARTING_SIZE), self.inputs) 
                                for _ in xrange(self.pop_size)]


class ProgramResult(object):
    """Holds a program and it's output/score"""
    def __init__(self, program, inputs):
        super(ProgramResult, self).__init__()
        self.program = program

        self.computer = Computer()
        self.computer.load_program(program)
        
        self.output = None
        self.memory = None
        self.was_killed = False

    def run_program(self):
        def target():
            self.computer.run_program()
        
        self.was_killed = False

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(TIMEOUT)
        if thread.is_alive():
            self.computer.kill_program()
            self.was_killed = True
            thread.join()

        self.output = self.computer.output_queue
        self.memory = self.computer.memory