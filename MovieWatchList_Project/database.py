
###################################################################################################################
###################################################################################################################
# Imports yo! Only the finest imports from around the world!

import datetime
import sqlite3

###################################################################################################################
###################################################################################################################

###################################################################################################################
###################################################################################################################
# Global variables. List it all out here

######### Tables Below ########
#create a table named movies. has 3 coloums named title, release_timestamp and id
CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies ( 
    id INTEGER,
    title TEXT,
    release_timestamp REAL,
    PRIMARY KEY (id)
);"""

#create a table named watchlist. has 2 coloums named watcher_name and movie_id.
CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    watcher_name TEXT,
    movie_id INTEGER,
    FOREIGN KEY(watcher_name) REFERENCES users(watcher_name),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""
    
#create a table named users. has 1 coloums named watcher_name
CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    watcher_name TEXT,
    PRIMARY KEY (watcher_name)
);"""

######### SQL Query commands ########
INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?,?);" #CREATES or inserts a value, this case inserts into the table movie into the coulums title, release_timestamp, watched giving watched a default value of 0. The other title and relese timestamp will be looking for values when this variable is used. 
DELETE_MOVIE = "DELETE FROM movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;" # selects ALL from the table called movies
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;" #Selects all from movies table WHERE the coloum 'release_timestamp' is greater then 'somevalue not yet assigned'.. going to use timestamp here though when this is used.
SELECT_WATCHED_MOVIES = "SELECT movies.* FROM movies JOIN watched ON watched.movie_id = movies.title JOIN users ON users.watcher_name = watched.watcher_name WHERE users.watcher_name = ?;" #selects all from movie table where the coloum watched is 1 or True.
INSERT_WATCHED_MOVIE = "INSERT INTO watched (watcher_name, movie_id) VALUES (?,?)"
INSERT_USER = "INSERT INTO users (watcher_name) VALUES (?)"

connection = sqlite3.connect("data.db") #connection to sqlite3 and creates a file named data.db IF it does not exist.. if it does then it just connects to it.

###################################################################################################################
###################################################################################################################

###################################################################################################################
###################################################################################################################
# Thur be gold and functions down below!!!

def add_user(watcher_name):
    with connection:
        connection.execute(INSERT_USER, (watcher_name,))


def create_tables(): #makes a table called 'movies'
    with connection: #uses the variable we created which is assigned to connect to a file named data.db using sqlite3. Once done running everything inside of the with statement it closes the connection.
        connection.execute(CREATE_MOVIES_TABLE)
        connection.execute(CREATE_USERS_TABLE)
        connection.execute(CREATE_WATCHLIST_TABLE)


def add_movie(title, release_timestamp):#adds a movie to the table. takes its title and release date as arguments for the INSERT_MOVIES variable that requires 2 for its two ?,?..
    with connection:
        connection.execute(INSERT_MOVIES, (title, release_timestamp))

def get_movies(upcoming=False): #gets movies. and seperates the selection by a boolean. Movie comes intofuntion. Function assigns it false be default. Movie will have a upcoming propertie .
    with connection: #connects and closes after everything is ran
        cursor = connection.cursor() #create a cursor variable 
        if upcoming: # this checks the value of the bool. if it is a upcoming movie it will trigger here and run the SELECT_UPCOMING_MOVIES and if not then select_all_movies
            today_timestamp = datetime.datetime.today().timestamp() #a way of getting the time of RIGHT NOW
            cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,)) #executes (connect to data base and do a query) SELECT_UPCOMING_MOVIES with the variable today_timestamp we just created in the line before this one as the ? referance.replacment
        else:
            cursor.execute(SELECT_ALL_MOVIES) # select all movies in the table
        return cursor.fetchall() #returns everything the cursor has 'touched'/'pointed to'

def watch_movie(watcher_name, movie_id):
    with connection:
        connection.execute(INSERT_WATCHED_MOVIE, (watcher_name, movie_id))


def get_watched_movies(watcher_nameArgument): # returns all the movies that have been watched
    watcher_name = str(watcher_nameArgument)
    with connection: # connects and closes
        cursor = connection.cursor() #create cursor
        cursor.execute(SELECT_WATCHED_MOVIES, (watcher_name,))#execute (connect to data base and run Query) SELECT_WATCHED_MOVIES which just returns back all movies with a 1 value in the watched coloum
        return cursor.fetchall() #return back everything cursor pointed to. 

###################################################################################################################
###################################################################################################################
