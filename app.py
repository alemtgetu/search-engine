# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from engine import get_soup, get_words, get_links

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


@app.post("/page")
def get_page():

    # breakpoint()

    # try:
    #     base_url = request.args['page_url']
    # except:
    #     return {"error": "page_url is required"}, 415

    return "hi", 200


@app.get("/search")
def search_word():
    # breakpoint()
    # print(request)
    # words_dict = {}
    try:
        base_url = request.args['url']
        search_word = request.args['word']

    except:
        return {"error": "url and word aren't passed correctly"}, 415

    construct_words(base_url)
    print(words_dict)
    try:
        word_count = words_dict[search_word]
    except KeyError:
        return {"count": 0}, 200

    return {"count": word_count}, 200
