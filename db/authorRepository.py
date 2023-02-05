from db import db

class AuthorRepository():
    def __init__(self):
       self.db = db.Db() 

    def getAuthor(self, id):
        query = "SELECT name FROM authors WHERE id = %s"
        with self.db:
            return self.db.query_one(query, (id,))
    
    def getAllAuthors(self):
        query = "SELECT * FROM authors"
        with self.db:
            return self.db.query_all(query,)

    def addAuthor(self, name):
        query = "INSERT INTO authors (name) VALUES (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (name,))
    
    def updateAuthor(self, name, id):
        query = "UPDATE authors SET name = (%s) WHERE id = (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (name, id,))
    
    def deleteAuthor(self, id):
        query = "DELETE FROM authors WHERE id = (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (id))
    



