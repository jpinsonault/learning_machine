from Computer import Computer
from Generation import Generation
from Generation import ProgramResult
from pprint import pprint



def main():
    comp = Computer()

    done = False

    successes = []
    gen_number = 0

    while not done:
        if gen_number % 10 == 0:
            print("Generation: {}".format(gen_number))
        gen_number += 1
        gen = Generation(10, [1,2,3,4,5])

        gen.run_all()

        successes += [result.program for result in gen.program_results if 3 in result.output]
        if len(successes) > 1:
            done = True

    pprint(successes)

def print_ascii_program():
    return [
        ["load",         [32, "4"]],
        ["inc",          ["4"]],
        ["print_char",   ["4"]],
        ["add",          ["1", "2", "1"]],
        ["jump_if_eq",   ["4", 126, 2]],
        ["jump",         [-4]],
        ["nop",          []],
    ]


def run_program(program, inputs=[]):
    run = ProgramResult(program, inputs)
    run.run_program()

    print("Output: {}\nKilled?: {}\n".format(run.output, run.was_killed))


if __name__ == '__main__':
    main()