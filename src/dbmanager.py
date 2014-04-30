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

  def show_all(self):
    string = ""
    string += self.show_pages() + "\n"
    string += self.sample_pages() + "\n"
    string += self.show_frontier() + "\n"
    string += self.sample_frontier()
    return string

  def show_pages(self):
    rows = [row for row in self.con.cursor().execute('SELECT COUNT(*) FROM pages')]
    count = rows[0][0]
    string = "PAGES (" + str(count) + ")"
    return string

  def show_frontier(self):
    rows = [row for row in self.con.cursor().execute('SELECT COUNT(*) FROM frontier')]
    count = rows[0][0]
    string = "FRONTIER (" + str(count) + ")"
    return string

  def sample_pages(self):
    rows = [row for row in self.con.cursor().execute('SELECT * FROM pages LIMIT 8')]
    string = "URL, SIZE\n"
    for r in rows:
      string += r[0] + ", " + str(r[1]) + "\n"
    return string

  def sample_frontier(self):
    rows = [row for row in self.con.cursor().execute('SELECT * FROM frontier LIMIT 8')]
    string = "URL, PARENT\n"
    for r in rows:
      string += r[0] + ", " + str(r[1]) + "\n"
    return string

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

if __name__ == '__main__':
  dbman = dbmanager("crawler.db")
  print dbman.show_all()
