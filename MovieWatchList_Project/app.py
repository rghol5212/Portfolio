###################################################################################################################
###################################################################################################################
# Imports yo! Only the finest imports from around the world!

import datetime
import database

###################################################################################################################
###################################################################################################################

###################################################################################################################
###################################################################################################################
# Global variables. List it all out here

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Add user to the app.
7) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"

###################################################################################################################
###################################################################################################################


###################################################################################################################
###################################################################################################################
# Thur be gold and functions down below!!!

def prompt_add_movie():
    '''
    inputs from user, movie title and release date. Then uses add_movie funtion from database.py to add both to a table. 
    '''
    title = input("Movie title: ")
    release_date = input("Release date (mm-dd-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%m-%d-%Y")
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)


def print_movie_list(heading, movies): #prints out movie list. Takes 2 argue ments. heading will be a str, movie a list.
    print(f"-- {heading} movies --")
    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie[2])#this creates the date but its in a 1192040239 whatever format. so make a variable here that will be that format that we can convert in the next line below this one into a human readable format.
        human_date = movie_date.strftime("%b %d %Y") # here we just take the movie_date varialbe above this line and format it into a more human readable form. should look like Jan-24-1999 or something. With the month being a 3 letter str representing that month. 
        print(f"{movie[0]}: {movie[1]} (on {human_date})")  # id: name (on date)
    print("---- \n")


def prompt_watched_movie():
    watchers_name = input("Enter your name please: ")
    movie_id = input("Movie Name: ")
    database.watch_movie(watchers_name, movie_id)

def prompt_add_user():
    username = input("Username: ")
    database.add_user(username)

###################################################################################################################
###################################################################################################################



###################################################################################################################
###################################################################################################################
# Main Menu logic. 

print(welcome)
database.create_tables()

if __name__ == '__main__': #THIS Makes this file able to be importable whithout AUTORUNNING the while loop. 
    while (user_input := input(menu)) != "7": #selection of 5 choices (6th choice ends program) using if and elif structure. This is the logic to the menu selections 1-6.. ***use of WALRUS funtion here..':='...
        if user_input == "1": #Add new movie
            prompt_add_movie()
        elif user_input == "2":#View upcoming movies
            movies = database.get_movies(True) # runs get_movie funtion but passes True along with it. get-movie function will return upcoming movies due to this.
            print_movie_list("Upcoming", movies)#upcoming formats into print statment in line 30 and prints upcoming movies
        elif user_input == "3":#view all movies
            movies = database.get_movies(False) # can leave out 'False' but added it for better readability... runs get_movie function but passes False so returns all the movies. 
            print_movie_list("All", movies)#formats 'ALL' into line 30 as the heading argument value, and prints the movie list.
        elif user_input == "4":#watch a movie
            prompt_watched_movie()
        elif user_input == "5":#view watched movies
            watchers_name = input("Enter your name please:  ")
            movies = database.get_watched_movies(watchers_name) #list. gets watched movies.
            #print(movies)
            print_movie_list("Watched", movies)

        elif user_input == "6":
            prompt_add_user()       
        else:
            print("Invalid input, please try again!")

###################################################################################################################
###################################################################################################################

