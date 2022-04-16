# search-engine

## What is it?

Simple python tool to scrap all words from a web page and child pages via a href links(only one level down).

For simplicity sake all the words of the page are stored in memory using dictionary hash. When loading new page previous page's words are cleared out from memory.

Python Libraries Used

- `urllib` - to load, read, and decode html pages using url
- `beatifulSoup` - to beautify html and get texts
- `flask` - to build simple api

In addition, it includes a simple UI to demo the application. The UI page is html using bootstrap and jquery.

### How to run the dockerized app

Note: docker and docker-compose are used

1. Build the docker images (api and ui)

   `docker-compose build`

1. Run both api and ui docker containers
   `docker-compose up`

   api - uses port 5001

   ui - uses port 8080

   Note: if you dont have this ports availabe in the hosts machine, you may edit the docker-compose.yaml file for ports on each services

1. open browser http://localhost:8080

   Enter url for site you would like to scrap words in the url text box (eg https://subslikescript.com/movie/Titanic-120338)

   NOTE: Most website don't allow or want users to use scrapping tools like this, so check the site before trying.

1. Once the page is loaded, you may search for word in the text box shown
