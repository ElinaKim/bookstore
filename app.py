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
    
    return name

@app.route("/api/authors/<id>", methods = ['PUT'])
def update_author(id):
    author = request.json

    name = author['name']

    return name
    
@app.route("/api/authors", methods = ['GET'])
def get_all_authors():
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM authors")
    records = cur.fetchall()
    return {'authors': records}, 200

@app.route("/api/authors/<id>", methods = ['GET'])
def get_author(id):
    return id

@app.route("/api/books", methods = ["GET"])
def get_all_books():
    return "All books"

@app.route("/api/books/<id>", methods = ["GET"])
def get_book(id):
    return id

@app.route("/api/books", methods = ["POST"])
def create_book():
    book = request.json
    
    name = book['name']
    
    return name

@app.route("/api/books/<id>", methods = ["PUT"])
def update_book(id):
    book = request.json

    name = book['name']

    return name
