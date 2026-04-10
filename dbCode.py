# dbCode.py
# Author: Amber Lange
# Helper functions for database connection and queries

import pymysql
import creds
import boto3


#Relational Database

def get_conn():
    """
    Returns a connection to the MySQL RDS instance.
    """

    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """
    Executes a SELECT query and returns all rows as dictionaries.
    """

    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows


#The following function was generated with help from Claude but didn't end up being used
#def db_changes(query, args=()):
#    """
#    Executes a change to database
#    """
#
#    conn = get_conn()
#    cur = conn.cursor(pymysql.cursors.DictCursor)
#    cur.execute(query, args)
#    conn.commit()
#    cur.close()
#    conn.close()


def view_movies_query():
    """
    Displays the first 50 movies in the database with theirnids, titles, genres, release_date, and popularity.
    """
    
    rows = execute_query("""
        SELECT movie.movie_id, title, GROUP_CONCAT(genre_name SEPARATOR ', ') AS genres, release_date, popularity
        FROM movie
        JOIN movie_genres ON movie.movie_id=movie_genres.movie_id
        JOIN genre ON movie_genres.genre_id=genre.genre_id
        GROUP BY movie.movie_id, title, release_date, popularity
        LIMIT 50""")
    
    return(rows)


def find_movie_query(name):
    """
    Displays the id, title, genres, release date, and popularity of a specific movies.
    """
    
    rows = execute_query("""
            SELECT movie.movie_id, title, GROUP_CONCAT(genre_name SEPARATOR ', ') AS genres, release_date, popularity
            FROM movie 
            JOIN movie_genres 
                ON movie.movie_id = movie_genres.movie_id
            JOIN genre 
                ON movie_genres.genre_id = genre.genre_id
            WHERE title = %s
            GROUP BY movie.movie_id, title, release_date, popularity""",
        (name,))
    
    return(rows)
    

"""Somehow broke find_movie_query and view_movie_query"""
#def insert_movie(id, name, release):
#    """
#    Inserts the id, title, release date of a movie into the movie table.
#    """
#
#    db_changes("""
#        INSERT INTO movie(movie_id, title, release_date)
#        VALUES (%s, %s, %s)
#        """,
#    (id, name, release, ))
#
#    return 


#Non-Relational Database

def get_table():
    """Return a reference to the DynamoDB CompletedMovies table."""
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    return dynamodb.Table('CompletedMovies')


def return_movie(name, info):
    """
    returns data for specific user review
    """

    return { 'Movie' : name,
    'Rating' : info.get("Rating", "Rating Unavailable"),
    'Review' : info.get("Review", "Review Unavailable")}


def return_all_movies():
    """
    Returns all reviews for every user
    """

    table = get_table()
    
    response = table.scan()
    items = response.get("Items", [])
    
    data = []
    for item in items:
        user = item.get("User", "User Unknown")
        movies = item.get("Movies", {})
        completed_movies = []

        for name, info in movies.items():
            completed_movies.append(return_movie(name, info))

        data.append({'User' : user, 'Movies' : completed_movies})
    
    return data


def create_movie(user, movie_title, rating, review):
    """
    Creates a new user with their first review
    """

    table = get_table()

    table.put_item(
        Item = { 'User' : user,
        'Movies' : {
            movie_title : {
                'Rating' : rating,
                'Review' : review
            }}})
    return


def update_completed(user, movie_title, rating, review):
    """Allows users to add reviews
    """

    table = get_table()

    try:
        table.update_item(
            Key={'User': user},
            UpdateExpression="SET Movies.#movie = :info",
            ExpressionAttributeNames={'#movie' : movie_title},
            ExpressionAttributeValues = {'info' : {
                'Rating' : rating,
                'Review' : review
            }})
        return
    
    except:
        print("error adding completed movie")


def delete_db_reviews(user):
    """
    Delete all reviews for a user
    """

    table = get_table()

    table.delete_item(
        Key = {
            'User' : user
        })
    
    return