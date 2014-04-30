import threading
import logging
import requests

class Requester(threading.Thread):
  def __init__(self, url, timeout, output):
    self.url = url
    self.output = output
    self.timeout = timeout
    super(Requester, self).__init__()

  def http_success(self, status_code):
    return 200 <= status_code < 299

  def run(self):
    url = self.url
    try:
      r = requests.get(url, timeout=self.timeout)
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
      logging.warning("Request for " + url + " threw " + str(e))
