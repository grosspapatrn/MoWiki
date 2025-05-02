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
##################### main code #####################
    # creating cursor to use connection to database
    cursor_write = connection_write.cursor(buffered=True)

    # creating function to save history of searching by name
    def history_by_name(data):
        # creating variables to save or update counter words
        check_request = 'select * from history_search_by_name where entered_text = %s'
        save_request = 'insert into history_search_by_name (entered_text) values (%s)'
        update_request = 'update history_search_by_name set counter = counter + 1 where entered_text = %s'

        # creating check and write method
        cursor_write.execute(check_request, (data,))
        all_rows = cursor_write.fetchall()
        if len(all_rows) == 0:
            cursor_write.execute(save_request, (data,))
        else:
            cursor_write.execute(update_request, (data,))

        # saving all entered datas
        connection_write.commit()


    # creating function to save history of searching by category
    def history_by_category(categ_id, categ_name):
        # creating variables to save or update counter words
        check_request = 'select * from history_search_by_category where entered_category_id = %(id)s and entered_category_name = %(name)s'
        save_request = 'insert into history_search_by_category (entered_category_id, entered_category_name) values (%(id)s, %(name)s)'
        update_request = 'update history_search_by_category set counter = counter + 1 where entered_category_id = %(id)s and entered_category_name = %(name)s'

        # creating check and write method
        cursor_write.execute(check_request, {'id': categ_id, 'name': categ_name})
        all_rows = cursor_write.fetchall()
        if len(all_rows) == 0:
            cursor_write.execute(save_request, {'id': categ_id, 'name': categ_name})
        else:
            cursor_write.execute(update_request, {'id': categ_id, 'name': categ_name})

        # saving all entered datas
        connection_write.commit()


    # creating function to save history of searching by one year
    def history_by_one_year(data):
        # creating variables to save or update counter words
        check_request = 'select * from history_search_by_year where one_year = %s'
        save_request = 'insert into history_search_by_year (one_year) values (%s)'
        update_request = 'update history_search_by_year set counter = counter + 1 where one_year = %s'

        # creating check and write method
        cursor_write.execute(check_request, (data,))
        all_rows = cursor_write.fetchall()
        if len(all_rows) == 0:
            cursor_write.execute(save_request, (data,))
        else:
            cursor_write.execute(update_request, (data,))

        # saving all entered datas
        connection_write.commit()


    # creating function to save history of searching by more years
    def history_by_more_years(first_year, last_year):
        # creating variables to save or update counter words
        check_request = 'select * from history_search_by_year where first_year = %(first_year)s and last_year = %(last_year)s'
        save_request = 'insert into history_search_by_year (first_year, last_year) values (%(first_year)s, %(last_year)s)'
        update_request = 'update history_search_by_year set counter = counter + 1 where first_year = %(first_year)s and last_year = %(last_year)s'

        # creating check and write method
        cursor_write.execute(check_request, {'first_year': first_year, 'last_year': last_year})
        all_rows = cursor_write.fetchall()
        if len(all_rows) == 0:
            cursor_write.execute(save_request, {'first_year': first_year, 'last_year': last_year})
        else:
            cursor_write.execute(update_request, {'first_year': first_year, 'last_year': last_year})

        # saving all entered datas
        connection_write.commit()


    # creating function to save history of searching by one year and category
    def history_by_one_year_category(year, category_id, category_name):
        # creating variables to save or update counter words
        check_request = 'select * from history_search_by_year_category where year = %(year)s and entered_category_id = %(category_id)s and entered_category_name = %(category_name)s'
        save_request = 'insert into history_search_by_year_category (year, entered_category_id, entered_category_name) values (%(year)s, %(category_id)s, %(category_name)s)'
        update_request = 'update history_search_by_year_category set counter = counter + 1 where year = %(year)s and entered_category_id = %(category_id)s and entered_category_name = %(category_name)s'

        # creating check and write method
        cursor_write.execute(check_request, {'year': year, 'category_id': category_id, 'category_name': category_name})
        all_rows = cursor_write.fetchall()
        if len(all_rows) == 0:
            cursor_write.execute(save_request, {'year': year, 'category_id': category_id, 'category_name': category_name})
        else:
            cursor_write.execute(update_request, {'year': year, 'category_id': category_id, 'category_name': category_name})

        # saving all entered datas
        connection_write.commit()


    # creating function to save history of searching by more years and category
    def history_by_more_year_category(first, last, category_id, category_name):
        # creating variables to save or update counter words
        check_request = 'select * from history_search_by_year_category where first_year = %(first_year)s and last_year = %(last_year)s and entered_category_id = %(category_id)s and entered_category_name = %(category_name)s'
        save_request = 'insert into history_search_by_year_category (first_year, last_year, entered_category_id, entered_category_name) values (%(first_year)s, %(last_year)s, %(category_id)s, %(category_name)s)'
        update_request = 'update history_search_by_year_category set counter = counter + 1 where first_year = %(first_year)s and last_year = %(last_year)s and entered_category_id = %(category_id)s and entered_category_name = %(category_name)s'

        # creating check and write method
        cursor_write.execute(check_request, {'first_year': first, 'last_year': last, 'category_id': category_id, 'category_name': category_name})
        all_rows = cursor_write.fetchall()
        if len(all_rows) == 0:
            cursor_write.execute(save_request, {'first_year': first, 'last_year': last, 'category_id': category_id, 'category_name': category_name})
        else:
            cursor_write.execute(update_request, {'first_year': first, 'last_year': last, 'category_id': category_id, 'category_name': category_name})

        # saving all entered datas
        connection_write.commit()

#####################################################

    # closing connection
    def close_db_write():
        cursor_write.close()
        connection_write.close()


else:
    print(frame, '[ FAILED TO CONNECT TO DATABASE ]'.center(100, '-'), frame, sep="\n")