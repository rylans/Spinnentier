from bs4 import BeautifulSoup
from urlparse import urljoin
from urlnorm import norms
from urlparse import urlparse

SCHEME_HTTP = 'http://'
SCHEME_SEP = '://'
NET_DOT = '.'
RESOURCE_JS = 'javascript:'
RESOURCE_MAILTO = 'mailto:'
MEDIA_EXT = ['.jpeg', '.jpg', '.gif', '.mp3', '.avi', '.wmv', '.png', '.wav',
	     '.bmp']
DOMAIN_PARTS = 3

def get_domain(url):
  if SCHEME_SEP not in url:
    url = SCHEME_HTTP + url
  netloc = urlparse(url).netloc
  while len(netloc.split(NET_DOT)) > DOMAIN_PARTS:
    netloc = NET_DOT.join(netloc.split(NET_DOT)[1:])
  return netloc

def is_same_domain(url1, url2):
  return get_domain(url1) == get_domain(url2)

def is_absolute(url):
  return bool(urlparse(url).netloc)

def is_blacklisted(url):
  url = url.lower()
  if RESOURCE_JS in url:
    return True
  if RESOURCE_MAILTO in url:
    return True
  for ext in MEDIA_EXT:
    if ext in url:
      return True
  return False

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
  if url.startswith('//'):
    url = 'http:' + url
    return norms(url)
  elif url.startswith('www.'):
    http_url = SCHEME_HTTP + url
    if is_absolute(http_url):
      return norms(http_url)
  elif is_absolute(url):
    return norms(url)
  else:
    return norms(urljoin(baseurl, url))
