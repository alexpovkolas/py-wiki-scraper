from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from igraph import *
import matplotlib.pyplot as plt

class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    if LinkParser.filter_page(value):
                        self.links.append(value)


    def getLinks(self, url):
        self.links = []
        response = urlopen(parse.urljoin("https://en.wikipedia.org", url))

        if response.getheader('Content-Type') and response.getheader('Content-Type').startswith('text/html'):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return self.links
        else:
            return []

    @staticmethod
    def filter_page(l):
        return l.startswith("/wiki") and ":" not in l # auxiliary pages have : inside the url


def spider(url, maxPages):
    pages_to_visit = [url]
    number_visited = 0
    g = Graph()

    while number_visited < maxPages and pages_to_visit != []:
        number_visited = number_visited + 1
        url = pages_to_visit[0]
        g.add_vertex(pages_to_visit[0])
        pages_to_visit = pages_to_visit[1:]

        try:
            print(number_visited, "Visiting:", url)
            parser = LinkParser()
            links = parser.getLinks(url)
            for link in links:
                g.add_vertex(link)
                g.add_edge(url, link)
            pages_to_visit.extend(links)
        except ValueError as err:
            print(" **Failed!**" + str(err))

    page_rank = g.pagerank()
    degree = g.degree()

    g.degree_distribution()

    plt.hist(page_rank, density=True, log=True)
    plt.title('Histogram of PageRank')
    plt.ylabel('Probability')
    plt.show()

    plt.hist(degree, density=True, log=True)
    plt.title('Histogram of page degree')
    plt.ylabel('Probability')
    plt.show()
