import unittest
import spinnentier
from urlparse import urljoin

class TestSequence(unittest.TestCase):
  def setUp(self):
    self.base = "http://basedomain.org/2014/04/article"
    self.html = """<html>
	      <head></head>
	      <body>
		<div>
		  <a href="http://www.otherdomain.ca">another domain link</a>
		</div>
		<span>
		  <a href="/nextpage">next</a>
		</span>
		<ul>
		<li>
		<a href="../foo/bar/">foobar</a>
		</li>
		</ul>
		<a href="www.mysite.gov/path/page">site</a>
		</body>
	      </html>"""

  def test_get_urls1(self):
    all_urls = spinnentier.get_urls(self.base, self.html)
    testurl = "http://www.otherdomain.ca"
    assert testurl in all_urls

  def test_get_urls2(self):
    all_urls = spinnentier.get_urls(self.base, self.html)
    testurl = "http://basedomain.org/nextpage"
    assert testurl in all_urls

  def test_get_urls3(self):
    all_urls = spinnentier.get_urls(self.base, self.html)
    testurl = "http://basedomain.org/2014/foo/bar/"
    assert testurl in all_urls
  
  def test_get_urls4(self):
    all_urls = spinnentier.get_urls(self.base, self.html)
    testurl = "http://www.mysite.gov/path/page"
    assert testurl in all_urls

  def test_is_same_domain1(self):
    url1 = "http://www.amazon.com/gp/store/books"
    url2 = "http://www.amazon.com/other/path"
    assert spinnentier.is_same_domain(url1, url2)

  def test_is_same_domain2(self):
    url1 = "http://www.japan.co.jp/p1"
    url2 = "http://www.uk.co.uk/p2"
    assert not spinnentier.is_same_domain(url1, url2)

  def test_is_same_domain3(self):
    url1 = "www.asdf.org/p1/foo/bar/rel=fsda"
    url2 = "http://www.asdf.org" 
    assert spinnentier.is_same_domain(url1, url2)

  def test_join_urls1(self):
    base = "//en.wikipedia.org/w/index.php"
    rel = "?title=Pacific"
    joint = spinnentier.join_urls(base, rel)
    correct = "http://en.wikipedia.org/w/index.php?title=Pacific"
    assert joint == correct

if __name__ == '__main__':
  unittest.main()
