import os.path
import sqlite3

class dbmanager:
  PAGE_TABLE = "pages"
  FRONTIER_TABLE = "frontier"

  def __init__(self, database_name):
    if os.path.isfile(database_name):
      self.con = sqlite3.connect(database_name)
    else:
      self.con = sqlite3.connect(database_name)
      c = self.con.cursor()
      c.execute('''CREATE TABLE pages(url text, size integer)''')
      c.execute('''CREATE TABLE frontier(url text, parenturl text)''')
      self.con.commit()
    self.con.text_factory = str

  def show_all(self):
    string = ""
    string += self.show_pages() + "\n"
    string += self.sample_pages() + "\n"
    string += self.show_frontier() + "\n"
    string += self.sample_frontier()
    return string

  def _show_table(self, tablename):
    rows = [row for row in self.con.cursor().execute('SELECT COUNT(*) FROM ' + tablename)]
    count = rows[0][0]
    string = tablename + " (" + str(count) + ")"
    return string

  def show_pages(self):
    return self._show_table(dbmanager.PAGE_TABLE)

  def show_frontier(self):
    return self._show_table(dbmanager.FRONTIER_TABLE)
    
  def _sample_table(self, tablename, count):
    count = str(count)
    rows = [row for row in self.con.cursor().execute('SELECT * FROM ' + tablename + ' LIMIT ' + count)]
    string = ""
    for r in rows:
      string += r[0] + ", " + str(r[1]) + "\n"
    return string

  def sample_pages(self):
    string = "URL, SIZE\n"
    return string + self._sample_table(dbmanager.PAGE_TABLE, 8)

  def sample_frontier(self):
    string = "URL, PARENT\n"
    return string + self._sample_table(dbmanager.FRONTIER_TABLE, 8)

  def _get_table(self, tablename):
    return [row[0] for row in self.con.cursor().execute('SELECT * FROM ' + tablename)]

  def get_visited(self):
    return self._get_table(dbmanager.PAGE_TABLE)

  def get_frontier(self):
    return self._get_table(dbmanager.FRONTIER_TABLE)

  def insert_visited(self, url, size):
    params = (url, size)
    self.con.cursor().execute('INSERT INTO pages VALUES (?,?)', params)
    self.con.commit()

  def insert_frontier(self, urls, parenturl):
    for url in urls:
      params = (url, parenturl)
      self.con.cursor().execute('INSERT INTO frontier VALUES (?,?)', params)
    self.con.commit()

  def close(self):
    self.con.close()

if __name__ == '__main__':
  dbman = dbmanager("crawler.db")
  print dbman.show_all()
