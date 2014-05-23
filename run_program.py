from Computer import Computer


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

    comp.run_program()


if __name__ == '__main__':
    main()