from Computer import Computer
from InstructionGenerator import Generator
from pprint import pprint


def main():
    comp = Computer()

    # Print ascii chars
    program = [
        ["load",         [32, "4"]],
        ["inc",          ["4"]],
        ["print_char",   ["4"]],
        ["add",          ["1", "2", "1"]],
        ["jump_if_eq",   ["4", 126, 2]],
        ["jump",         [-4]],
        ["nop",          []],
    ]

    # Print ascii chars as string
    program = [
        ["load",         [32, "4"]],
        ["inc",          ["4"]],
        ["add",          ["1", "2", "1"]],
        ["jump_if_eq",   ["4", 126, 2]],
        ["jump",         [-3]],
        ["print_string", ["4", 30]],
    ]



    generator = Generator()

    # program = [generator.random() for _ in range(10)]
    # program = [
    #     ['multiply', [90, 70, '7']],
    #     ['nop', []],
    #     ['jump', ['3']],
    #     ['jump_if_pos', ['62', -1]],
    #     ['load', [52, '5']],
    #     ['inc', ['17']],
    #     ['jump_if_zero', ['79', -99]],
    #     ['nop', []],
    #     ['print_mem', ['12']],
    #     ['clear', ['67']],
    #     ['divide', ['40', -78, '97']],
    #     ['multiply', [-83, '4', '48']],
    #     ['clear', ['20']],
    #     ['load', [-93, '22']],
    #     ['multiply', [-64, '51', '99']],
    #     ['nop', []],
    #     ['add', ['27', '50', '49']],
    #     ['dec', ['5']],
    #     ['nop', []],
    #     ['jump', ['96']]
    # ]

    pprint(program)
    comp.load_program(program)
    comp.run_program()

    pprint(dict([key, location.value] for key, location in comp.memory.iteritems()))
    pprint(comp.output_queue)


if __name__ == '__main__':
    main()