import sqlite3
from datetime import datetime

def database_con(path: str):
  con = sqlite3.connect("{0}/fls_parse.db".format(path))
  return con

def createTable(name: str, con):
  print('Creating tables: {0}'.format(name))
  cur = con.cursor()
  cur.execute("CREATE TABLE {0}(md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime)".format(name.replace('-','_')))
  con.commit()

def inputValues(name: str, values, con):
  cur = con.cursor()
  cur.executemany("INSERT INTO {0} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()

def getTableData(name: str, con):
  cur = con.cursor()
  res = cur.execute("SELECT * FROM {0}".format(name))
  return res.fetchall()
