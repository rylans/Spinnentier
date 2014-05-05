import threading
import logging
import requests

class Requester(threading.Thread):
  def __init__(self, url, timeout, output, max_size):
    self.url = url
    self.output = output
    self.timeout = timeout
    self.max_size = max_size
    super(Requester, self).__init__()

  def http_success(self, status_code):
    return 200 <= status_code < 299

  def run(self):
    url = self.url
    r = None
    try:
      r = requests.get(url, timeout=self.timeout, stream=True)
      clength = r.headers.get('content-length')
      if clength == None:
	clength = 0
      else:
	clength = int(clength)
      
      if clength > self.max_size:
	logging.warning("Request for " + url + " exceed max size.")
	return

      ctype = r.headers.get('content-type', "")
      if 'text/html' not in ctype:
	logging.warning("Request for " + url + " was not text/html but rather " + ctype)
	return

      if self.http_success(r.status_code):
	self.output.append(r.text)
      else:
	logging.warning("Status code for " + url + " was " + str(r.status_code))
      	
    except requests.exceptions.Timeout:
      logging.warning("Request for " + url + " timed out.")
    except requests.exceptions.InvalidSchema:
      logging.warning("Request for " + url + " caused an invalid schema exception.")
    except requests.exceptions.ConnectionError:
      logging.warning("Request for " + url + " caused a connection error.")
    except Exception as e:
      logging.exception("Request for " + url + " threw " + str(e))

    finally:
      if r:
	r.close()
