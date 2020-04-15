# !/usr/bin/python
# version 1.0.0.0

from libs.colors import COLORS
from os.path import dirname, realpath
from subprocess import check_output, CalledProcessError, call
from os import devnull
from terminaltables import AsciiTable
from mysql.connector import connect
from libs.logo import PrintLogo
from sys import argv


devnull = open(devnull, 'w')
colors = COLORS()
program_path = dirname(realpath(__file__))
activated_option = [colors.ULINE + colors.BOLD + 'ykey' + colors.RESET]
logo_printer = PrintLogo(program_path)

global_dict = {
    'colors' : colors,
    'program_path' : program_path,
    'activated_option' : activated_option,
    'logo_printer' : logo_printer,
}


# definitions fo global program

def execfile_y(file_name, globals_variables):
    exec(compile(open(file_name, "rb").read(), file_name, 'exec'), globals_variables)



# defifnition for main program

def print_main_options():
    options = {
        'generator': 'Use this option to generate keyloggers',
        'listener': 'Use this options to read logged keys of all victims'
    }

    table_data = [[colors.BOLD + 'Option', colors.BOLD + 'Description' + colors.RESET]]
    for option in options:
        row_data = [option, options[option]]
        table_data.append(row_data)

    table = AsciiTable(table_data)
    print(table.table, end='\n\n')


# the main program

def main():
    global program_path
    global activated_option
    global global_dict
    # firstly clear the screen
    call('clear', shell=True)
    logo_printer.print()

    # then enter the infinite command input section
    while True:
        # Input the command
        command = input("".join(activated_option) + ' > ')

        # if the command is use generation
        if command == 'use generator':
            activated_option.append(' {}generate({}KeyLogger{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            execfile_y('libs/generator.py', global_dict)

        # if the command is to activate the listenet
        elif command == 'use listener':
            activated_option.append(' {}listen({}KeyLogger{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            execfile_y('libs/listener.py', global_dict)

        # if the command is options or show options
        elif command == 'options' or command == 'show options':
            print_main_options()

        # if the ommcand is clear clrat the screen
        elif command == 'clear':
            call('clear', shell=True)

        # if the command is exit or quit breake the progrm
        elif command == 'quit' or command == 'exit':
            break

        elif command == 'help':
            logo_printer.print_help()

        else:
            print(command)
            print(colors.Red + '[-]Invalid command' + colors.RESET)


def check_out_arguments():
    """
    DOCSTRING: this function will look up to the arguments user gives
    """
    argument_dictionary = {
        '--help': logo_printer.print_help,
        '--logo': logo_printer.print,
        '--version': lambda :print('1.0.0.0')
    }
    try:
        argument_dictionary[argv[1]]()
    except KeyError:
        print('[-]Invalid Command')


if __name__ == '__main__':

    try:
        check_out_arguments()
    except IndexError:
        main()
        exit(0)