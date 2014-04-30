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

if __name__ == '__main__':
  unittest.main()
