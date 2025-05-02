# using database sakila
use sakila;

# showing all used tables
select * from film;
select * from film_category;
select * from category;



################################ MySQL REQUESTS ################################

# got movie title, release year and category name (MYSQL)
select f.title, f.release_year year, c.name category_name from film f
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
order by f.title;


# attempts with search by category_id
select f.title, f.release_year year from film f
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id and c.category_id = 3
order by f.title;


# getting all possible years (two methods)
select release_year from film group by release_year order by release_year;
select release_year, count(*) from film group by release_year order by release_year;



# checking some results (there was more than one release year used)
select f.title, f.release_year year, c.name category_name from film_category fc
join category c on fc.category_id = c.category_id
join film f on f.film_id = fc.film_id and release_year = 2000
order by title;

# making request with release_year and category_name and group by of column "year"
select f.release_year year, c.name category_name from film f
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
group by year;


# some another requests for project
# getting the same as with group by
select distinct release_year from film;
select distinct name from category;


# request with "where" and using release_year and category_id
select f.title, f.release_year year, c.name category_name from film f
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
where f.release_year = 2000 and c.category_id = 2
order by f.title;


# attempts with between
select title, release_year from film
where release_year between 2000 and 2020 order by release_year;


# getting info with using of "where" and "between"
select f.title, f.release_year year, c.name category_name from film f
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
where f.release_year between 2000 and 2002 and c.category_id = 2
order by f.title;

################################ PYTHON REQUESTS ################################

# got movie title, release year and category name and using "where" (PYTHON)
select f.title, f.release_year year, c.name category_name from film f
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
where title like %s
order by f.title;


# attempts with search by category_id
select c.category_id, c.name, count(f.title) amount_of_movies from film f
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id and c.category_id = %s
group by c.name order by c.category_id;


# request with "where" and using release_year and category_id
select f.title, f.release_year year, c.name category_name from film f
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
where f.release_year = %(year)s and c.name = %(category)s
order by f.title;


# getting info with using of "where" and "between" for python
select f.title, f.release_year year, c.name category_name from film f
join film_category fc on f.film_id = fc.film_id
join category c on fc.category_id = c.category_id
where f.release_year between %(first_year)s and %(last_year)s and c.category_id = %(category)s
order by f.release_year;


############################################ CREATING DATABASE ############################################

create database group_111124_fp_Klymentii_Taran;
use group_111124_fp_Klymentii_Taran;


# creating table to history search by name
create table history_search_by_name (
    id int auto_increment primary key,
    entered_text varchar(255) not null unique,
    counter int default 1);


# creating table to history search by category
create table history_search_by_category (
    id int auto_increment primary key,
    entered_category_id varchar(255) not null unique,
    entered_category_name varchar(255) not null unique,
    counter int default 1);


# creating table to history search by year
create table history_search_by_year (
    id int auto_increment primary key,
    one_year int,
    first_year int,
    last_year int,
    counter int default 1);


# creating table to history search by year and category
create table history_search_by_year_category (
    id int auto_increment primary key,
    year int,
    first_year int,
    last_year int,
    entered_category_id int,
    entered_category_name varchar(255),
    counter int default 1);



# looking all created tables
select * from history_search_by_name;
select * from history_search_by_year;
select * from history_search_by_category;
select * from history_search_by_year_category;



# making limit of 10 and sorting by counter
select * from history_search_by_name order by counter desc limit 10;
select * from history_search_by_year_category order by counter desc limit 10;
select * from history_search_by_year order by counter desc limit 10;
select * from history_search_by_category order by counter desc limit 10;





############################################ EXTRA ############################################
####################### commented with more "#" to avoid consequences)) #######################


########### drop table history_search_by_year_category;
########### drop table history_search_by_category;
########### drop table history_search_by_year;
########### drop table history_search_by_name;

########### truncate history_search_by_category;