import logging
from bs4 import BeautifulSoup

class Indexer:
  '''Index pages using an inverted index.'''
  def __init__(self):
    self.index = {}

  def index_page(self, url, html):
    soup = BeautifulSoup(html)
    text = soup.stripped_strings

    words = []
    for text_item in text:
      text_split = text_item.split()
      for t in text_split:
	words.append(t.lower())
    
    for word in words:
      if self.index.get(word, None):
	if url not in self.index[word]:
	  self.index[word].append(url)
      else:
	self.index[word] = [url]
