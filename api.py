from collections import defaultdict
from pprint import pprint

from bson.json_util import (dumps, loads)
from flask import Flask, request
from flask_cors import CORS
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.library
books = db.books
tags = db.tags
prefixes = db.prefixes

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/tags', methods=['GET'])
def get_tags():
    all_t = tags.find()
    return dumps(all_t)


@app.route('/books', methods=['POST'])
# @cross_origin(supports_credentials=True)
def filter_books():
    rs = None
    if request.method == "POST":
        req_list = loads(request.data.decode('unicode_escape'))
        and_dict = defaultdict(list)
        final_dict = defaultdict(list)
        if len(req_list) > 0:
            print(req_list)
            filter_dict = modifikuj_kriterijume(req_list)
            print(filter_dict)
            if not filter_dict:
                return dumps({})
            for k, v in filter_dict.items():

                search_value = get_value_by_key_in_list(req_list, k)
                # print("Nasao: " + search_value[k] + " logic: " + search_value['logic'])
                if search_value is not None:
                    if search_value['logic'] == 'OR':
                        partial_dict = generate_simple_query_dict(v, search_value[k])
                        and_dict['$or'].append(partial_dict)
                        # print("Za " + search_value[k])
                        # print(and_dict)
                    else:
                        partial_dict = generate_or_query_dict(v, search_value[k])
                        final_dict['$and'].append(partial_dict)

            final_dict['$and'].append(dict(and_dict))
        # print("Query: ")
        pprint(dict(final_dict))
        rs = books.find(final_dict)
        # pprint(dumps(rs))
    return dumps(rs)


@app.route('/prefixes', methods=['GET'])
# @cross_origin(supports_credentials=True)
def get_prefixes():
    prefix_list = prefixes.find()
    return dumps(prefix_list, ensure_ascii=False)  # , JSONOptions(json_mode=JSONMode.RELAXED)


def modifikuj_kriterijume(query):
    # query = [{"KW": "Haos", "logic": "AND"}, {"AU": "NEDELJKOVIĆ", "logic": "OR"}]
    tag_values = tags.find_one()
    dict_sq = {}
    for q in query:
        for key, value in q.items():
            if key == "logic":
                continue

            fields = tag_values.get(key)
            if fields is None:
                print("Prazno za: " + key)
                continue
            lista = fields.split(', ')
            dicter = parse_list(lista)
            dict_sq[key] = dicter
            # print(q[k])
            # logic = upit[0]["logic"]

            # print(logic)
            # value = tag_values[upit[0]]
            # print(value)
    return dict_sq


def parse_list(lista):
    # dicter = defaultdict(list)
    # for el in lista:
    #     num = el[:3]
    #     char = el[3]
    #     dicter[num].append(char)
    final_set = set()
    for el in lista:
        final_set.add(el[:3])
    return list(final_set)


def get_value_by_key_in_list(dict_list, key):
    for item in dict_list:
        for k, v in item.items():
            if k == key:
                return item
    return None


# books.find($'$or':[{'965':'Beban'}, {'605':'Beban'}
#
#
# def generisi_query_dict(req_list, filter_dict):
#     final_dict = defaultdict(list)
#     for k, v in filter_dict:
#         for item in req_list:
#             if item.get(k) is not None:
#
#                 final_dict['$or'].append()

def generate_simple_query_dict(field_list, value):
    or_dict = {}
    # final_dict = defaultdict(list)
    for item in field_list:
        or_dict[item] = {"$regex": u"" + value}
        # final_dict['$or'].append(or_dict)
        # or_dict = {}
    # print(final_dict)
    return or_dict


def generate_or_query_dict(field_list, value):
    or_dict = {}
    final_dict = defaultdict(list)
    for item in field_list:
        or_dict[item] = {"$regex": u"" + value}
        final_dict['$or'].append(or_dict)
        or_dict = {}
    return dict(final_dict)


if __name__ == '__main__':
    app.run(port=8080)
