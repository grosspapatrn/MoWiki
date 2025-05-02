#---- import some libraries ----#
import os
from pathlib import Path
import mysql.connector
import dotenv

from popular_requests import *
from write_option import *
#-------------------------------#

def main():
    # creating variable to decorate
    frame = '----------------------------------------------------------------------------------------------------'

    # loading datas from .env
    dotenv.load_dotenv(Path('.env')) # loading .env file with db connection datas


    # creating function to make connection to database only with read
    def connect_db_read():
        try:
            read_conn = mysql.connector.connect(
                host=os.getenv('dbr_host'),
                user=os.getenv('dbr_user'),
                password=os.getenv('dbr_pass'),
                database='sakila'
            )

            if read_conn.is_connected():
                print("[ Successful connected to DataBase ]".center(100, "-"))
                return read_conn
            else:
                print(frame, '[ FAILED TO CONNECT TO DATABASE ]'.center(100, '-'), frame, sep="\n")
                return None

        except Exception as err:
            return f'>> Error | {err}'.center(100, "-")

    # making variable for connection
    connection_read = connect_db_read()
    # checking if variable of connection exist and variable fits module
    if isinstance(connection_read, mysql.connector.connection_cext.CMySQLConnection):

        # making cursor for readable database. using parameter buffered to avoid problems with "fetchmany"
        cursor_read = connection_read.cursor(buffered=True)

        # creating loop to ask user
        print('', frame, 'Welcome to "MoWiki"!'.center(100), frame, sep='\n')
        close_app = ""
        while not close_app:
            print('', 'What do you want to watch? :)'.center(100), sep='\n')
            print(f'\n1 - Search movie by name\n2 - Search by category and / or release year\n3 - Search by popular requests')
            ask_for_close_app = input('\nEnter a number of option or press "enter" to close app: ').strip().upper()#.split(" ")

            # creating exit loop check
            if ask_for_close_app == "":
                close_app = True
                print('', frame, 'Thank you for using "MoWiki". Have a nice day!'.center(100), frame, sep='\n')
                break

            # creating condition to search movies by name
            if ask_for_close_app == "1":
                print(f'\n{frame}\n\n', '---[ Your choose: search by name ]---'.center(100))

                # create loop to search film by name
                again_search = ""
                while not again_search:
                    title_name_ask = input('\nGood, so than type movies name here or press enter to quit search: ').strip().upper()
                    # exit from loop
                    if title_name_ask == "":
                        again_search = True
                        print('', '~~{ Exit search by title of movie }~~'.center(100), frame, sep='\n')
                        break

                    # making barrier of min letters to enter
                    if len(title_name_ask) < 3:
                        print('', ' >> ERROR | Enter 3 and more letters << '.center(100, '-'), '', sep='\n')

                    # if entered data fit
                    else:
                        raw_title_input = f"""select f.title, f.release_year year, c.name category_name from film f
                                                join film_category fc on f.film_id = fc.film_id
                                                join category c on fc.category_id = c.category_id
                                                where title like %s
                                                order by f.title;"""
                        cursor_read.execute(raw_title_input, (f"%{title_name_ask}%",))
                        raw_data = cursor_read.fetchall()

                        # saving entered data to database
                        history_by_name(title_name_ask)

                        # variable if no data founded
                        if len(raw_data) == 0:
                            print('', ' >> ERROR | No movie was found << '.center(100, '-'), '', sep='\n')

                        # creating variation if there are founded less than 10 movies
                        elif len(raw_data) <= 10:
                            founded_data = [[title, year, category] for title, year, category in raw_data]
                            print(f'\n{frame}\n\nThere was {len(raw_data)} movies found on "{title_name_ask}":\n')
                            for film in founded_data:
                                for title, year, category in [film]:
                                    print(f'>> Title: {title} \n\tYear: {year} \n\tCategory: {category}\n')
                            print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')

                        # creating variation if more than 10 movies was found
                        elif len(raw_data) > 10:
                            print(f'\n{frame}\n\nThere was {len(raw_data)} movies found on "{title_name_ask}".')
                            cursor_read.execute(raw_title_input, (f"%{title_name_ask}%",))
                            end_of_query = ""
                            while not end_of_query:
                                raw_every_10_films = cursor_read.fetchmany(10)
                                if len(raw_every_10_films) == 0:
                                    print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                    break

                                # showing next films in queue
                                every_10_films = [[title, year, category] for title, year, category in raw_every_10_films]
                                print(f'\nShowing {len(every_10_films)} movies:\n')
                                for film in every_10_films:
                                    for title, year, category in [film]:
                                        print(f'>> Title: {title} \n\tYear: {year} \n\tCategory: {category}\n')

                                # creating variable to show more movies
                                while True:
                                    ask_to_show_more = input('|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                    if ask_to_show_more == "y":
                                        break
                                    elif ask_to_show_more == "n":
                                        end_of_query = True
                                        print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                        break

                    # loop to research another movie
                    while True:
                        ask_to_research = input('|-> Do you want to search movie again? [y/n] ').strip().lower()
                        if ask_to_research == "n":
                            again_search = True
                            print('', '~~{ Exit search by title of movie }~~'.center(100), frame, sep='\n')
                            break
                        elif ask_to_research == "y":
                            break


            # creating condition to search films by category and year
            if ask_for_close_app == "2":
                print(f'\n{frame}\n\n', '---[ Your choose: search by category and year ]---'.center(100), '\n')

                # create loop to search film by name
                again_search = ""
                while not again_search:
                    print('How do you want to search for? \n>> 1 - Search by category\n>> 2 - Search by year\n>> 3 - Search by category and year\n')
                    select_input = input('-> Enter a number of option or press enter to exit: ').strip().lower()

                    # creating exit from loop
                    if select_input == '':
                        again_search = True
                        print('', '~~{ Exit search by category and year of movie }~~'.center(100), frame, sep='\n')
                        break


                    # search by category
                    elif select_input == '1':
                        print(f'\n{frame}\n\n', '---[ Search by category of movie ]---'.center(100), '\n')

                        # showing all possible category
                        counted_category_query = """select c.category_id, c.name, count(f.title) amount_of_movies from film f
                                                    join film_category fc on f.film_id = fc.film_id
                                                    join category c on fc.category_id = c.category_id
                                                    group by c.name order by c.category_id;"""
                        cursor_read.execute(counted_category_query)
                        raw_categories = cursor_read.fetchall()
                        # creating variable with id, name and amount of filmes grouped by category
                        all_categories = [[cid, name, amount_of_movies] for cid, name, amount_of_movies in raw_categories]

                        # creating dictionary with key:id and value:name of category
                        raw_id_name_category = [[cid, name] for cid, name, amount_of_movies in raw_categories]
                        category_dict = {}
                        for cid, name in raw_id_name_category:
                            category_dict[cid] = name

                        # showing all possible categories to search
                        print(f'\nAll possible movie categories:\n')
                        for category in all_categories:
                            for cid, name, amount_of_movies in [category]:
                                print(f'>> Name: {name}\n\tCategory ID: {cid}\n\tAmount of movies: {amount_of_movies}\n')
                        print(frame)

                        # creating input variable for category
                        category_loop = ""
                        while not category_loop:
                            selected_category = input('Choose a category by entering a number of category or press enter to exit: ')

                            # creating exit from loop
                            if selected_category == "":
                                category_loop = True
                                print('', '~~{ Exit search by category of movie }~~'.center(100), frame, sep='\n')
                                break

                            # making try-except method to convert possible stroke into number
                            try:
                                selected_category = int(selected_category)
                            except ValueError:
                                print('', ' >> ERROR | Enter a number of category << '.center(100, '-'), '', sep='\n')
                                continue

                            # checking if entered data has an int value and checking if it is in possible dictionary
                            if isinstance(selected_category, int):
                                if selected_category in category_dict:
                                    # creating request to database
                                    raw_category_query = """select f.title, f.release_year year from film f
                                                            join film_category fc on f.film_id = fc.film_id
                                                            join category c on fc.category_id = c.category_id and c.category_id = %s
                                                            order by f.title;"""
                                    cursor_read.execute(raw_category_query, (selected_category,))
                                    raw_category_data = cursor_read.fetchall()

                                    # taking category name to save in out database
                                    category_name = category_dict[selected_category]

                                    # saving datas to database
                                    history_by_category(selected_category, category_name)

                                    # creating variation if there are founded less than 10 movies
                                    if len(raw_category_data) <= 10:
                                        all_movies_in_category = [[name, year] for name, year in raw_category_data]
                                        print(f'\n{frame}\n\nAll movies {len(raw_category_data)} found in category {category_dict[selected_category]}:\n')
                                        for movie in all_movies_in_category:
                                            for name, year in [movie]:
                                                print(f'>> Name: {name}\n\tYear: {year}\n')
                                        print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                                        category_loop = True
                                        break

                                    # creating variation if more than 10 movies was found
                                    elif len(raw_category_data) > 10:
                                        print(f'\n{frame}\n\nThere was {len(raw_category_data)} movies found on category "{category_dict[selected_category]}":')
                                        cursor_read.execute(raw_category_query, (selected_category,))
                                        end_of_query = ""
                                        while not end_of_query:
                                            raw_every_10_movies = cursor_read.fetchmany(10)
                                            if len(raw_every_10_movies) == 0:
                                                category_loop = True
                                                print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                                break

                                            # showing next films in queue
                                            every_10_movies = [[name, year] for name, year in raw_every_10_movies]
                                            print(f'\nShowing {len(every_10_movies)} movies:\n')
                                            for movie in every_10_movies:
                                                for name, year in [movie]:
                                                    print(f'>> Name: {name}\n\tYear: {year}\n')

                                            # creating variable to show more movies
                                            while True:
                                                ask_to_show_more = input(
                                                    '|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                                if ask_to_show_more == "y":
                                                    break
                                                elif ask_to_show_more == "n":
                                                    end_of_query = True
                                                    category_loop = True
                                                    print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                                    break

                                # variable if no data founded
                                else:
                                    print('', ' >> ERROR | No category found << '.center(100, '-'), '', sep='\n')


                    # option to search by years
                    elif select_input == '2':
                        print(f'\n{frame}\n\n', '---[ Search by year of movie ]---'.center(100), '\n')

                        # creating question for user to use search only by one year or more years
                        year_option_choice_loop = ""
                        while not year_option_choice_loop:
                            print(f'Do you want to search by one year or more years? \n\n>> 1 - Search by one year\n>> 2 - Search by more years\n')
                            year_option_choice = input(f'Enter a number of option or press enter to exit: ').strip().lower()

                            # exit program
                            if year_option_choice == "":
                                year_option_choice_loop = True
                                print('', '~~{ Exit search by years of movie }~~'.center(100), frame, '', sep='\n')
                                break


                            # option to search by one year
                            if year_option_choice == "1":
                                print('', '---[ Your choice: search by one year ]---'.center(100, '-'), '', sep='\n')

                                # showing all possible years of movies
                                cursor_read.execute('select release_year from film group by release_year order by release_year')
                                raw_year_data = cursor_read.fetchall()
                                all_years = [year[0] for year in raw_year_data]
                                print(f'All possible year to search:\n')
                                for year in all_years:
                                    print(f'>> {year}')

                                # creating loop to get movies by years
                                year_loop = ""
                                while not year_loop:
                                    selected_year = input('\nChoose a year: ')
                                    try:
                                        selected_year = int(selected_year)
                                    except ValueError:
                                        print('', ' >> ERROR | Enter a number << '.center(100, '-'), '', sep='\n')
                                        continue
                                    if isinstance(selected_year, int):
                                        if selected_year in all_years:
                                            # creating request to database
                                            raw_year_query = """select f.title, f.release_year year, c.name category_name from film_category fc
                                                                join category c on fc.category_id = c.category_id
                                                                join film f on f.film_id = fc.film_id and release_year = %s
                                                                order by title;"""
                                            cursor_read.execute(raw_year_query, (selected_year,))
                                            raw_year_data = cursor_read.fetchall()

                                            # saving data to database
                                            history_by_one_year(selected_year)

                                            # creating variation if there are founded less than 10 movies
                                            if len(raw_year_data) <= 10:
                                                all_movies_by_year = [[name, category] for name, year, category in raw_year_data]
                                                print(f'\n{frame}\n\nAll movies {len(raw_year_data)} found by year "{selected_year}":\n')
                                                for movie in all_movies_by_year:
                                                    for name, category in [movie]:
                                                        print(f'>> Name: {name}\n\tCategory: {category}\n')
                                                print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                                                year_loop = True
                                                break

                                            # creating variation if more than 10 movies was found
                                            elif len(raw_year_data) > 10:
                                                print(f'\n{frame}\n\nThere was {len(raw_year_data)} movies found on year "{selected_year}":\n')
                                                cursor_read.execute(raw_year_query, (selected_year,))
                                                end_of_query = ""
                                                while not end_of_query:
                                                    raw_every_10_movies = cursor_read.fetchmany(10)
                                                    if len(raw_every_10_movies) == 0:
                                                        year_loop = True
                                                        print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                                        break

                                                    # showing next films in queue
                                                    every_10_movies = [[name, category] for name, year, category in raw_every_10_movies]
                                                    print(f'\nShowing {len(every_10_movies)} movies:\n')
                                                    for movie in every_10_movies:
                                                        for name, category in [movie]:
                                                            print(f'>> Name: {name}\n\tCategory: {category}\n')

                                                    # creating variable to show more movies
                                                    while True:
                                                        ask_to_show_more = input(
                                                            '|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                                        if ask_to_show_more == "y":
                                                            break
                                                        elif ask_to_show_more == "n":
                                                            end_of_query = True
                                                            year_loop = True
                                                            print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                                            break

                            # option to search by more years
                            elif year_option_choice == "2":
                                print('', '---[ Your choice: search by more years ]---'.center(100, '-'), '', sep='\n')

                                # showing all possible years of movies
                                cursor_read.execute('select release_year from film group by release_year order by release_year')
                                raw_year_data = cursor_read.fetchall()
                                all_years = [year[0] for year in raw_year_data]
                                print(f'All possible year to search:\n')
                                for year in all_years:
                                    print(f'>> {year}')

                                # creating variables for user to search movies by years and category
                                first_year = ""
                                last_year = ""
                                while True:
                                    ask_year1 = input('\nChoose a first year: ')
                                    ask_year2 = input('Choose a last year: ')
                                    # creating try-except method to convert stroke into int
                                    try:
                                        ask_year1 = int(ask_year1)
                                        ask_year2 = int(ask_year2)
                                    except ValueError:
                                        print('>> Enter a number << '.center(100, '-'), '', sep='\n')

                                    # reassignment of variables
                                    if ask_year1 and ask_year2 in all_years:
                                        first_year = ask_year1
                                        last_year = ask_year2
                                        break

                                # creating raw query to make request by more years
                                raw_more_year_query = """select f.title, f.release_year year, c.name category_name from film_category fc
                                                         join category c on fc.category_id = c.category_id
                                                         join film f on f.film_id = fc.film_id and release_year between %(first_year)s and %(last_year)s
                                                         order by title;"""
                                cursor_read.execute(raw_more_year_query, {'first_year': first_year, 'last_year': last_year})
                                all_selected_years = cursor_read.fetchall()

                                # saving all datas in database
                                history_by_more_years(first_year, last_year)

                                # creating variation if there are founded less than 10 movies
                                if len(all_selected_years) <= 10:
                                    all_movies_by_year = [[name, year, category] for name, year, category in all_selected_years]
                                    print(f'\n{frame}\n\nAll movies {len(all_selected_years)} found on years "{first_year} - {last_year}":\n')
                                    for movie in all_movies_by_year:
                                        for name, year, category in [movie]:
                                            print(f'>> Name: {name}\n\tYear: {year}\n\tCategory: {category}\n')
                                    print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                                    year_option_choice_loop = True
                                    break

                                # creating variation if more than 10 movies was found
                                elif len(all_selected_years) > 10:
                                    print(f'\n{frame}\n\nThere was {len(all_selected_years)} movies found on years "{first_year} - {last_year}":')
                                    cursor_read.execute(raw_more_year_query,{'first_year': first_year, 'last_year': last_year})
                                    end_of_query_more_year = ""
                                    while not end_of_query_more_year:
                                        raw_every_10_movies_more_years = cursor_read.fetchmany(10)
                                        if len(raw_every_10_movies_more_years) == 0:
                                            year_option_choice_loop = True
                                            print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                            break

                                        # showing next films in queue
                                        every_10_movies = [[name, year, category] for name, year, category in raw_every_10_movies_more_years]
                                        print(f'\nShowing {len(every_10_movies)} movies:\n')
                                        for movie in every_10_movies:
                                            for name, year, category in [movie]:
                                                print(f'>> Name: {name}\n\tYear: {year}\n\tCategory: {category}\n')

                                        # creating variable to show more movies
                                        while True:
                                            ask_to_show_more = input('|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                            if ask_to_show_more == "y":
                                                break
                                            elif ask_to_show_more == "n":
                                                end_of_query_more_year = True
                                                print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                                break

                    # option to search by category and year
                    elif select_input == '3':
                        print(f'\n{frame}\n\n', '---[ Search by category and year ]---'.center(100), '\n')

                        # showing all possible year and category
                        cursor_read.execute('select release_year from film group by release_year;')
                        raw_year_datas = cursor_read.fetchall()
                        all_years = [year[0] for year in raw_year_datas]

                        cursor_read.execute('select category_id, name from category group by name;')
                        raw_category_names = cursor_read.fetchall()
                        raw_all_category = [[cid, category] for cid, category in raw_category_names]
                        all_categories = {}
                        for cid, category in raw_all_category:
                            all_categories[cid] = category

                        print(f'All possible year to search:\n')
                        for year in all_years:
                            print(f'>> {year}')

                        print(f'\nAll possible categories to search:\n')
                        for movie in raw_all_category:
                            for cid, category in [movie]:
                                print(f'>> Name: {category} \n\tCategory ID: {cid}\n')
                        print(f'{frame}\n')

                        # creating ask loop for user to use more than one year
                        choice_loop_year_category = ""
                        while not choice_loop_year_category:
                            print(f'Do you want to search by one year or more years? \n\n>> 1 - Search by one year\n>> 2 - Search by more years\n')
                            user_choice = input(f'Enter a number of option or press enter to exit: ').strip().lower()

                            # exit loop
                            if user_choice == "":
                                choice_loop_year_category = True
                                print('', '~~{ Exit search by category and years of movie }~~'.center(100), frame, sep='\n')
                                break

                            # option with one year
                            if user_choice == "1":
                                print('', '---[ Your choice: search by one year ]---'.center(100, '-'), '', sep='\n')

                                # creating variables for user to search movies by year and category
                                selected_year= ''
                                while True:
                                    ask_year = input('Choose a year to search for: ')
                                    # creating try-except method to convert stroke into int
                                    try:
                                        ask_year = int(ask_year)
                                    except ValueError:
                                        print('>> Enter a number << '.center(100, '-'), '', sep='\n')

                                    # reassignment existed variables
                                    if ask_year in all_years:
                                        selected_year = ask_year
                                        break

                                # creating loop to choose category
                                selected_category = ''
                                while True:
                                    ask_category = input('Choose a category by entering a number to search for: ')
                                    # creating try-except method to convert stroke into int
                                    try:
                                        ask_category = int(ask_category)
                                    except ValueError:
                                        print('>> Enter a number << '.center(100, '-'), '', sep='\n')
                                        continue
                                    # reassignment existed variables
                                    if ask_category in all_categories:
                                        selected_category = ask_category
                                        break

                                # creating request for search by one year and category
                                raw_year_category_request = """select f.title, f.release_year, c.name, c.category_id from film f
                                                            join film_category fc on f.film_id = fc.film_id
                                                            join category c on fc.category_id = c.category_id
                                                            where f.release_year = %(year)s and c.category_id = %(category)s
                                                            order by f.title;"""
                                cursor_read.execute(raw_year_category_request, {'year': selected_year, 'category': selected_category})
                                all_raw_datas = cursor_read.fetchall()

                                # making category name for saving in database
                                category_name = all_categories[selected_category]

                                # saving all datas in database
                                history_by_one_year_category(selected_year, selected_category, category_name)

                                if len(all_raw_datas) == 0:
                                    print('', ' >> No movies found << '.center(100, '-'), '', sep='\n')

                                # creating variation if there are founded less than 10 movies
                                elif len(all_raw_datas) <= 10:
                                    all_founded_movies = [name for name, year, category, cid in all_raw_datas]
                                    print(f'\n{frame}\n\nAll movies ({len(all_raw_datas)}) founded by year {selected_year} and category "{all_categories[selected_category]}":\n')
                                    for movie in all_founded_movies:
                                        print(f'>> {movie}\n')
                                    print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                                    choice_loop_year_category = True
                                    break

                                # creating variation if more than 10 movies was found
                                elif len(all_raw_datas) > 10:
                                    print(f'\n{frame}\n\nThere was {len(all_raw_datas)} movies founded by year {selected_year} and category "{all_categories[selected_category]}":\n')
                                    cursor_read.execute(raw_year_category_request, {'year': selected_year, 'category': selected_category})
                                    end_of_query_year_category = ""
                                    while not end_of_query_year_category:
                                        raw_every_10_movies = cursor_read.fetchmany(10)
                                        if len(raw_every_10_movies) == 0:
                                            end_of_query_year_category = True
                                            print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                            break

                                        # showing next films in queue
                                        every_10_movies = [name for name, year, category, cid in raw_every_10_movies]
                                        print(f'\nShowing {len(every_10_movies)} movies:\n')
                                        for movie in every_10_movies:
                                            print(f'>> {movie}\n')

                                        # creating variable to show more movies
                                        while True:
                                            ask_to_show_more = input('|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                            if ask_to_show_more == "y":
                                                break
                                            elif ask_to_show_more == "n":
                                                # end_of_query_year_category = True
                                                choice_loop_year_category = True
                                                print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                                break


                            # option with more years
                            if user_choice == "2":
                                print('', '---[ Your choice: search by more years ]---'.center(100, '-'), '', sep='\n')

                                # creating variables for user to search movies by years and category
                                first_year = ""
                                last_year = ""
                                while True:
                                    ask_year1 = input('Choose a first year: ')
                                    ask_year2 = input('Choose a last year: ')
                                    # creating try-except method to convert stroke into int
                                    try:
                                        ask_year1 = int(ask_year1)
                                        ask_year2 = int(ask_year2)
                                    except ValueError:
                                        print('>> Enter a number << '.center(100, '-'), '', sep='\n')
                                    # reassignment existed variables
                                    if ask_year1 and ask_year2 in all_years:
                                        first_year = ask_year1
                                        last_year = ask_year2
                                        break

                                selected_category = ''
                                while True:
                                    ask_category = input('Choose a category by entering a number to search for: ')
                                    # creating try-except method to convert stroke into int
                                    try:
                                        ask_category = int(ask_category)
                                    except ValueError:
                                        print('>> Enter a number << '.center(100, '-'), '', sep='\n')
                                        continue
                                    # reassignment existed variables
                                    if ask_category in all_categories:
                                        selected_category = ask_category
                                        break

                                # creating request for search by more years and category
                                raw_more_year_category_request = """select f.title, f.release_year year, c.name category_name, c.category_id from film f
                                                                    join film_category fc on f.film_id = fc.film_id
                                                                    join category c on fc.category_id = c.category_id
                                                                    where f.release_year between %(first_year)s and %(last_year)s and c.category_id = %(category)s
                                                                    order by f.release_year;"""
                                cursor_read.execute(raw_more_year_category_request, {'first_year': first_year, 'last_year': last_year, 'category': selected_category})
                                all_years_category_datas = cursor_read.fetchall()

                                # making category name for saving in database
                                category_name = all_categories[selected_category]

                                # saving all datas in database
                                history_by_more_year_category(first_year, last_year, selected_category, category_name)

                                # creating variation if no data founded
                                if len(all_years_category_datas) == 0:
                                    print('', ' >> No movies found << '.center(100, '-'), '', sep='\n')

                                # creating variation if there are founded less than 10 movies
                                elif len(all_years_category_datas) <= 10:
                                    all_founded_movies = [name for name, year, category, cid in all_years_category_datas]
                                    print(f'\n{frame}\n\nAll movies ({len(all_years_category_datas)}) founded by years {first_year} - {last_year} and category "{all_categories[selected_category]}":\n')
                                    for movie in all_founded_movies:
                                        print(f'>> {movie}\n')
                                    print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                                    choice_loop_year_category = True
                                    break

                                # creating variation if more than 10 movies was found
                                elif len(all_years_category_datas) > 10:
                                    print(f'\n{frame}\n\nThere was {len(all_years_category_datas)} movies founded by years {first_year} - {last_year} and category "{all_categories[selected_category]}":\n')
                                    cursor_read.execute(raw_more_year_category_request, {'first_year': first_year, 'last_year': last_year, 'category': selected_category})
                                    end_of_query_more_year_category = ""
                                    while not end_of_query_more_year_category:
                                        raw_every_10_movies = cursor_read.fetchmany(10)
                                        if len(raw_every_10_movies) == 0:
                                            end_of_query_more_year_category = True
                                            print('', '---[ No more movie found ]---'.center(100),'---[ End of query ]---'.center(100), frame, '', sep='\n')
                                            break
                                        # showing next films in queue
                                        every_10_movies = [name for name, year, category, cid in raw_every_10_movies]
                                        print(f'\nShowing {len(every_10_movies)} movies:\n')
                                        for movie in every_10_movies:
                                            print(f'>> {movie}\n')

                                        # creating variable to show more movies
                                        while True:
                                            ask_to_show_more = input('|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                            if ask_to_show_more == "y":
                                                break
                                            elif ask_to_show_more == "n":
                                                end_of_query_more_year_category = True
                                                choice_loop_year_category = True
                                                print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                                break

            # option to search by popular requests
            elif ask_for_close_app == "3":
                print('', '---[ Your choice: search by popular requests ]---'.center(100, '-'), '', sep='\n')

                # creating loop of popularity
                popular_requests = ""
                while not popular_requests:
                    # creating ask variable to choose search
                    print(f'Choose which popular category you would like to search for:\n\n1 - Top 10 movie name requests\n2 - Top 10 year requests\n3 - Top 10 category requests\n4 - Top 10 year and category requests\n')
                    select_choice = input('Enter a number of option or press enter to exit: ').strip()

                    # closing loop
                    if select_choice == "":
                        popular_requests = ''
                        print('---[ Exit from popular requests ]---'.center(100, '-'))
                        break


                    # popular names
                    if select_choice == "1":
                        print('', '---[ Your choice: search by popular name requests ]---'.center(100, '-'), '', sep='\n')

                        # showing top 10 popular name requests
                        selected_request = top_name_requests()

                        # creating exit if no one request was selected to re-search
                        if selected_request is None:
                            popular_requests = True
                            break

                        # creating raw query to search
                        raw_top_name_query = """select f.title, f.release_year year, c.name category_name from film f
                                                join film_category fc on f.film_id = fc.film_id
                                                join category c on fc.category_id = c.category_id
                                                where f.title like %s
                                                order by f.title"""
                        cursor_read.execute(raw_top_name_query, (f'%{selected_request}%',))
                        founded_datas = cursor_read.fetchall()

                        # saving entered data to database
                        history_by_name(selected_request)

                        # creating variation if there are founded less than 10 movies
                        if len(founded_datas) <= 10:
                            founded_data = [[name, year, category] for name, year, category in founded_datas]
                            print(f'\n{frame}\n\nThere was {len(founded_datas)} movies found on "{selected_request}":\n')
                            for film in founded_data:
                                for title, year, category in [film]:
                                    print(f'>> Title: {title} \n\tYear: {year} \n\tCategory: {category}\n')
                            print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')

                        # creating variation if more than 10 movies was found
                        elif len(founded_datas) > 10:
                            print(f'\n{frame}\n\nThere was {len(founded_datas)} movies found on "{selected_request}".')
                            cursor_read.execute(raw_top_name_query, (f"%{selected_request}%",))
                            end_of_query = ""
                            while not end_of_query:
                                raw_every_10_films = cursor_read.fetchmany(10)
                                if len(raw_every_10_films) == 0:
                                    print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                    break
                                # showing next films in queue
                                every_10_films = [[name, year, category] for name, year, category in raw_every_10_films]
                                print(f'\nShowing {len(every_10_films)} movies:\n')
                                for film in every_10_films:
                                    for title, year, category in [film]:
                                        print(f'>> Title: {title} \n\tYear: {year} \n\tCategory: {category}\n')

                                # creating variable to show more movies
                                while True:
                                    ask_to_show_more = input('|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                    if ask_to_show_more == "y":
                                        break
                                    elif ask_to_show_more == "n":
                                        end_of_query = True
                                        print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                        break

                        # exit loop
                        popular_requests = True
                        break


                    # popular years
                    if select_choice == "2":
                        print('', '---[ Your choice: search by popular year requests ]---'.center(100, '-'), '', sep='\n')

                        # showing top 10 popular year requests
                        selected_request = top_year_requests()

                        # creating exit if no one request was selected to re-search
                        if selected_request is None:
                            popular_requests = True
                            break

                        # checking if called datas is dictionary
                        if isinstance(selected_request, dict):
                            # making from datas variables
                            first_year, last_year = selected_request["fy"], selected_request["ly"]

                            # creating raw query to search
                            raw_top_years_query = """select f.title, f.release_year year, c.name category_name from film_category fc
                                                     join category c on fc.category_id = c.category_id
                                                     join film f on f.film_id = fc.film_id and release_year between %(first_year)s and %(last_year)s
                                                     order by title;"""
                            cursor_read.execute(raw_top_years_query, {'first_year': first_year, 'last_year': last_year})
                            all_selected_years = cursor_read.fetchall()

                            # saving all datas in database
                            history_by_more_years(first_year, last_year)

                            # creating variation if there are founded less than 10 movies
                            if len(all_selected_years) <= 10:
                                all_movies_by_year = [[name, year, category] for name, year, category in all_selected_years]
                                print(f'\n{frame}\n\nAll movies {len(all_selected_years)} found on years "{first_year} - {last_year}":\n')
                                for movie in all_movies_by_year:
                                    for name, year, category in [movie]:
                                        print(f'>> Name: {name}\n\tYear: {year}\n\tCategory: {category}\n')
                                print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                                popular_requests = True
                                break

                            # creating variation if more than 10 movies was found
                            elif len(all_selected_years) > 10:
                                print(f'\n{frame}\n\nThere was {len(all_selected_years)} movies found on years "{first_year} - {last_year}":')
                                cursor_read.execute(raw_top_years_query, {'first_year': first_year, 'last_year': last_year})
                                end_of_query_more_year = ""
                                while not end_of_query_more_year:
                                    raw_every_10_movies_more_years = cursor_read.fetchmany(10)
                                    if len(raw_every_10_movies_more_years) == 0:
                                        popular_requests = True
                                        print('', '---[ No more movie found ]---'.center(100),'---[ End of query ]---'.center(100), frame, '', sep='\n')
                                        break

                                    # showing next films in queue
                                    every_10_movies = [[name, year, category] for name, year, category in
                                                       raw_every_10_movies_more_years]
                                    print(f'\nShowing {len(every_10_movies)} movies:\n')
                                    for movie in every_10_movies:
                                        for name, year, category in [movie]:
                                            print(f'>> Name: {name}\n\tYear: {year}\n\tCategory: {category}\n')

                                    # creating variable to show more movies
                                    while True:
                                        ask_to_show_more = input(
                                            '|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                        if ask_to_show_more == "y":
                                            break
                                        elif ask_to_show_more == "n":
                                            popular_requests = True
                                            end_of_query_more_year = True
                                            print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                            break


                        # checking if selected variant only with one year
                        elif isinstance(selected_request, int):
                            # creating raw query to search
                            raw_top_years_query = """select f.title, f.release_year year, c.name category_name from film_category fc
                                                     join category c on fc.category_id = c.category_id
                                                     join film f on f.film_id = fc.film_id and release_year = %s
                                                     order by title;"""
                            cursor_read.execute(raw_top_years_query, (selected_request,))
                            raw_year_data = cursor_read.fetchall()

                            # saving data to database
                            history_by_one_year(selected_request)

                            # creating variation if there are founded less than 10 movies
                            if len(raw_year_data) <= 10:
                                all_movies_by_year = [[name, category] for name, year, category in raw_year_data]
                                print(f'\n{frame}\n\nAll movies {len(raw_year_data)} found by year "{selected_request}":\n')
                                for movie in all_movies_by_year:
                                    for name, category in [movie]:
                                        print(f'>> Name: {name}\n\tCategory: {category}\n')
                                print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                                popular_requests = True
                                break

                            # creating variation if more than 10 movies was found
                            elif len(raw_year_data) > 10:
                                print(f'\n{frame}\n\nThere was {len(raw_year_data)} movies found on year "{selected_request}":\n')
                                cursor_read.execute(raw_top_years_query, (selected_request,))
                                end_of_query = ""
                                while not end_of_query:
                                    raw_every_10_movies = cursor_read.fetchmany(10)
                                    if len(raw_every_10_movies) == 0:
                                        year_loop = True
                                        print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                        break

                                    # showing next films in queue
                                    every_10_movies = [[name, category] for name, year, category in raw_every_10_movies]
                                    print(f'\nShowing {len(every_10_movies)} movies:\n')
                                    for movie in every_10_movies:
                                        for name, category in [movie]:
                                            print(f'>> Name: {name}\n\tCategory: {category}\n')

                                    # creating variable to show more movies
                                    while True:
                                        ask_to_show_more = input('|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                        if ask_to_show_more == "y":
                                            break
                                        elif ask_to_show_more == "n":
                                            popular_requests = True
                                            end_of_query = True
                                            print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                            break


                    # popular categories
                    if select_choice == "3":
                        print('', '---[ Your choice: search by popular category requests ]---'.center(100, '-'), '', sep='\n')

                        # showing top 10 popular category requests
                        selected_request = top_category_requests()

                        # creating exit if no one request was selected to re-search
                        if selected_request is None:
                            popular_requests = True
                            break

                        # creating raw query to search
                        raw_top_category_query = """select f.title, f.release_year year, c.category_id, c.name from film f
                                                    join film_category fc on f.film_id = fc.film_id
                                                    join category c on fc.category_id = c.category_id 
                                                    where c.name like %s
                                                    order by f.title;"""
                        cursor_read.execute(raw_top_category_query, (f'%{selected_request}%',))
                        raw_top_category_data = cursor_read.fetchall()

                        # creating dictionary with key:id and value:name of category
                        raw_id_name_category = [[category_id, category_name] for movie_name, year, category_id, category_name in raw_top_category_data]
                        category_dict = {}
                        for cid, name in raw_id_name_category:
                            category_dict[cid] = name

                        # getting key from dict by using value
                        raw_category_id = [key for key, value in category_dict.items() if value == selected_request]
                        category_id = int(raw_category_id[0])

                        # saving datas to database
                        history_by_category(category_id, selected_request)

                        # creating variation if there are founded less than 10 movies
                        if len(raw_top_category_data) <= 10:
                            all_movies_in_category = [[name, year] for name, year, cid, category in raw_top_category_data]
                            print(f'\n{frame}\n\nAll movies {len(raw_top_category_data)} found in category "{selected_request}":\n')
                            for movie in all_movies_in_category:
                                for name, year in [movie]:
                                    print(f'>> Name: {name}\n\tYear: {year}\n')
                            print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                            popular_requests = True
                            break

                        # creating variation if more than 10 movies was found
                        elif len(raw_top_category_data) > 10:
                            print(f'\n{frame}\n\nThere was {len(raw_top_category_data)} movies found on category "{selected_request}":')
                            cursor_read.execute(raw_top_category_query, (selected_request,))
                            end_of_query = ""
                            while not end_of_query:
                                raw_every_10_movies = cursor_read.fetchmany(10)
                                if len(raw_every_10_movies) == 0:
                                    category_loop = True
                                    print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, sep='\n')
                                    break

                                # showing next films in queue
                                every_10_movies = [[name, year] for name, year, cid, category in raw_every_10_movies]
                                print(f'\nShowing {len(every_10_movies)} movies:\n')
                                for movie in every_10_movies:
                                    for name, year in [movie]:
                                        print(f'>> Name: {name}\n\tYear: {year}\n')

                                # creating variable to show more movies
                                while True:
                                    ask_to_show_more = input('|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                    if ask_to_show_more == "y":
                                        break
                                    elif ask_to_show_more == "n":
                                        end_of_query = True
                                        popular_requests = True
                                        print('', '---[ End of query ]---'.center(100), frame, sep='\n')
                                        break

                    # option to search by years and categories
                    if select_choice == '4':
                        print('', '---[ Your choice: search by popular year(-s) & category requests ]---'.center(100, '-'), '', sep='\n')

                        # showing top 10 popular category requests
                        selected_request = top_year_category_requests()

                        # creating exit if no one request was selected to re-search
                        if selected_request is None:
                            popular_requests = True
                            break

                        # checking if in dictionary are more dictionaries
                        if any(isinstance(years, dict) for years in selected_request.values()):

                            # taking all values from main dictionary
                            first_year = selected_request["year"]["fy"]
                            last_year = selected_request["year"]["ly"]
                            selected_category = selected_request["category"]

                            # creating request for search by more years and category
                            raw_more_year_category_request = """select f.title, f.release_year year, c.name category_name, c.category_id from film f
                                                                join film_category fc on f.film_id = fc.film_id
                                                                join category c on fc.category_id = c.category_id
                                                                where f.release_year between %(first_year)s and %(last_year)s and c.name = %(category)s
                                                                order by f.release_year;"""
                            cursor_read.execute(raw_more_year_category_request,{'first_year': first_year, 'last_year': last_year, 'category': selected_category})
                            all_years_category_datas = cursor_read.fetchall()

                            # creating dictionary with key:id and value:name of category
                            raw_id_name_category = [[category_id, category_name] for movie_name, year, category_name, category_id in all_years_category_datas]
                            category_dict = {}
                            for cid, name in raw_id_name_category:
                                category_dict[cid] = name

                            # getting key from dict by using value
                            raw_category_id = [key for key, value in category_dict.items() if value == selected_category]
                            category_id = int(raw_category_id[0])

                            # saving all datas in database
                            history_by_more_year_category(first_year, last_year, category_id, selected_category)

                            # creating variation if there are founded less than 10 movies
                            if len(all_years_category_datas) <= 10:
                                all_founded_movies = [name for name, year, category, cid in all_years_category_datas]
                                print(
                                    f'\n{frame}\n\nAll movies ({len(all_years_category_datas)}) founded by years {first_year} - {last_year} and category "{selected_category}":\n')
                                for movie in all_founded_movies:
                                    print(f'>> {movie}\n')
                                print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                                popular_requests = True
                                break

                            # creating variation if more than 10 movies was found
                            elif len(all_years_category_datas) > 10:
                                print(
                                    f'\n{frame}\n\nThere was {len(all_years_category_datas)} movies founded by years {first_year} - {last_year} and category "{selected_category}":\n')
                                cursor_read.execute(raw_more_year_category_request,{'first_year': first_year, 'last_year': last_year, 'category': selected_category})
                                end_of_query_more_year_category = ""
                                while not end_of_query_more_year_category:
                                    raw_every_10_movies = cursor_read.fetchmany(10)
                                    if len(raw_every_10_movies) == 0:
                                        end_of_query_more_year_category = True
                                        print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, '',sep='\n')
                                        break

                                    # showing next films in queue
                                    every_10_movies = [name for name, year, category, cid in raw_every_10_movies]
                                    print(f'\nShowing {len(every_10_movies)} movies:\n')
                                    for movie in every_10_movies:
                                        print(f'>> {movie}\n')

                                    # creating variable to show more movies
                                    while True:
                                        ask_to_show_more = input('|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                        if ask_to_show_more == "y":
                                            break
                                        elif ask_to_show_more == "n":
                                            end_of_query_more_year_category = True
                                            popular_requests = True
                                            print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                            break

                        # if only one dictionary returned
                        else:
                            # taking all values from dictionary
                            selected_year = selected_request["year"]
                            selected_category = selected_request["category"]

                            # creating request for search by one year and category
                            raw_year_category_request = """select f.title, f.release_year, c.name, c.category_id from film f
                                                           join film_category fc on f.film_id = fc.film_id
                                                           join category c on fc.category_id = c.category_id
                                                           where f.release_year = %(year)s and c.name = %(category)s
                                                           order by f.title;"""
                            cursor_read.execute(raw_year_category_request,{'year': selected_year, 'category': selected_category})
                            all_years_category_datas = cursor_read.fetchall()

                            # creating dictionary with key:id and value:name of category
                            raw_id_name_category = [[category_id, category_name] for movie_name, year, category_name, category_id in all_years_category_datas]
                            category_dict = {}
                            for cid, name in raw_id_name_category:
                                category_dict[cid] = name

                            # getting key from dict by using value
                            raw_category_id = [key for key, value in category_dict.items() if value == selected_category]
                            category_id = int(raw_category_id[0])

                            # saving all datas in database
                            history_by_one_year_category(selected_year, category_id, selected_category)

                            # creating variation if there are founded less than 10 movies
                            if len(all_years_category_datas) <= 10:
                                all_founded_movies = [name for name, year, category, cid in all_years_category_datas]
                                print(f'\n{frame}\n\nAll movies ({len(all_years_category_datas)}) founded by year {selected_year} and category "{selected_category}":\n')
                                for movie in all_founded_movies:
                                    print(f'>> {movie}\n')
                                print('---[ End of query ]---'.center(100), frame, '', sep='\n')
                                popular_requests = True
                                break

                            # creating variation if more than 10 movies was found
                            elif len(all_years_category_datas) > 10:
                                print(f'\n{frame}\n\nThere was {len(all_years_category_datas)} movies founded by year {selected_year} and category "{selected_category}":\n')
                                cursor_read.execute(raw_year_category_request,{'year': selected_year, 'category': selected_category})
                                end_of_query_year_category = ""
                                while not end_of_query_year_category:
                                    raw_every_10_movies = cursor_read.fetchmany(10)
                                    if len(raw_every_10_movies) == 0:
                                        end_of_query_year_category = True
                                        print('', '---[ No more movie found ]---'.center(100), '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                        break

                                    every_10_movies = [name for name, year, category, cid in raw_every_10_movies]
                                    print(f'\nShowing {len(every_10_movies)} movies:\n')
                                    for movie in every_10_movies:
                                        print(f'>> {movie}\n')

                                    # creating variable to show more movies
                                    while True:
                                        ask_to_show_more = input('|-> Do you want to see more movie offers? [y/n] ').strip().lower()
                                        if ask_to_show_more == "y":
                                            break
                                        elif ask_to_show_more == "n":
                                            end_of_query_year_category = True
                                            popular_requests = True
                                            print('', '---[ End of query ]---'.center(100), frame, '', sep='\n')
                                            break

        # closing connection to database
        cursor_read.close()
        connection_read.close()
        close_db_write()

    # if connection failed
    else:
        print(frame, '[ FAILED TO CONNECT TO DATABASE ]'.center(100, '-'), frame, sep="\n")