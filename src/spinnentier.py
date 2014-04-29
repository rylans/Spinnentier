import requests
import re
from bs4 import BeautifulSoup

def get_urls(htmltext):
  urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', htmltext)
  return urls

def get_urls2(htmltext):
  soup = BeautifulSoup(htmltext)
  ret = []
  links = soup.find_all('a')
  for tag in links:
    link = tag.get('href', None)
    if link != None:
      ret.append(link)
  return ret


def main():
  seeds = ["http://www.dmoz.org/", "http://en.wikipedia.org/wiki/Main_Page"]
  frontier = []

  for url in seeds:
    r = requests.get(url)
    if(200 <= r.status_code <= 299):
      print
      print get_urls2(r.text)

if __name__ == '__main__':
  main()
