# author: Amber Lange
# description: Flask movie database website
# credit: Project based off examples from Professors Urness and Moore

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *


app = Flask(__name__)
app.secret_key = 'your_secret_key' 


@app.route('/')
def home():
    return render_template('home.html')


@app.route("/add-movie", methods = ['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        release = request.form['release']

        insert_movie(id, name, release)

        flash('Movie successfully added to database! Thank you for your contribution!', 'success')  

        return redirect(url_for('home'))
    else:
        return render_template('add_movie.html')


@app.route("/view-movies")
def view_movies():
    
    viewed = view_movies_query()

    return render_template("view_movies.html", movies = viewed)


@app.route('/find-movie', methods = ['GET', 'POST'])
def find_movie():
    if request.method == 'POST':
        name = request.form["name"]

        found = find_movie_query(name)

        return render_template("view_found_movie.html", movie = found)

    else:
        return render_template('find_movie.html')



@app.route('/delete-movie',methods=['GET', 'POST'])
def delete_movie():
    if request.method == 'POST':
        name = request.form['name']

        flash('Movie removed successfully.', 'warning') 

        return redirect(url_for('home'))
    else:
        return render_template('delete_movie.html')


@app.route('/complete-movies')
def complete_movies():
    return render_template('complete_movies.html')

@app.route('/add-complete-movie', methods=['GET', 'POST'])
def add_complete_movie():
    if request.method == 'POST':
        user_name = request.form['user_name']
        movie_name = request.form["movie_name"]
        rating = request.form['rating']
        review = request.form['review']
                
        complete_movie(user_name, movie_name, rating, review)

        flash('Completed movie recorded!', 'success')  

        return redirect(url_for('home.html'))
    else:
        return render_template('add_complete_movie.html')





# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
