import requests
import re
from bs4 import BeautifulSoup
from urlparse import urljoin
from urlparse import urlparse
import logging
import dbmanager
from random import shuffle
from urlnorm import norms

DB_NAME = "crawler.db"

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
  logging.basicConfig(filename = 'crawler.log', filemode='w', level=logging.INFO)
  frontier = ["http://www.yahoo.co.jp","http://www.twitter.com"]
  frontier = [norms(f) for f in frontier]
  visited = {}
  db_visited = db_manager.get_visited()
  db_frontier = db_manager.get_frontier()

  frontier += db_frontier
  #shuffle(frontier)

  for url in db_visited:
    print "Already visited: " + url
    visited[url] = 1

  for url in frontier:
    if visited.get(url, None):
      logging.info("Not requesting " + url + " because it has already been visited.")
      continue

    logging.info("Requesting " + url)
    print "Requesting " + url
    try:
      visited[url] = 1
      r = requests.get(url, timeout=0.7)
      if http_success(r.status_code):
	db_manager.insert_visited(url, len(r.text))
	page_urls = get_urls(url, r.text)

	for page_url in page_urls:
	  db_manager.insert_frontier(page_url, url)

	frontier += page_urls
      else:
	logging.warning("Status code for " + url + " was " + str(r.status_code))

    except requests.exceptions.Timeout:
      logging.warning("Request for " + url + " timed out.")
    except requests.exceptions.InvalidSchema:
      logging.warning("Request for " + url + " caused an invalid schema exception.")
    except requests.exceptions.ConnectionError:
      logging.warning("Request for " + url + " caused a connection error.")
    except Exception as e:
      logging.warning("Request for " + url + " threw " + str(e))

  db_manager.close()

if __name__ == '__main__':
  main()
