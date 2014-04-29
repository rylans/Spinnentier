import os.path
import sqlite3

class dbmanager:
  def __init__(self, database_name):
    if os.path.isfile(database_name):
      self.con = sqlite3.connect(database_name)
    else:
      self.con = sqlite3.connect(database_name)
      c = self.con.cursor()
      c.execute('''CREATE TABLE pages(url text, size integer)''')
      c.execute('''CREATE TABLE frontier(url text, parenturl text)''')
      self.con.commit()

  def get_visited(self):
    return [row[0] for row in self.con.cursor().execute('SELECT * FROM pages')]

  def get_frontier(self):
    return [row[0] for row in self.con.cursor().execute('SELECT * FROM frontier')]

  def insert_visited(self, url, size):
    params = (url, size)
    self.con.cursor().execute('INSERT INTO pages VALUES (?,?)', params)
    self.con.commit()

  def insert_frontier(self, url, parenturl):
    params = (url, parenturl)
    self.con.cursor().execute('INSERT INTO frontier VALUES (?,?)', params)
    self.con.commit()

  def close(self):
    self.con.close()
