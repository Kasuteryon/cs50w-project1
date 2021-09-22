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
import json

app = Flask(__name__)

load_dotenv("./env")
FLASK_APP = os.getenv("FLASK_APP")
DB_URL = os.getenv("DB_URL")
FLASK_DEBUG = os.getenv("FLASK_DEBUG")

# Check for environment variable
if not os.getenv("DB_URL"):
    raise RuntimeError("DB_URL is not set")

# Configure session to use filesystem
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
#app.config["SESSION_FILE_DIR"] = mkdtemp()
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DB_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():

    id = session.get("user_id")
    
    values = db.execute(f"SELECT username FROM users WHERE id_user = '{id}'").fetchall()      
    username = values[0]['username']

    books = db.execute("SELECT * FROM Books ORDER BY title LIMIT 8").fetchall()
    booksAll = db.execute("SELECT * FROM Books ORDER BY title ").fetchall()

    items =  []
    dicto = {}

    print("_-------------------------")

    for book in books:
        responses = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+ book.isbn).json()

        if responses["totalItems"] != 0:
            if "imageLinks" in responses["items"][0]["volumeInfo"]:
                image = responses["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
            
            else:
                image = "https://imagenes.elpais.com/resizer/EkPGHGt1AYBU6-FFuStAwC_NKSw=/1960x0/arc-anglerfish-eu-central-1-prod-prisa.s3.amazonaws.com/public/YC5XJK5X2DES4MGR2W3HWWS7JU.jpg"
        else:
            image = "https://imagenes.elpais.com/resizer/EkPGHGt1AYBU6-FFuStAwC_NKSw=/1960x0/arc-anglerfish-eu-central-1-prod-prisa.s3.amazonaws.com/public/YC5XJK5X2DES4MGR2W3HWWS7JU.jpg"
    
        
        dicto = ({"title":book.title},
        {"isbn":book.isbn},
        {"author":book.author},
        {"date":book.publish_date},
        {"id":book.id_book},
        {"image": image})

        items.append(dicto)

    # print(query.paginate(page=page, per_page=items))
    #books.query.paginate()
    #print(books)
    return render_template("index.html", username=username, books=books, booksAll=booksAll, items=items)

@app.route("/login", methods=["GET", "POST"])  
def login():

    session.clear()

    error1 = None
    if request.method == 'POST':
   
        logemail = request.form.get("logemail")
        # rows = db.execute(f"SELECT COUNT(username) FROM users WHERE email = '{logemail}'").fetchall()
        values = db.execute(f"SELECT * FROM users WHERE email = '{logemail}'").fetchall()
        
        
        #hashpass = request.form.get("logpass")
        #check = check_password_hash(values[0]['hash'], request.form.get("logpass"))

        if len(values) != 1 or check_password_hash(values[0]['hash'], request.form.get("logpass")) == False:

          # Remember which user has logged in
            error1= True
            ##return redirect("/login")
        else:
            session["user_id"] = values[0]["id_user"]
                # Redirect user to home page
            #return render_template("index.html", username=username)
            return redirect("/")
            

    return render_template("login.html", error1=error1)
    

@app.route("/register", methods=["GET", "POST"])
def register():

    error2 = None
    error3 = None
    if request.method == "POST":
        logemail=request.form.get("logemail2")
        logname = request.form.get("logname2")

        rows = db.execute(f"SELECT COUNT(email) FROM users WHERE email = '{logemail}'").fetchall()
        rows2 = db.execute(f"SELECT COUNT(username) FROM users WHERE username = '{logname}'").fetchall()

        if rows2[0][0] != 0:
            error3 = True
        elif rows[0][0] == 0:
            logpass = generate_password_hash(request.form.get("logpass2"))
                        
            db.execute(f"INSERT INTO users(username, hash, email) VALUES ('{logname}', '{logpass}', '{logemail}')")

            db.commit()
            return redirect("/login")
        else:
            error2 = True

    return render_template("login.html", error2=error2, error3=error3)

@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/details/<int:id_book>", methods=["GET", "POST"])
@login_required
def details(id_book):

    id = session["user_id"] 

    values = db.execute(f"SELECT username FROM users WHERE id_user = '{id}'").fetchall()      
    username = values[0]['username']

    if request.method == "POST":
        db.execute("INSERT INTO reviews(id_user, id_book, isset, message, stars) VALUES(:id_user, :id_book, :isset, :review, :stars)",
         {"id_user":id,"id_book":id_book,"review":request.form.get("review"),"isset":1, "stars":request.form.get("stars")}) 
        db.commit()
    ## Para el detalle
    book = db.execute(f"SELECT * FROM Books WHERE id_book = {id_book}").fetchone()

    reviews = db.execute(f"SELECT *, users.username FROM reviews INNER JOIN users ON reviews.id_user = users.id_user WHERE id_book = {id_book}").fetchall()
    isset = db.execute(f"SELECT id_user FROM reviews WHERE id_user = {id} and id_book = {id_book}").fetchall()

    print("--------------------------------------")
    #print(len(isset))
    
    response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+ book.isbn).json()

    # el .json() fue aplicado  ya UWU
    #print(response["items"][0]["volumeInfo"]["description"])
    itemsApi = []
    
    itemsApi.append({"title": book.title})
    itemsApi.append({"isbn": book.isbn})
    itemsApi.append({"author": book.author})
    itemsApi.append({"publish_date": book.publish_date})

    if response["totalItems"] != 0:
        if "description" in response["items"][0]["volumeInfo"]:
            itemsApi.append({"description":response["items"][0]["volumeInfo"]["description"]})
        else:
            itemsApi.append({"description":"Wasn't found on Google Book's API"})

        if "averageRating" in response["items"][0]["volumeInfo"]:
            itemsApi.append({"averageRating":response["items"][0]["volumeInfo"]["averageRating"]})
        else:
            itemsApi.append({"averageRating":"Wasn't found on Google Book's API"})

        if "ratingsCount" in response["items"][0]["volumeInfo"]:
            itemsApi.append({"ratingsCount":response["items"][0]["volumeInfo"]["ratingsCount"]})
        else:
            itemsApi.append({"ratingsCount":"Wasn't found on Google Book's API"})

        if "categories" in response["items"][0]["volumeInfo"]:
            itemsApi.append({"categories":response["items"][0]["volumeInfo"]["categories"][0]})
        else:
            itemsApi.append({"categories":"Wasn't found on Google Book's API"})
        
        if "imageLinks" in response["items"][0]["volumeInfo"]:
            itemsApi.append({"image":response["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]})
            
        else:
            itemsApi.append({"image":"https://imagenes.elpais.com/resizer/EkPGHGt1AYBU6-FFuStAwC_NKSw=/1960x0/arc-anglerfish-eu-central-1-prod-prisa.s3.amazonaws.com/public/YC5XJK5X2DES4MGR2W3HWWS7JU.jpg"})
    else:
        itemsApi.append({"description":"Wasn't found on Google Book's API"})
        itemsApi.append({"averageRating":"Wasn't found on Google Book's API"})
        itemsApi.append({"ratingsCount":"Wasn't found on Google Book's API"})
        itemsApi.append({"categories":"Wasn't found on Google Book's API"})
        itemsApi.append({"image":"https://imagenes.elpais.com/resizer/EkPGHGt1AYBU6-FFuStAwC_NKSw=/1960x0/arc-anglerfish-eu-central-1-prod-prisa.s3.amazonaws.com/public/YC5XJK5X2DES4MGR2W3HWWS7JU.jpg"})

    if len(isset) == 1:
        bandera = False
    else:
        bandera = True
    
    print("----------")
    print(bandera)

    return render_template("detail.html", username=username, reviews=reviews, bandera=bandera, items=itemsApi)

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

if __name__ == "main":
    app.run()