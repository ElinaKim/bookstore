from flask import Flask, request

app = Flask(__name__)

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
    return "All authors"
