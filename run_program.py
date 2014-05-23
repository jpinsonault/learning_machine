from Computer import Computer


def main():
	comp = Computer()

	comp.load_program([
		["add", [5, 2, "1"]],
		["move", ["1", "2"]],
		["print_mem", ["2"]],
	])

	comp.run_program()


if __name__ == '__main__':
	main()