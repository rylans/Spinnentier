import requests
import re
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlparse
import logging
import dbmanager
from random import shuffle
from urlnorm import norms
from requester import Requester

DB_NAME = "crawler.db"
LOG_NAME = "crawler.log"

def is_absolute(url):
  return bool(urlparse(url).netloc)

def get_urls(baseurl, htmltext):
  soup = BeautifulSoup(htmltext)
  ret = []
  links = soup.find_all('a')
  for tag in links:
    link = tag.get('href', None)
    if link != None:
      ret.append(join_urls(baseurl, link))
  return ret

def join_urls(baseurl, url):
  if is_absolute(url):
    return norms(url)
  elif url.startswith('www.'):
    http_url = "http://" + url
    if is_absolute(http_url):
      return norms(http_url)
  else:
    return norms(urljoin(baseurl, url))
    
def http_success(status_code):
  return 200 <= status_code < 299

def main():
  db_manager = dbmanager.dbmanager(DB_NAME)
  logging.basicConfig(filename = LOG_NAME, filemode='w', level=logging.INFO)
  frontier = ["http://www.yahoo.co.jp","http://www.twitter.com"]
  frontier = [norms(f) for f in frontier]
  visited = {}
  db_visited = db_manager.get_visited()
  db_frontier = db_manager.get_frontier()

  frontier += db_frontier
  shuffle(frontier)

  for url in db_visited:
    print "Already visited: " + url
    visited[url] = 1

  MAX_THREADS = 6
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
	db_manager.insert_visited(t_urls[i], len(data[i]))
	if data[i]:
	  htmldata = data[i][0]

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
      t = Requester(url, 0.7, d) 
      t.start()
      threads.append(t)
      current_threads += 1

  #Join all threads before closing the database
  for t in threads:
    t.join()

  for i in range(len(t_urls)):
    db_manager.insert_visited(t_urls[i], len(data[i]))
    
    htmldata = ""
    if data[i]:
      htmldata = data[i][0]

    page_urls = get_urls(t_urls[i], htmldata)
    for page_url in page_urls:
      db_manager.insert_frontier(page_url, t_urls[i])
    frontier += page_urls

  db_manager.close()

if __name__ == '__main__':
  main()
