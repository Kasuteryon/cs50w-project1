import os
from dotenv import load_dotenv

from flask import Flask, session, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tempfile import mkdtemp
from helpers import login_required

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
    return "K pex"

@app.route("/login")
def login():

    session.clear()
    return render_template("login.html")