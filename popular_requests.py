#---- import some libraries ----#
import os
from pathlib import Path
import mysql.connector
import dotenv
#-------------------------------#

# creating variable to decorate
frame = '----------------------------------------------------------------------------------------------------'

# loading datas from .env
dotenv.load_dotenv(Path('.env')) # loading .env file with db connection datas


# creating function to make connection to database with read and write
def connect_db_write():
    try:
        write_conn = mysql.connector.connect(
            host=os.getenv('dbw_host'),
            user=os.getenv('dbw_user'),
            password=os.getenv('dbw_pass'),
            database='group_111124_fp_Klymentii_Taran'
        )

        if write_conn.is_connected():
            # print("[ Successful connected to DataBase ]".center(100, "-"))
            return write_conn
        else:
            print(frame, '[ FAILED TO CONNECT TO DATABASE ]'.center(100, '-'), frame, sep="\n")
            return None

    except Exception as err:
        return f'>> Error | {err}'.center(100, "-")


connection_write = connect_db_write()
if isinstance(connection_write, mysql.connector.connection_cext.CMySQLConnection):

    # creating cursor to use connection to database
    cursor_write = connection_write.cursor(buffered=True)


    # creating function to look top 10 name requests
    def top_name_requests():
        # showing top 10 requests
        raw_top_names = """select * from history_search_by_name order by counter desc limit 10"""
        cursor_write.execute(raw_top_names)
        raw_reqs = cursor_write.fetchmany(10)
        all_reqs = [[id, text, counter] for id, text, counter in raw_reqs]
        for request in all_reqs:
            for id, text, counter in [request]:
                print(f'>> ID: {id}\n\tEntered text: {text}\n')
        print(f'\n{frame}\n')

        # creating dictionary for easier search
        all_reqs_dict = {}
        for req in all_reqs:
            for id, text, counter in [req]:
                all_reqs_dict[id] = text

        # creating loop to close variant of search
        top_name_loop = ""
        while not top_name_loop:
            # creating ask variable to search by any request
            user_choice = input(f'\nDo you want to search by popular name requests? [y/n] ').strip().lower()
            # close function
            if user_choice == 'n':
                print('', '---{ Closing top of name requests }---'.center(100), frame, '', sep='\n')
                return None

            # search top requests
            if user_choice == 'y':
                print('', frame, '---[ Searching top of requests ]---'.center(100), sep='\n')

                # creating loop to choose a number of request
                selected_request_number = ""
                while not selected_request_number:
                    request_number = input(f'\nEnter a number of request to search for: ')
                    try:
                        request_number = int(request_number)
                    except ValueError:
                        print('', '>> Enter a number << '.center(100, '-'), sep='\n')

                    if request_number in all_reqs_dict:
                        selected_request_number = request_number
                        break

                selected_request = all_reqs_dict[selected_request_number]

                return selected_request


    # creating function to look top 10 years requests
    def top_year_requests():
        # showing top 10 requests
        raw_top_years = """select * from history_search_by_year order by counter desc limit 10"""
        cursor_write.execute(raw_top_years)
        raw_reqs = cursor_write.fetchmany(10)
        all_reqs = [[id, one_year, first_year, last_year, counter] for id, one_year, first_year, last_year, counter in raw_reqs]
        for request in all_reqs:
            for id, one_year, first_year, last_year, counter in [request]:
                print(f'>> ID: {id}\n\tEntered year: {one_year}\n\tFirst year: {first_year}\n\tLast year: {last_year}\n')
        print(f'\n{frame}\n')

        all_reqs_one_year_dict = {}
        for request in all_reqs:
            for id, one_year, first_year, last_year, counter in [request]:
                if first_year is None and last_year is None:
                    all_reqs_one_year_dict[id] = one_year

        all_reqs_more_years_dict = {}
        for request in all_reqs:
            for id, one_year, first_year, last_year, counter in [request]:
                if one_year is None:
                    all_reqs_more_years_dict[id] = {"fy": first_year, "ly": last_year}

        # creating ask variables to search by any request
        user_choice = input(f'Do you want to search by popular year requests? [y/n] ').strip().lower()
        # close function
        if user_choice == 'n':
            print('', '---{ Closing top of name requests }---'.center(100), frame, '', sep='\n')
            return None

        if user_choice == 'y':
            print('', frame, '---[ Searching top of requests ]---'.center(100), sep='\n')

            # creating variable to choose a request
            selected_request_number = ""
            while not selected_request_number:
                request_number = input(f'\nEnter a number of request to search for: ')
                try:
                    request_number = int(request_number)
                except ValueError:
                    print('', '>> Enter a number << '.center(100, '-'), sep='\n')

                if request_number in all_reqs_one_year_dict:
                    selected_request_number = all_reqs_one_year_dict[request_number]
                    break
                elif request_number in all_reqs_more_years_dict:
                    selected_request_number = all_reqs_more_years_dict[request_number]
                    break

            return selected_request_number


    # creating function to look top 10 categories requests
    def top_category_requests():
        # showing top 10 requests
        raw_top_category = """select * from history_search_by_category order by counter desc limit 10"""
        cursor_write.execute(raw_top_category)
        raw_reqs = cursor_write.fetchmany(10)
        all_reqs = [[table_id, name, counter] for table_id, category_id, name, counter in raw_reqs]
        for request in all_reqs:
            for table_id, name, counter in [request]:
                print(f'>> ID: {table_id}\n\tEntered category: {name}\n')
        print(f'\n{frame}\n')

        category_dict = {}
        for request in all_reqs:
            for table_id, name, counter in [request]:
                category_dict[table_id] = name

        # creating loop for ask variables to search by any request
        top_category_loop = ""
        while not top_category_loop:
            user_choice = input(f'Do you want to search by popular year requests? [y/n] ').strip().lower()
            # close function
            if user_choice == 'n':
                top_category_loop = True
                print('', '---{ Closing top of category requests }---'.center(100), frame, '', sep='\n')
                return None

            elif user_choice == 'y':
                print('', frame, '---[ Searching top of requests ]---'.center(100), sep='\n')

                # creating variables to choose a request
                selected_request_number = ""
                while not selected_request_number:
                    while True:
                        request_number = input(f'\nEnter a number of request to search for: ')
                        try:
                            request_number = int(request_number)
                            break
                        except ValueError:
                            print('', '>> Enter a number << '.center(100, '-'), sep='\n')

                    if request_number in category_dict:
                        selected_request_number = category_dict[request_number]
                    break

                return selected_request_number


    # creating function to look top 10 years and categories requests
    def top_year_category_requests():
        # showing top 10 requests
        raw_year_year_category = """select * from history_search_by_year_category order by counter desc limit 10"""
        cursor_write.execute(raw_year_year_category)
        raw_reqs = cursor_write.fetchmany(10)
        all_reqs = [[table_id, year, first_year, last_year, entered_category_id, entered_category_name, counter]
                    for table_id, year, first_year, last_year, entered_category_id, entered_category_name, counter in raw_reqs]
        for request in all_reqs:
            for table_id, year, first_year, last_year, entered_category_id, entered_category_name, counter in [request]:
                print(f'>> ID: {table_id}\n\tYear: {year}\n\tFirst Year: {first_year}\n\tLast Year: {last_year}\n\tEntered category name: {entered_category_name}\n')
        print(f'\n{frame}\n')

        # creating requirements for function
        all_reqs_one_year_dict = {}
        for request in all_reqs:
            for table_id, year, first_year, last_year, entered_category_id, entered_category_name, counter in [request]:
                if first_year is None and last_year is None:
                    all_reqs_one_year_dict[table_id] = year

        all_reqs_more_years_dict = {}
        for request in all_reqs:
            for table_id, year, first_year, last_year, entered_category_id, entered_category_name, counter in [request]:
                if year is None:
                    all_reqs_more_years_dict[table_id] = {"fy": first_year, "ly": last_year}

        all_table_id = []
        for request in all_reqs:
            all_table_id.append(request[0])

        # creating category dictionary
        category_dict = {}
        for request in all_reqs:
            for table_id, year, first_year, last_year, entered_category_id, entered_category_name, counter in [request]:
                category_dict[table_id] = entered_category_name

        # creating loop for ask variables to search by any request
        top_year_category_loop = ""
        while not top_year_category_loop:
            # creating ask variables to search by any request
            user_choice = input(f'Do you want to search by popular year requests? [y/n] ').strip().lower()
            # close function
            if user_choice == 'n':
                print('', '---{ Closing top of years & categories requests }---'.center(100), frame, '', sep='\n')
                top_year_category_loop = True
                return None

            if user_choice == 'y':
                print('', frame, '---[ Searching top of requests ]---'.center(100), sep='\n')

                # creating ask loop to re-search movies by using different top requests
                extra_option = ""
                while not extra_option:
                    print(f'\nWhich option do you want to use?\n\n1 - Search by existed request\n2 - Search by using different requests\n')
                    ask_for_extra_option = input(f'Enter a number of option: ')

                    # variant if searching by existed request
                    if ask_for_extra_option == '1':
                        print('', '-- > Looking for existed request < --'.center(100), sep='\n')
                        # creating variables for years and categories to choose a request
                        selected_year_requests = ""
                        selected_category_request = ""

                        # creating loop to get one request
                        getting_request = ""
                        while not getting_request:
                            request_number = input(f'\nEnter a number of request to search for: ')
                            try:
                                request_number = int(request_number)
                            except ValueError:
                                print('', '>> Enter a number << '.center(100, '-'), sep='\n')

                            # checking if entered request number in possible table id`s
                            if request_number in all_table_id:
                                cursor_write.execute('select * from history_search_by_year_category where id = %s', (request_number,))
                                founded_request = cursor_write.fetchone()
                                # unpacking founded result
                                for table_id, year, first_year, last_year, entered_category_id, entered_category_name, counter in [founded_request]:
                                    if year is None:
                                        selected_year_requests = {"fy": first_year, "ly": last_year}
                                        selected_category_request = entered_category_name
                                        mixed_request = {"year": selected_year_requests, "category": selected_category_request}
                                        top_year_category_loop = True
                                        return mixed_request

                                    elif first_year is None and last_year is None:
                                        selected_year_requests = year
                                        selected_category_request = entered_category_name
                                        mixed_request = {"year": selected_year_requests, "category": selected_category_request}
                                        top_year_category_loop = True
                                        return mixed_request

                    # variant if searching by mixed request
                    if ask_for_extra_option == '2':
                        # creating variables for years and categories to choose a request
                        selected_year_requests = ""
                        while not selected_year_requests:
                            print('', '-- > Looking for different requests < --'.center(100), sep='\n')
                            request_number = input(f'\nEnter a number of request for years to search for: ')
                            try:
                                request_number = int(request_number)
                            except ValueError:
                                print('>> Enter a number << '.center(100, '-'), '', sep='\n')

                            if request_number in all_reqs_one_year_dict:
                                selected_year_requests = all_reqs_one_year_dict[request_number]
                                top_year_category_loop = True
                                break
                            elif request_number in all_reqs_more_years_dict:
                                selected_year_requests = all_reqs_more_years_dict[request_number]
                                top_year_category_loop = True
                                break

                        selected_category_request = ""
                        while not selected_category_request:
                            request_number = input(f'\nEnter a number of request for category to search for: ')
                            try:
                                request_number = int(request_number)
                            except ValueError:
                                print('', '>> Enter a number << '.center(100, '-'), sep='\n')

                            if request_number in category_dict:
                                selected_category_request = category_dict[request_number]
                                top_year_category_loop = True
                                break

                        mixed_request = {"year": selected_year_requests, "category": selected_category_request}
                        return mixed_request


    # closing connection
    def close_db_write():
        cursor_write.close()
        connection_write.close()

else:
    print(frame, '[ FAILED TO CONNECT TO DATABASE ]'.center(100, '-'), frame, sep="\n")