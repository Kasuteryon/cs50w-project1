import csv
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()
DB_URL = os.getenv("DB_URL")
#print(DATABASE_URL)

if not os.getenv("DB_URL"):
    raise RuntimeError("DB_URL is not set")

engine = create_engine(os.getenv("DB_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    i = 0
    for isbn, title, author, year in reader:
        if title == "title":
            print("Omitted First Line")
        else:    
            db.execute("INSERT INTO books (isbn, title, author, publish_date) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "author": author, "title": title, "year": year})

            i += 1
            print(f"{i}: {isbn} - {author} - {title} - {year}")
            #db.commit()

if __name__ == "__main__":
    main()