from pprint import pprint

from bson.json_util import (dumps)
from flask import Flask
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.library
books = db.books
tags = db.tags

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/tags', methods=['GET'])
def get_tags():
    all_t = tags.find()
    return dumps(all_t)


@app.route('/books', methods=['GET', 'POST'])
def filter_books():
    one_book = books.find({"100": {
        "h": "scr",
        "c": "2001"
    }}).limit(10)
    # one_book = books.find_one({"_id": ObjectId("5a727954d3354a1b3ee82868")})
    pprint(one_book)
    return dumps(one_book, ensure_ascii=False)  # , JSONOptions(json_mode=JSONMode.RELAXED)


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run(port=8080)
