from bs4 import BeautifulSoup
from urlparse import urljoin
from urlnorm import norms
from urlparse import urlparse

SCHEME_HTTP = 'http://'
SCHEME_SEP = '://'

def get_domain(url):
  if SCHEME_SEP not in url:
    url = SCHEME_HTTP + url
  return urlparse(url).netloc

def is_same_domain(url1, url2):
  return get_domain(url1) == get_domain(url2)

def is_absolute(url):
  return bool(urlparse(url).netloc)

def get_urls(baseurl, htmltext):
  soup = BeautifulSoup(htmltext)
  ret = []
  links = soup.find_all('a')
  for tag in links:
    link = tag.get('href', None)
    if link != None:
      try:
	ret.append(join_urls(baseurl, link))
      except ValueError:
	pass
      except AttributeError:
	pass
  return ret

def join_urls(baseurl, url):
  if is_absolute(url):
    return norms(url)
  elif url.startswith('www.'):
    http_url = SCHEME_HTTP + url
    if is_absolute(http_url):
      return norms(http_url)
  else:
    return norms(urljoin(baseurl, url))
