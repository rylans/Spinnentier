import logging
import dbmanager
from random import shuffle
from requester import Requester
from urlutils import get_urls

DB_NAME = "crawler.db"
LOG_NAME = "crawler.log"
MAX_THREADS = 12
TIME_LIMIT = 0.7

def main():
  db_manager = dbmanager.dbmanager(DB_NAME)
  logging.basicConfig(filename = LOG_NAME, filemode='w', level=logging.INFO)
  frontier = ["http://www.yahoo.co.jp","http://www.twitter.com"]
  visited = {}
  db_visited = db_manager.get_visited()
  db_frontier = db_manager.get_frontier()

  frontier += db_frontier
  shuffle(frontier)

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

    if(current_threads >= MAX_THREADS):
      current_threads = 0
      for t in threads:
	t.join()

      for i in range(len(t_urls)):
	htmldata = ""
	if data[i]:
	  htmldata = data[i][0]
	db_manager.insert_visited(t_urls[i], len(htmldata))

	page_urls = get_urls(t_urls[i], htmldata)
	for page_url in page_urls:
	  db_manager.insert_frontier(page_url, t_urls[i])
	frontier += page_urls

      threads = []
      data = []
      t_urls = []

    if(current_threads < MAX_THREADS):
      logging.info("Requesting " + url)
      print "Requesting " + url + " as t=" + str(current_threads)
      visited[url] = 1

      d = []
      data.append(d)
      t_urls.append(url)
      t = Requester(url, TIME_LIMIT, d) 
      t.start()
      threads.append(t)
      current_threads += 1

  #Join all threads before closing the database
  for t in threads:
    t.join()

  for i in range(len(t_urls)):
    htmldata = ""
    if data[i]:
      htmldata = data[i][0]
    db_manager.insert_visited(t_urls[i], len(htmldata))

    page_urls = get_urls(t_urls[i], htmldata)
    for page_url in page_urls:
      db_manager.insert_frontier(page_url, t_urls[i])
    frontier += page_urls

  db_manager.close()

if __name__ == '__main__':
  main()
