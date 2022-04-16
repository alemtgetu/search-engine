
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlsplit, urlparse

# url = "http://olympus.realpython.org/profiles"
# split_url = urlsplit(url)
# # print(split_url)
# # will be used as base url for relative paths in <a href>
# base_url = split_url.scheme+'://'+split_url.netloc
syncategorematic_words = ["a", "an", "is", "of", "and",
                          "the", "then", "to", "for", "but", "it", "all"]


def is_valid_url(url) -> bool:
    """Validate if string is valid url

    Parameters
    ----------
    url: str
        The url of the web page

    Returns
    -------
    bool
        True if it is valid url
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


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

    return([w for w in soup_obj.get_text().replace('\n', ' ').split() if w.lower() not in syncategorematic_words])


def get_links(soup_object: BeautifulSoup, url: str) -> list:
    """Get links (a href) from soup object and returns list of urls

    If the href is relative it will 
    Parameters
    ----------
    soup_obj: BeautifulSoup
        The soup object to get words from the page text
    url: str
        The URL of the page, will be used to create base url and create absolut url if link is relative
    Returns
    -------
    list
        a list of absolute urls
    """
    split_url = urlsplit(url)
    # will be used as base url for relative paths in <a href>
    base_url = split_url.scheme+'://'+split_url.netloc
    links = soup_object.select("a")
    absolute_urls = []
    for l in links:
        if bool(urlparse(l['href']).netloc):
            absolute_urls.append(l['href'])
        else:
            absolute_urls.append(base_url+l['href'])
    return absolute_urls
