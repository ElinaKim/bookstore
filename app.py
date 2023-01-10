from flask import Flask, request
import psycopg2

app = Flask(__name__)

conn_str = "postgres://postgres:postgrespw@localhost:55000/bookstore"
conn = psycopg2.connect(conn_str)


@app.route("/")
def index():
    return "Hello World"

@app.route("/api/authors", methods = ['POST'])
def create_author():
    author = request.get_json()
    
    name = author['name']

    cur = conn.cursor()
    cur.execute("INSERT INTO authors (name) VALUES (%s) RETURNING id",(name,))
    records = cur.fetchall()

    return {'authors': records}, 201

@app.route("/api/authors/<id>", methods = ['PUT'])
def update_author(id):
    author = request.json

    name = author['name']

    cur = conn.cursor()
    cur.execute("UPDATE authors SET name = (%s) WHERE id = (%s) RETURNING id", (name, id))
    records = cur.fetchall()

    return {'authors': records}, 200

@app.route("/api/authors/<id>", methods = ['DELETE'])
def delete_author(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM authors WHERE id = (%s) RETURNING id",(id))
    records = cur.fetchall()

    return {'authors': records}, 200
    
@app.route("/api/authors", methods = ['GET'])
def get_all_authors():
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM authors")
    records = cur.fetchall()

    return {'authors': records}, 200

@app.route("/api/authors/<id>", methods = ['GET'])
def get_author(id):
    cur = conn.cursor()
    cur.execute("SELECT name FROM authors WHERE id = %s",(id))
    records = cur.fetchone()

    return {'authors': records}, 200


@app.route("/api/books", methods = ["GET"])
def get_all_books():
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM books")
    records = cur.fetchall()
    
    return {'books': records}, 200

@app.route("/api/books/<id>", methods = ["GET"])
def get_book(id):
    cur = conn.cursor()
    cur.execute("SELECT name FROM books WHERE id = %s",(id))
    records = cur.fetchone()

    return {'books': records}, 200

@app.route("/api/books", methods = ["POST"])
def create_book():
    book = request.json
    
    name = book['name']
    
    cur = conn.cursor()
    cur.execute("INSERT INTO books (name) VALUES (%s) RETURNING id",(name,))
    records = cur.fetchall()

    return {'books': records}, 201

@app.route("/api/books/<id>", methods = ["PUT"])
def update_book(id):
    book = request.json

    name = book['name']

    cur = conn.cursor()
    cur.execute("UPDATE books SET name = (%s) WHERE id = (%s) RETURNING id", (name, id))
    records = cur.fetchall()

    return {'books': records}, 200

@app.route("/api/books/<id>",methods = ["DELETE"])
def delete_book(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = (%s) RETURNING id", (id))
    records = cur.fetchall()

    return {'books': records}, 200