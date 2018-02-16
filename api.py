import json
from collections import defaultdict
from datetime import datetime, timedelta
from pprint import pprint
from uuid import uuid4

from bson.json_util import (dumps, loads)
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.library
books = db.books
tags = db.tags
prefixes = db.prefixes

app = Flask(__name__, static_url_path='')
# app.permanent_session_lifetime = 24000
# app.config['SESSION_COOKIE_DOMAIN'] = 'dev.localhost'
# app.session_interface = MongoSessionInterface()


CORS(app, support_credentials=True)


@app.route('/', methods=['GET'])
def get_template():
    return render_template('index.html')


@app.route('/tags', methods=['GET'])
def get_tags():
    all_t = tags.find({}, {'_id': False})
    return dumps(all_t)


@app.route('/books_simple', methods=['POST'])
@cross_origin(supports_credentials=True)
def get_books():
    resp = None
    if request.method == "POST" and request.data is not None:
        print(request.data)
        req_list = loads(request.data.decode('utf-8'))
        t = request.headers.get('Authorization')
        if not find_and_update(t, req_list):
            resp = json.dumps({'Authorized': False})
        else:
            # resp = json.dumps(req_list)
            resp = json.dumps(filter_books(req_list))
    return resp


@app.route('/get_access_token', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_token():
    t = str(uuid4())
    exp = datetime.utcnow() + timedelta(hours=10)
    db.custom_auth.update({'id': t}, {'id': t, 'expires': exp, 'data': []}, upsert=True)
    return json.dumps({'id': t, 'expires': str(exp)})


def find_and_update(token, req_list):
    # token = r.headers.get('Authorization')
    if not token:
        return False

    token = db.custom_auth.find_one({'id': token})
    if token and token['expires'] > datetime.utcnow():
        token['data'] += req_list
        # exp = datetime.utcnow() + timedelta(hours=10)
        db.custom_auth.update({'id': token['id']},
                              {"$set": {'id': token['id'],
                                        'expires': token['expires'],
                                        'data': token['data']}}, True)
        return True
    else:
        return False


@app.route('/get_session_history', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_session_history(token):
    if not token:
        return False

    token = db.custom_auth.find_one({'id': token})
    if token and token['expires'] > datetime.utcnow():
        return json.dumps({'searches': token['data']})
    return json.dumps({})


# @app.route('/books_complex', methods=['POST'])
# # @cross_origin(supports_credentials=True)
# def get_books_by_query_complex():
#     """
#     Metoda za slanje svih podataka za knjige
#     :return:
#     """
#     resp = []
#     if request.method == "POST" and request.data is not None:
#         req_list = loads(request.data.decode('utf-8'))
#         print(request.data)
#         resp = filter_books(req_list, simple=False)
#     return json.dumps(resp)


def filter_books(req_list, simple=True):
    """
    metoda za filtriranje knjiga prema upitu, koriste je get_books_by_query_ simple|complex
    :param req_list: upit sa frontenda
    :param simple: false = complex
    :return: 
    """
    resp = []
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
            print("Nasao: " + search_value[k] + " logic: " + search_value['logic'])
            if search_value is not None:
                if search_value['logic'] == 'AND':
                    partial_dict = generate_or_query_dict(v, search_value[k])  # OVAJ IZMENJEN
                    and_dict['$and'].append(partial_dict)
                else:
                    partial_dict = generate_or_query_dict(v, search_value[k])
                    if not partial_dict:
                        print("OVDE SAM PUKO")
                    final_dict['$or'].append(partial_dict)

        if and_dict:
            final_dict['$or'].append(dict(and_dict))
    pprint(dict(final_dict))
    resp = books.find(final_dict, {'_id': False})
    # if simple:  # ako je simple response vraca odgovarajuca polja
    resp = prepare_response(resp)
    return resp


@app.route('/prefixes', methods=['GET', 'OPTIONS'])
# @cross_origin(supports_credentials=True)
def get_prefixes():
    """
    Metoda za slanje human readable prefiksa na frontend
    :return: 
    """
    prefix_list = prefixes.find()
    return dumps(prefix_list, ensure_ascii=False)  # , JSONOptions(json_mode=JSONMode.RELAXED)


def modifikuj_kriterijume(query):
    """
    Parsiranje parametara na podpolja
    :param query: [{"KW": "Haos", "logic": "AND"}, {"AU": "NEDELJKOVIĆ", "logic": "OR"}]
    :return: 
    """
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


# def generate_simple_query_dict(field_list, value):
#     or_dict = {}
#     # final_dict = defaultdict(list)
#     for item in field_list:
#         or_dict[item] = {"$regex": u"" + value}
#         # final_dict['$or'].append(or_dict)
#         # or_dict = {}
#     print(or_dict)
#     return or_dict


def generate_or_query_dict(field_list, value):
    """
    Generisanje or upita
    :param field_list: 
    :param value: 
    :return: 
    """
    or_dict = {}
    final_dict = defaultdict(list)
    for item in field_list:
        # or_dict[item] = parse_single_query(item, value)
        final_dict['$or'].append(parse_single_query(item, value))
        or_dict = {}
    print(final_dict)
    return dict(final_dict)


def parse_single_query(item, values):
    """
    Metoda za obradu upira u slucaju vise reci // Ivo Andric, Mesa Selimovic
    :param item: broj polja
    :param values: reci u upiru
    :return: 
    """
    and_dict = defaultdict(list)
    value_list = values.split(' ')
    for val in value_list:
        and_dict['$and'].append({item: {"$regex": u"" + val}})
    return dict(and_dict)


def prepare_dict(final_dict):
    """
    Priprema jednog record-a za simple response, za naslovom, autorom i ostalim zahtevanim poljima
    :param final_dict: 
    :return: 
    """
    print(final_dict)
    prepared_dict = {}
    try:
        title_author = final_dict.get('200').split(';')
        title = title_author[0]
        prepared_dict["title"] = title.title()

    except:
        prepared_dict["title"] = ""
    try:
        full_author = final_dict.get('700').split(';')
        author = full_author[1] + " " + full_author[2]

        prepared_dict["author"] = author.title()
    except:
        prepared_dict["author"] = ""
    try:
        pub_year = final_dict.get('210').split(';')
        publisher = pub_year[1]
        year = pub_year[2]
        prepared_dict["publisher"] = publisher.title()
        prepared_dict["year"] = year
    except:
        prepared_dict["publisher"] = ""
        prepared_dict["year"] = ""
    try:
        place_str = final_dict['102'].split(';')[0]
        prepared_dict["place"] = place_str
    except:
        prepared_dict["place"] = ""

    prepared_dict["record"] = stringify_dict(final_dict)

    return prepared_dict


def prepare_response(rs):
    """
    Priprema liste dict-ova za krajnji response za simple response
    :param rs: 
    :return: 
    """
    response = []
    for element in rs:
        # print(element)
        prepared = prepare_dict(element)
        response.append(prepared)
    return response


def stringify_dict(resp_dict):
    """
    prebacivanje jednog record-a u string za complex response
    :param resp_dict: 
    :return: 
    """
    lst = []
    for k, v in resp_dict.items():
        field = str(k) + '  ' + str(recover_string(v))
        lst.append(field)
    return ' '.join(lst)


def recover_string(raw_data):
    lst = raw_data.split(';')
    result = ""
    for i, element in enumerate(lst):
        result += str(chr(97 + i)) + element.strip() + " "
    return result


# def stringify_response(resp):
#     """
#     za complex response priprema stringova
#     :param resp:
#     :return:
#     """
#     lst = []
#     for r in resp:
#         record = {"record": stringify_dict(r)}
#         lst.append(record)
#     return lst


if __name__ == '__main__':
    app.run('dev.localhost')
