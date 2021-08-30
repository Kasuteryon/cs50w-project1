import csv
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv("./env")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine("DATABASE_URL")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, publish_date) VALUES (:isbn, :author, :title, :year)",
                    {"isbn": isbn, "author": author, "title": title, "year": year})
        
    db.commit()

if __name__ == "__main__":
    main()