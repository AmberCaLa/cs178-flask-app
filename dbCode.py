# dbCode.py
# Author: Amber Lange
# Helper functions for database connection and queries

import pymysql
import creds


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


#The following function was generate with help from Claude
def db_changes(query, args=()):
    """
    Executes a change to database
    """

    conn = get_conn()
    cur = conn.cursur(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()


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
    

def insert_movie(id, name, release):
    """
    Inserts the id, title, release date of a movie into the movie table.
    """

    db_changes("""
        INSERT INTO movie(movie_id, title, release_date)
        VALUES (%s, %s, %s)
        """,
    (id, name, release, ))

    return "Inserted"