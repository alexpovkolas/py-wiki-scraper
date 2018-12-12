from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from igraph import *
import matplotlib.pyplot as plt
import queue
import itertools
import threading
import time

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


urls_q = queue.Queue()
tasks = queue.Queue()
visited = set()
counter = itertools.count()


def worker(i, graph):
    while True:
        item = urls_q.get_nowait()
        if item is None:
            continue
        if item in visited:
            continue

        task = tasks.get()
        if task is None:
            break

        visited.add(item)
        #g.add_vertex(item)
        print(i, "Visiting:", item)
        print(next(counter), i, "Visiting:", item)
        parser = LinkParser()
        links = parser.getLinks(item)
        urls_q.task_done()
        graph[item] = links
        for l in links:
            urls_q.put_nowait(l)
            #g.add_vertex(l)
            #g.add_edge(item, l)

        tasks.task_done()


def spider(url, maxPages):
    start_time = time.time()
    for u in url:
        urls_q.put(u)
    for p in range(maxPages):
        tasks.put(p)

    threads = []
    graph = dict()
    for i in range(len(url)):
        t = threading.Thread(target=worker, args=[i, graph])
        t.start()
        threads.append(t)

    # block until all tasks are done
    tasks.join()

    # stop workers
    for i in range(len(url)):
        tasks.put(None)
    for t in threads:
        t.join(timeout=0.1)

    print("--- %s parsing seconds ---" % (time.time() - start_time))

    start_time = time.time()
    g = Graph()
    g.add_vertices(iter(visited))
    for vert, out_vert in graph.items():
        g.add_vertices(out_vert)
        g.add_edges([(vert, v) for v in out_vert])
        #for v in out_vert:
        #    g.add_edge(vert, v)
        #edges = [(vert, v) for v in out_vert]
        #g.add_edges(edges)
        #[g.add_edge(vert, v) for v in out_vert]


    print("--- %s graph creation seconds ---" % (time.time() - start_time))

    start_time = time.time()
    page_rank = g.pagerank()
    print("--- %s page rank seconds ---" % (time.time() - start_time))

    start_time = time.time()
    degree = g.degree()
    print("--- %s degree seconds ---" % (time.time() - start_time))

    g.degree_distribution()

    plt.hist(page_rank, density=True, log=True)
    plt.title('Histogram of PageRank')
    plt.ylabel('Probability')
    plt.show()

    plt.hist(degree, density=True, log=True)
    plt.title('Histogram of page degree')
    plt.ylabel('Probability')
    plt.show()

