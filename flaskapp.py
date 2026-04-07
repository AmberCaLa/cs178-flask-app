# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *
import pymysql
import creds

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

def get_connection():
    """Opens and returns a connection to the RDS MySQL database."""
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db
    )

def execute_query(query, args=()):
    """
    Runs a SQL query and returns all result rows as a list of tuples.
    Always use parameterized queries (args) when inserting user input —
    never build SQL strings with f-strings or concatenation.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall()
    conn.close()
    return rows

def display_html(rows):
    """
    Converts query result rows into a simple HTML table string.
    Flask routes can return this directly as a response.
    """
    html = "<table border='1'>"
    for row in rows:
        html += "<tr>"
        for col in row:
            html += f"<td>{col}</td>"
        html += "</tr>"
    html += "</table>"
    return html

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/view-movies")
def view_movies():
    """
    Fetches the first 20 tracks from the movie database
    and returns them as an HTML table.
    Route: /view-movies
    """
    rows = execute_query("""
        SELECT movie.movie_id, title, genre_name, release_date, popularity
        FROM movie
        JOIN movie_genre ON movie.movie_id=movie_genre.movie_id
        JOIN genre ON movie_genre.genre_id=genre.genre_id
        LIMIT 50
    """)
    return render_template("view_movies.html", movies = rows)


@app.route('/find-movie', methods = ['GET', 'POST'])
def find_movie():
    if request.method == 'POST':
        name = request.form["name"]

        rows = execute_query("""
            SELECT movie.movie_id, title, genre_name, release_date, popularity
            FROM movie 
            JOIN movie_genre 
                ON movie.movie_id = movie_genre.movie_id
            JOIN genre 
                ON movie_genre.genre_id = genre.genre_id
            WHERE title = %s""",
        (name,))

        return render_template("view_found_movie.html", movie = rows)

    else:
        return render_template('find_movie.html')


@app.route('/add-movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form["first"]
        genre = request.form["last"]
        release = request.form['release']
        popularity = request.form['popularity']
                
        flash('Movie added successfully! Thank you for your contribution!', 'success')  

        return redirect(url_for('home.html'))
    else:
        return render_template('add_movie.html')

@app.route('/delete-movie',methods=['GET', 'POST'])
def delete_movie():
    if request.method == 'POST':
        name = request.form['name']

        flash('Movie removed successfully.', 'warning') 

        return redirect(url_for('home'))
    else:
        return render_template('delete_movie.html')


@app.route('/display-users')
def display_users():
    # hard code a value to the users_list;
    # note that this could have been a result from an SQL query :) 
    users_list = (('John','Doe','Comedy'),('Jane', 'Doe','Drama'))
    return render_template('display_users.html', users = users_list)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
