from db import db

class BookRepository:
    def __init__(self):
        self.db = db.Db()
    
    def getAllBooks(self):
        query = "SELECT id, name FROM books"
        with self.db:
            return self.db.query_all(query, None)
    
    def getBook(self, id):
        query = "SELECT name FROM books WHERE id = %s"
        with self.db:
            return self.db.query_one(query, (id,))
    
    def addBook(self, bookName):
        query = "INSERT INTO books (name) VALUES (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (bookName,))[0]
