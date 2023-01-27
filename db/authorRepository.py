from db import db

class AuthorRepository():
    def __init__(self):
       self.db = db.Db() 

    def getAuthor(self, id):
        query = "SELECT name FROM authors WHERE id = %s"
        with self.db:
            return self.db.query_one(query, (id,))
