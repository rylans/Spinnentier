import requests
import re
from bs4 import BeautifulSoup
from urlparse import urljoin
import logging

def get_urls(baseurl, htmltext):
  soup = BeautifulSoup(htmltext)
  ret = []
  links = soup.find_all('a')
  for tag in links:
    link = tag.get('href', None)
    if link != None:
      ret.append(urljoin(baseurl, link))
  return ret

def main():
  logging.basicConfig(filename = 'crawler.log', filemode='w', level=logging.INFO)
  frontier = ["http://www.dmoz.org/", "http://en.wikipedia.org/wiki/Main_Page"]

  for url in frontier:
    logging.info("Requesting " + url)
    print "Requesting " + url
    r = requests.get(url)
    if(200 <= r.status_code <= 299):
      page_urls = get_urls(url, r.text)
      frontier += page_urls
    else:
      logging.warning("Request for " + url + " was not in 2xx range.")

if __name__ == '__main__':
  main()
