import os.path
import requests
import sqlite3
import re
from bs4 import BeautifulSoup
from urlparse import urljoin
import logging

DB_NAME = "crawler.db"

def get_urls(baseurl, htmltext):
  soup = BeautifulSoup(htmltext)
  ret = []
  links = soup.find_all('a')
  for tag in links:
    link = tag.get('href', None)
    if link != None:
      ret.append(urljoin(baseurl, link))
  return ret

def get_db():
  if os.path.isfile(DB_NAME):
    return sqlite3.connect(DB_NAME)
  else:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE pages(url text, size integer)''')
    c.execute('''CREATE TABLE frontier(url text, size integer)''')
    conn.commit()
    return conn

def get_visited_from_db(conn):
  return [row[0] for row in conn.cursor().execute('SELECT * FROM pages')]

def get_frontier_from_db(conn):
  return [row[0] for row in conn.cursor().execute('SELECT * FROM frontier')]

def main():
  logging.basicConfig(filename = 'crawler.log', filemode='w', level=logging.INFO)
  frontier = ["http://www.dmoz.org/", "http://en.wikipedia.org/wiki/Main_Page"]
  visited = {}
  db_con = get_db()
  db_visited = get_visited_from_db(db_con)
  db_frontier = get_frontier_from_db(db_con)

  frontier += db_frontier

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
      if(200 <= r.status_code <= 299):
	params = (url, len(r.text))

	db_con.cursor().execute('INSERT INTO pages VALUES (?,?)', params)
	db_con.commit()

	page_urls = get_urls(url, r.text)

	for page_url in page_urls:
	  params = (page_url, 0)
	  db_con.cursor().execute('INSERT INTO frontier VALUES (?,?)', params)
	db_con.commit()

	frontier += page_urls
      else:
	logging.warning("Request for " + url + " was not in 2xx range.")
    except requests.exceptions.Timeout:
      logging.warning("Request for " + url + " timed out.")
    except requests.exceptions.ConnectionError:
      logging.warning("Request for " + url + " caused a connection error.")

  if db_con:
    db_con.close()

if __name__ == '__main__':
  main()
