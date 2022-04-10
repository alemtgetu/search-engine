from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlsplit, urlparse
import re

url = "http://olympus.realpython.org/profiles"
split_url = urlsplit(url)
# print(split_url)
# will be used as base url for relative paths in <a href>
base_url = split_url.scheme+'://'+split_url.netloc


def get_soup(url: str) -> BeautifulSoup:
    """Reads web page and return soup object

    Parameters
    ----------
    url: str
        The url of the web page

    Returns
    -------
    BeautifulSoup
        Soup object
    """
    page = urlopen(url)
    html = page.read().decode("utf-8")
    return(BeautifulSoup(html, "html.parser"))


def get_words(soup_obj: BeautifulSoup) -> list:
    """Get all words(text) from soup object and returns list of the words

    Parameters
    ----------
    soup_obj: BeautifulSoup
        The soup object to get words from the page text

    Returns
    -------
    list
        a list of words from the web page
    """
    return(soup_obj.get_text().replace('\n', ' ').split())


# (Indexing words)
# Lets use dictionary for now and add words to the main dictionary
# each word will be key and the count of the words will be the value
# page_words_list is a list of found in the page
words_dict = {}


def add_words_to_words_dict(page_words_list: list):
    """Accepts list of words and add the words to dictionary words_dict{}

    Each word as a key and the count of the word as value
    Parameters
    ----------
    page_words_list: list
        The list of all the words to be added to words_dict{}
    """
    for w in page_words_list:
        # strip word of non-alphanumeric characters
        pattern = re.compile('\W')
        w = re.sub(pattern, '', w).lower()
        # add word to dict
        if w in words_dict.keys():
            words_dict[w] = words_dict[w]+1
        else:
            words_dict[w] = 1


base_soup = get_soup(url)
base_words = get_words(base_soup)
# print(base_words)
add_words_to_words_dict(base_words)
# print(words_dict)
# get links (a hrefs) from the site
# some hrefs could be relative path
# check if the hrefs in a is absolute
# if not use base_url and create absolute path of that url
links = base_soup.select("a")
all_absolute_url = []
for l in links:
    if bool(urlparse(l['href']).netloc):
        all_absolute_url.append(l['href'])
    else:
        all_absolute_url.append(base_url+l['href'])
# links_url = [base_url+l["href"] for l in links]
# print(all_absolute_url)

# if there are links in the page
# lets also scrap all words from those pages (one level down only)
for child_url in all_absolute_url:
    # .get_text().replace('\n', ' ')
    page_words = get_words(get_soup(child_url))
    add_words_to_words_dict(page_words)


print(words_dict)
