from flask import Flask, request
import psycopg2

app = Flask(__name__)

conn_str = "postgres://postgres:postgrespw@localhost:55000/bookstore"

try:
    conn = psycopg2.connect(conn_str)
except psycopg2.Error as e:
    print("Unable to connect to the database.")
    print(e)
else:
    print("Connection to the database was successful.")



@app.route("/")
def index():
    return "Hello World"

@app.route("/api/authors", methods = ['POST'])
def create_author():
    author = request.get_json()
    
    name = author['name']

    with conn:
        with conn.cursor() as curs:
            curs.execute("INSERT INTO authors (name) VALUES (%s) RETURNING id",(name,))
            records = curs.fetchall()

    return {'authors': records}, 201

@app.route("/api/authors/<id>", methods = ['PUT'])
def update_author(id):
    author = request.json

    name = author['name']

    with conn:
        with conn.cursor() as curs:
            curs.execute("UPDATE authors SET name = (%s) WHERE id = (%s) RETURNING id", (name, id))
            records = curs.fetchall()

    return {'authors': records}, 200

@app.route("/api/authors/<id>", methods = ['DELETE'])
def delete_author(id):
    with conn:
        with conn.cursor() as curs:
            curs.execute("DELETE FROM authors WHERE id = (%s) RETURNING id",(id))
            records = curs.fetchall()

    return {'authors': records}, 200
    
@app.route("/api/authors", methods = ['GET'])
def get_all_authors():
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, name FROM authors")
            records = curs.fetchall()

    return {'authors': records}, 200

@app.route("/api/authors/<id>", methods = ['GET'])
def get_author(id):
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT name FROM authors WHERE id = %s",(id))
            records = curs.fetchone()

    return {'authors': records}, 200


@app.route("/api/books", methods = ["GET"])
def get_all_books():
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, name FROM books")
            records = curs.fetchall()

    return {'books': records}, 200

@app.route("/api/books/<id>", methods = ["GET"])
def get_book(id):
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT name FROM books WHERE id = %s",(id))
            records = curs.fetchone()

    return {'books': records}, 200

@app.route("/api/books", methods = ["POST"])
def create_book():
    book = request.json
    
    name = book['name']
    
    with conn:
        with conn.cursor() as curs:
            curs.execute("INSERT INTO books (name) VALUES (%s) RETURNING id",(name,))
            records = curs.fetchall()

    return {'books': records}, 201

@app.route("/api/books/<id>", methods = ["PUT"])
def update_book(id):
    book = request.json

    name = book['name']

    with conn:
        with conn.cursor() as curs:
            curs.execute("UPDATE books SET name = (%s) WHERE id = (%s) RETURNING id", (name, id))
            records = curs.fetchall()

    return {'books': records}, 200

@app.route("/api/books/<id>",methods = ["DELETE"])
def delete_book(id):
    with conn:
        with conn.cursor() as curs:
            curs.execute("DELETE FROM books WHERE id = (%s) RETURNING id", (id))
            records = curs.fetchall()

    return {'books': records}, 200