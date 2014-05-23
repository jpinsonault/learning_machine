from Computer import Computer
from InstructionGenerator import Generator
from pprint import pprint


def main():
    comp = Computer()

    comp.load_program([
        ["load",         [3, "4"]],
        ["load",         [5, "2"]],
        ["load",         [-3, "3"]],
        ["add",          ["1", "2", "1"]],
        ["dec",          ["4"]],
        ["jump_if_zero", ["4", 2]],
        ["jump",         ["3"]],
        ["print_mem",    ["1"]],
    ])


    program = [
        ["load",         [3, "4"]],
        ["load",         [5, "2"]],
        ["load",         [-3, "3"]],
        ["add",          ["1", "2", "1"]],
        ["dec",          [4]],
        ["jump_if_zero", ["4", 2]],
        ["jump",         ["3"]],
        ["print_mem",    ["1"]],
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

    pprint(dict(comp.memory))


if __name__ == '__main__':
    main()