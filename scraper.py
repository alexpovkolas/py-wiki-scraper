from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import numpy as nm


class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]


    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)

        if response.getheader('Content-Type') and response.getheader('Content-Type').startswith('text/html'):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return list(filter(LinkParser.filter_page, self.links))
        else:
            return []

    @staticmethod
    def filter_page(l):
        return l.startswith("https://en.wikipedia.org/wiki")

def spider(url, maxPages):
    pagesToVisit = [url]
    number_visited = 0

    while number_visited < maxPages and pagesToVisit != []:
        number_visited = number_visited + 1
        url = pagesToVisit[0]
        number_visited = pagesToVisit[1:]
        try:
            print(number_visited, "Visiting:", url)
            parser = LinkParser()
            links = parser.getLinks(url)
            pagesToVisit = pagesToVisit + links
        except ValueError as err:
            print(" **Failed!**" + str(err))
