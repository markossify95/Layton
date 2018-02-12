from pymongo import MongoClient


def insert_books(book_list):
    client = MongoClient()
    db = client['library']
    if 'books' not in db.collection_names():
        db.create_collection('books')

    db.books.insert_many(book_list)


def insert_keys(key_list):
    client = MongoClient()
    db = client['library']
    if 'tags' not in db.collection_names():
        db.create_collection('tags')

    db.tags.insert(key_list)


def insert_prefixes(prefixes):
    client = MongoClient()
    db = client['library']
    if 'prefixes' not in db.collection_names():
        db.create_collection('prefixes')

    db.prefixes.insert(prefixes)
