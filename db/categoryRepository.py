from db import db

class CategoryRepository:
    def __init__(self):
        self.db = db.Db()

    def getAllCategories(self):
        query = "SELECT * FROM category"
        with self.db:
            return self.db.query_all(query,)

    def getCategory(self, id):
        query = "SELECT name FROM category WHERE id = %s"
        with self.db:
            return self.db.query_one(query,(id,))
    
    def addCategory(self, name):
        query = "INSERT INTO category (name) VALUES (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (name,))

    def updateCategory(self, name, id):
        query = "UPDATE category SET name = (%s) WHERE id = (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (name, id))
    
    def deleteCategory(self, id):
        query = "DELETE FROM category WHERE id = (%s) RETURNING id"
        with self.db:
            return self.db.query_one(query, (id,))

    

