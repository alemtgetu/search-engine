# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from engine import get_soup, get_words, get_links, is_valid_url

import re

app = Flask(__name__)
CORS(app)
words_dict = {}


def add_words_to_dict(words: list):
    # breakpoint()
    for w in words:
        # strip word of non-alphanumeric characters
        pattern = re.compile('\W')
        w = re.sub(pattern, '', w).lower()
        # add word to dict
        if w in words_dict.keys():
            words_dict[w] = words_dict[w]+1
        else:
            words_dict[w] = 1


def construct_words(url: str):
    # breakpoint()
    base_soup = get_soup(url)
    base_words = get_words(base_soup)
    # add words in base web page to dictionary
    add_words_to_dict(base_words)
    links = get_links(base_soup, url)
    # scrap words from each child page (one level down)
    for l in links:
        child_soup = get_soup(l)
        child_words = get_words(child_soup)
        # then add words on the child page to the dictionary
        add_words_to_dict(child_words)


@app.get("/check")
def get_page_():
    return "welcome!", 200


@app.post("/page")
def get_page():

    # breakpoint()
    print(request.is_json)
    print(request.headers)
    try:
        req_data = request.get_json()
        if is_valid_url(req_data['page_url']):
            construct_words(req_data['page_url'])
            print(words_dict)
    except:
        return {"error": "page_url is not valid"}, 415

    return "words extracted from web "+req_data['page_url'], 200


@app.post("/search")
def search_word():
    # breakpoint()

    search_word = ""
    if request.is_json:
        search_word = request.get_json()['word']

    try:
        word_count = words_dict[search_word]
    except KeyError:
        return {"count": 0}, 200

    return {"count": word_count}, 200
