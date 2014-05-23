import logging
from bs4 import BeautifulSoup
import pickle

class Indexer:
  '''Index pages using an inverted index.'''
  filename = "index.pkl"
  def __init__(self, index):
    self.index = index

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

  def search(self, query):
    query_words = query.split()
    candidate_urls = []
    for query_word in query_words:
      if self.index.get(query_word, None):
	candidate_urls.append(self.index.get(query_word))

    urls = []
    for candidate_url in candidate_urls:
      for url in candidate_url:
	urls.append(url)

    return urls

if __name__ == '__main__':
  index_dict = {}
  try:
    pkl_file = open(Indexer.filename, 'rb')
    index_dict = pickle.load(pkl_file)
    pkl_file.close()
  except IOError:
    print "Pickle file not found."

  idx = Indexer(index_dict)
  result = idx.search("honda car race")
  print "RESULTS:"
  for i in result:
    print i
