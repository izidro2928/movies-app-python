from flask import current_app, render_template, request, redirect, Blueprint
from flask_paginate import Pagination, get_page_parameter
import mysql.connector
from flask_mysqldb import MySQL

movies = Blueprint('movies', __name__, template_folder='templates',
                   static_folder='static', static_url_path='/static/movies')


@movies.route('/')
def home():
    # Conectamos a la base de datos
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd="root", database="data_scrapper")
    cursor = mydb.cursor(buffered=True)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 20
    offset = page * limit - limit

    query = "SELECT * FROM movies"
    cursor.execute(query)
    result = cursor.fetchall()
    total = len(result)

    sql0 = "SELECT * FROM movies LIMIT %s OFFSET %s"
    val0 = (limit, offset)
    cursor.execute(sql0, val0)
    peliculas = cursor.fetchall()

    # MOSTRAR CATEGORIAS

    sql1 = "SELECT * FROM genres"
    cursor.execute(sql1)
    categories = cursor.fetchall()

    # MOSTRAR LOS AñOS

    sql2 = "SELECT * FROM years"
    cursor.execute(sql2)
    years = cursor.fetchall()

    pagination = Pagination(page=page, per_page=limit, total=total)
    title = "ToroMovies | Home"

    return render_template('index.html', pagination=pagination, peliculas=peliculas, title=title, pelicula="", categories=categories, years=years)

    cursor.close()
    mydb.close()


@movies.route('/movie/<id_pelicula>')
def single(id_pelicula):
    # Conectamos a la base de datos
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd="root", database="data_scrapper")
    cursor = mydb.cursor(buffered=True)

    sql1 = f"""SELECT * FROM movies WHERE movie_id = {id_pelicula} """
    cursor.execute(sql1)
    pelicula = cursor.fetchone()
    title = "ToroMovies | "

    # Mostrar Categorias
    sql2 = "SELECT * FROM genres"
    cursor.execute(sql2)
    categories = cursor.fetchall()

    # Mostrar por años
    sql3 = "SELECT * FROM years"
    cursor.execute(sql3)
    years = cursor.fetchall()

    return render_template('single.html', pelicula=pelicula, title=title, categories=categories, years=years)

    cursor.close()
    mydb.close()


@movies.route('/search', methods=['POST', 'GET'])
def search():
    # Conectamos a la base de datos
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd="root", database="data_scrapper")
    cursor = mydb.cursor(buffered=True)

    if request.method == "GET":
        limit = 12
        page = request.args.get(get_page_parameter(), type=int, default=1)
        offset = page * limit - limit
        title = request.args.get('query')
        if not title:
            return redirect('/')

        sql1 = f"SELECT * FROM movies WHERE title LIKE '%{title}%'"
        cursor.execute(sql1)
        data = cursor.fetchall()
        total = len(data)

        sql2 = f"SELECT * FROM movies WHERE title LIKE '%{title}%' LIMIT {limit} OFFSET {offset}"
        cursor.execute(sql2)
        movies = cursor.fetchall()

        # Mostrar Categorias
        sql3 = "SELECT * FROM genres"
        cursor.execute(sql3)
        categories = cursor.fetchall()

        # Mostrar por año
        sql4 = "SELECT * FROM years"
        cursor.execute(sql4)
        years = cursor.fetchall()

        pagination = Pagination(page=page, per_page=limit, total=total)
        title = "ToroMovies | Search"
        return render_template('search.html', movies=movies, pagination=pagination, title=title, pelicula="", categories=categories, years=years)

        cursor.close()
        mydb.close()


@movies.route('/genre/<genre_name>')
def genres(genre_name):
    # Conectamos a la base de datos
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd="root", database="data_scrapper")
    cursor = mydb.cursor(buffered=True)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 20
    offset = page * limit - limit

    query = f"SELECT * FROM movies WHERE genre= '{genre_name}'"
    cursor.execute(query)
    result = cursor.fetchall()
    total = len(result)

    sql1 = f"SELECT * FROM movies WHERE genre = '{genre_name}' LIMIT {limit} OFFSET {offset}"
    cursor.execute(sql1)
    movies_genres = cursor.fetchall()

    # Mostrar Categorias
    sql2 = "SELECT * FROM genres"
    cursor.execute(sql2)
    categories = cursor.fetchall()

    # MOSTRAR POR AñO
    sql3 = "SELECT * FROM years"
    cursor.execute(sql3)
    years = cursor.fetchall()

    title = "ToroMovies | Genres"

    pagination = Pagination(page=page, per_page=limit, total=total)
    return render_template('category.html', movies_genres=movies_genres, pelicula="", categories=categories, years=years, pagination=pagination, title=title)

    cursor.close()
    mydb.close()


@movies.route('/year/<year>')
def by_year(year):
    # Conectamos a la base de datos
    mydb = mysql.connector.connect(
        host="localhost", user="root", passwd="root", database="data_scrapper")
    cursor = mydb.cursor(buffered=True)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 20
    offset = page * limit - limit

    query = f"SELECT * FROM movies WHERE year={year}"
    cursor.execute(query)
    result = cursor.fetchall()
    total = len(result)

    sql1 = f"SELECT * FROM movies WHERE year={year} LIMIT {limit} OFFSET {offset}"
    cursor.execute(sql1)
    movies_year = cursor.fetchall()

    # MOSTRAR POR AñO
    sql2 = "SELECT * FROM years"
    cursor.execute(sql2)
    years = cursor.fetchall()

    # Mostrar categorias
    sql3 = "SELECT * FROM genres"
    cursor.execute(sql3)
    categories = cursor.fetchall()

    title = "ToroMovies | Years"
    pagination = Pagination(page=page, per_page=limit, total=total)
    return render_template('year.html', movies_year=movies_year, pelicula="", years=years, categories=categories, pagination=pagination, title=title)
    cursor.close()
    mydb.close()
