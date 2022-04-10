from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

url = "http://olympus.realpython.org/profiles/dionysus"

page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
# remove newlines from soup using replace
init_words = soup.get_text().replace('\n', ' ')

list_words = init_words.split()
words_dict = {}

for w in list_words:
    # strip word of non-alphanumeric characters
    pattern = re.compile('\W')
    w = re.sub(pattern, '', w).lower()
    if w in words_dict.keys():
        words_dict[w] = words_dict[w]+1
    else:
        words_dict[w] = 1

print(words_dict)
