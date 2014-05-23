import logging
import dbmanager
from random import shuffle
from requester import Requester
from urlutils import get_urls
from urlutils import is_same_domain
from urlutils import get_domain
from urlutils import is_blacklisted
from urlutils import join_urls

DB_NAME = "crawler.db"
LOG_NAME = "crawler.log"
MAX_THREADS = 16
MAX_REQ_PER_DOMAIN = 8
TIME_LIMIT = 0.7
MAX_SIZE_BYTES = 1024 * 512

def main():
  db_manager = dbmanager.dbmanager(DB_NAME)
  logging.basicConfig(filename = LOG_NAME, 
		      format='%(asctime)s:%(levelname)s:%(message)s',
		      filemode='w', level=logging.WARN)
  frontier = ['http://www.theonion.com','http://www.reddit.com']
  visited = {}
  domains = {}
  db_visited = db_manager.get_visited()
  db_frontier = db_manager.get_frontier()

  frontier += db_frontier
  #shuffle(frontier)

  for url in db_visited:
    print "Already visited: " + url
    visited[url] = 1

  current_threads = 0
  threads = []
  data = []
  t_urls = []
  
  for url in frontier:
    if visited.get(url, None):
      logging.info("Not requesting " + url + " because it has already been visited.")
      continue

    if domains.get(get_domain(url), 0) >= MAX_REQ_PER_DOMAIN:
      logging.info("Not requesting " + url + " because max requests per domain has been exceeded.")
      continue

    if is_blacklisted(url):
      logging.info("Not requesting " + url + " because it is blacklisted.")
      continue

    if(current_threads < MAX_THREADS):
      logging.info("Requesting " + url)
      print "Requesting " + url + " as t=" + str(current_threads)
      visited[url] = 1

      urldom = get_domain(url)
      if urldom in domains:
	domains[urldom] += 1
      else:
	domains[urldom] = 1

      d = []
      data.append(d)
      t_urls.append(url)
      t = Requester(url, TIME_LIMIT, d, MAX_SIZE_BYTES)
      t.start()
      threads.append(t)
      current_threads += 1

    if((current_threads >= MAX_THREADS) or (url == frontier[-1])):
      current_threads = 0
      for t in threads:
	t.join()

      for i in range(len(t_urls)):
	htmldata = ""
	if data[i]:
	  htmldata = data[i][0]
	db_manager.insert_visited(t_urls[i], len(htmldata))

	page_urls = list(set(get_urls(t_urls[i], htmldata)))
	db_manager.insert_frontier(page_urls, t_urls[i])
	frontier += page_urls

      threads = []
      data = []
      t_urls = []

  db_manager.close()

if __name__ == '__main__':
  main()
