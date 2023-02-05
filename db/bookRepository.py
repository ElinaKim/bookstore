from db import db

class BookRepository:
    def __init__(self):
        self.db = db.Db()
    
    def getAllBooks(self):
        query = "SELECT books.name AS book_name, authors.name AS author_name FROM books INNER JOIN authors ON books.author_id = authors.id"
        with self.db:
            return self.db.query_all(query,)
    
    def getBook(self, id):
        query = "SELECT books.name AS book_name, authors.name AS author_name FROM books INNER JOIN authors ON books.author_id = authors.id WHERE books.id = %s"
        with self.db:
            return self.db.query_one(query, (id,))
    
    def addBook(self, bookName):
        query = "INSERT INTO books (name) VALUES (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (bookName,))[0]
    
    def updateBook(self, name, id):
        query = "UPDATE books SET name = (%s) WHERE id = (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (name, id))
    
    def deleteBook(self, id):
        query = "DELETE FROM books WHERE id = (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (id,))
