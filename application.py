import os
import requests
from dotenv import load_dotenv
from flask import Flask, session, render_template, redirect, url_for, request, flash, jsonify
from flask.wrappers import Request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tempfile import mkdtemp
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

load_dotenv("./env")
FLASK_APP = os.getenv("FLASK_APP")
DATABASE_URL = os.getenv("DATABASE_URL")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():

    items = 20
    id = session.get("user_id")
    
    values = db.execute(f"SELECT username FROM users WHERE id_user = '{id}'").fetchall()      
    username = values[0]['username']

    page = request.args.get('page', 1, type=int)

    books = db.execute("SELECT * FROM Books ORDER BY title LIMIT 16").fetchall()
    booksAll = db.execute("SELECT * FROM Books ORDER BY title ").fetchall()

    # print(query.paginate(page=page, per_page=items))
    #books.query.paginate()
    #print(books)
    return render_template("index.html", username=username, books=books, booksAll=booksAll)

@app.route("/login", methods=["GET", "POST"])  
def login():

    session.clear()

    if request.method == 'POST':
   
        logemail = request.form.get("logemail")
        # rows = db.execute(f"SELECT COUNT(username) FROM users WHERE email = '{logemail}'").fetchall()
        values = db.execute(f"SELECT * FROM users WHERE email = '{logemail}'").fetchall()
        

        #hashpass = request.form.get("logpass")
        check = check_password_hash(values[0]['hash'], request.form.get("logpass"))

        if len(values) != 1 or check == False:

          # Remember which user has logged in
                
            return redirect("/login")
        else:
            session["user_id"] = values[0]["id_user"]
                # Redirect user to home page
            username = values[0]['username']

            #return render_template("index.html", username=username)
            return redirect("/")

    return render_template("login.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        logemail=request.form.get("logemail2")
                    
        rows = db.execute(f"SELECT COUNT(username) FROM users WHERE email = '{logemail}'").fetchall()
                    
        if rows[0][0] == 0:
            logname = (request.form.get("logname2"))
            logpass = generate_password_hash(request.form.get("logpass2"))
                        
            db.execute(f"INSERT INTO users(username, hash, email) VALUES ('{logname}', '{logpass}', '{logemail}')")

            db.commit()
            return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/details/<int:id_book>")
@login_required
def details(id_book):

    id = session["user_id"] 

    values = db.execute(f"SELECT username FROM users WHERE id_user = '{id}'").fetchall()      
    username = values[0]['username']

    ## Para el detalle
    book = db.execute(f"SELECT * FROM Books WHERE id_book = {id_book}").fetchall()

    reviews = db.execute(f"SELECT *, users.username FROM reviews INNER JOIN users ON reviews.id_user = users.id_user WHERE id_book = {id_book}").fetchall()
    isset = db.execute(f"SELECT id_user FROM reviews WHERE id_user = {id} and id_book = {id_book}").fetchall()

    print("----------")
    #print(len(isset))
    
    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+ book[0]["isbn"]).json()
    print(response)

     
    if len(isset) == 1:
        bandera = False
    else:
        bandera = True
    
    print("----------")
    print(bandera)

    return render_template("detail.html", username=username, book=book, reviews=reviews, bandera=bandera)

@app.route("/api/<string:isbn>")
@login_required
def api(isbn):

    # API OUTPUT
    books = db.execute(f"SELECT * FROM books WHERE isbn = '{isbn}'").fetchone()

    if books is None:
            return jsonify({"error": "ISBN INVALIDO"}), 404

    if books.score == 0 and books.review == 0:
        average = 0
    else:
        average = books.score / books.review
    #print("--------")
    #print(books.isbn)

    return jsonify({
        "title": books.title,
        "author": books.author,
        "year": books.publish_date,
        "isbn": books.isbn,
        "review_count": books.review,
        "average_score": average
    })
