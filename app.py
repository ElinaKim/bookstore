from flask import Flask, request, abort
from db import BookRepository
from db import AuthorRepository
import psycopg2

app = Flask(__name__)

bookRepo = BookRepository()
authorRepo = AuthorRepository()

# Sequence of events:
# app.py -> bookRepo.getAllBooks() -> self.db.__enter__() -> db.connect() -> curs.execute(...) -> result -> db.__exit__()

## TODO: Move to env file
## TODO: Create repository pattern
conn_str = "postgres://postgres:postgrespw@localhost:49153/bookstore"

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

    if name == None or len(name) == 0 or name.isspace() == True:
        return abort(400, description = "Invalid author name")

    with conn:
        with conn.cursor() as curs:
            curs.execute("INSERT INTO authors (name) VALUES (%s) RETURNING id", (name,))
            id = curs.fetchone()

    return {'id': id, 'message': f'author {name} was added'}, 201

@app.route("/api/authors/<id>", methods = ['PUT'])
def update_author(id):
    if int(id) <= 0:
        return abort(400, description="Invalid id in the Request-URI")
    author = request.json

    name = author['name']

    if name == None or len(name) == 0 or name.isspace() == True:
        abort(400, "Invalid author name")

    with conn:
        with conn.cursor() as curs:
            curs.execute("UPDATE authors SET name = (%s) WHERE id = (%s) RETURNING id", (name, id))

    return {'id': id, 'message': f'Author {name} was updated'}, 200

@app.route("/api/authors/<id>", methods = ['DELETE'])
def delete_author(id):
    if int(id) <= 0:
        return abort(400, description="Invalid id in the Request-URI")
    with conn:
        with conn.cursor() as curs:
            curs.execute("DELETE FROM authors WHERE id = (%s) RETURNING id",(id))

    return {'id': id, 'message': f'author with id {id} was deleted'}, 200
    
@app.route("/api/authors", methods = ['GET'])
def get_all_authors():
    with conn:
        with conn.cursor() as curs:
            curs.execute("SELECT id, name FROM authors")
            records = curs.fetchall()
            if records == None:
                return abort(404, description = "No authors can be found")

    return {'authors': records}, 200

@app.route("/api/authors/<id>", methods = ['GET'])
def get_author(id):
    if int(id) <= 0:
        return abort(400, description="Invalid id in the Request-URI")

    authors = authorRepo.getAuthor(id)
    if authors == None:
        return abort(404, description = "No author with such id can be found")

    return {'author': authors}, 200


@app.route("/api/books", methods = ["GET"])
def get_all_books():
    books = bookRepo.getAllBooks()

    return {'books': books}, 200

@app.route("/api/books/<id>", methods = ["GET"])
def get_book(id):
    if int(id) <= 0:
        return abort(400, description="Invalid id in the Request-URI")

    book = bookRepo.getBook(id)
    if (book == None):
        return abort(404, description="The server has not found book name matching the Request-URI")

    return {'books': book}, 200

@app.route("/api/books", methods = ["POST"])
def create_book():
    book = request.json
    
    name = book['name']
    
    if name == None or len(name) == 0 or name.isspace() == True:
        return abort(400, description = "Invalid book name")
    
    id = bookRepo.addBook(name)

    return {'id': id, 'message': f'{name} book was added'}, 201

@app.route("/api/books/<id>", methods = ["PUT"])
def update_book(id):
    if int(id) <= 0:
        return abort(400, description="Invalid id in the Request-URI")

    book = request.json

    name = book['name']
    
    if name == None or len(name) == 0 or name.isspace == True:
        return abort(400, description = "Invalid book name")

    with conn:
        with conn.cursor() as curs:
            curs.execute("UPDATE books SET name = (%s) WHERE id = (%s) RETURNING id", (name, id))

    return {'id': id, 'message': f'{name} book was updated'}, 200

@app.route("/api/books/<id>",methods = ["DELETE"])
def delete_book(id):
    if int(id) <= 0:
        return abort(400, description="Invalid id in the Request-URI")
    with conn:
        with conn.cursor() as curs:
            curs.execute("DELETE FROM books WHERE id = (%s) RETURNING id", (id))

    return {'id': id, 'message': f'book with id {id} was deleted.'}, 200