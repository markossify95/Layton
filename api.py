from pprint import pprint

from bson.json_util import (dumps)
from flask import Flask
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.library
books = db.books
tags = db.tags
prefixes = db.prefixes

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/tags', methods=['GET'])
def get_tags():
    all_t = tags.find()
    return dumps(all_t)


@app.route('/books', methods=['GET', 'POST'])
# @cross_origin(supports_credentials=True)
def filter_books():
    one_book = books.find({"100": {
        "h": "scr",
        "c": "2001"
    }}).limit(10)
    # one_book = books.find_one({"_id": ObjectId("5a727954d3354a1b3ee82868")})
    pprint(one_book)
    return dumps(one_book, ensure_ascii=False)  # , JSONOptions(json_mode=JSONMode.RELAXED)


@app.route('/prefixes', methods=['GET'])
# @cross_origin(supports_credentials=True)
def get_prefixes():
    prefix_list = prefixes.find()
    return dumps(prefix_list, ensure_ascii=False)  # , JSONOptions(json_mode=JSONMode.RELAXED)


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run(port=8080)
