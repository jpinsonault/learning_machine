from Computer import Computer


class Generation(object):
	"""A generation of programs"""
	def __init__(self):
		super(Generation, self).__init__()
		
		self.programs = []
		self.generate_programs()

	def run_all(self):
		for program in self.programs:
			program.run_program()

	def get_outputs():
		return [program.output for program in self.programs]


class ProgramResult(object):
	"""Holds a program and it's output/score"""
	def __init__(self, program):
		super(ProgramResult, self).__init__()
		self.program = program

		self.computer = Computer()
		self.computer.load_program(program)
		
		self.output = None

	def run(self):
		self.computer.run_program()

		self.output = self.computer.output_queue