import sqlite3, logging, os
from sqlite3 import Connection, DatabaseError, OperationalError
from loger import CustomFormatter


def create_db_logger():
  # Create custom logger logging all five levels
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)

  # Define format for logs
  fmt = '%(asctime)s | %(levelname)8s | %(message)s'

  # Create stdout handler for logging to the console (logs all five levels)
  stdout_handler = logging.StreamHandler()
  stdout_handler.setLevel(logging.DEBUG)
  stdout_handler.setFormatter(CustomFormatter(fmt))

  # Add both handlers to the logger
  logger.addHandler(stdout_handler)
  
  return logger

db_logger = create_db_logger()

def database_con(path: str) -> Connection:
  dbPath = "{0}/images_content.db".format(path)
  print('Path: ', dbPath)
  con = sqlite3.connect(database=dbPath, check_same_thread=False)
  db_logger.info('Connected to database: {0}'.format(dbPath))
  
  return con


def createImageFilesTable(name: str, con):
  db_logger.debug('Creating table: {0}_files'.format(name))
  cur = con.cursor()
  cur.execute("CREATE TABLE {0}_files(md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime)".format(name.replace('-','_')))
  con.commit()

def inputValuesImageFilesTable(name: str, values, con):
  cur = con.cursor()
  db_logger.debug('Inserting values into Database: {0}'.format(name))
  cur.executemany("INSERT INTO {0}_files VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()

def getImageFilesValues(name: str, con):
  cur = con.cursor()
  db_logger.debug('Retrieving values from database: {0}'.format(name))
  res = cur.execute("SELECT * FROM {0}_files LIMIT 100".format(name))
  return res.fetchall()

def getImageFilesValuesPath(name: str, path: str, con):
  cur = con.cursor()
  db_logger.debug('Retrieving values from database: {0}'.format(name))
  res = cur.execute("SELECT * FROM {0}_files where name like '{1}%' ORDER BY mtime DESC".format(name, path))
  return res.fetchall()

def createImageTimelineTable(name: str, con):
  db_logger.debug('Creating table: {0}_events'.format(name))
  cur = con.cursor()
  cur.execute("CREATE TABLE {0}_events(date,size,activity,permissions,uid,guid,inode,name)".format(name.replace('-','_')))
  con.commit()

def inputValuesImageTimelineTable(name: str, values ,con):
  cur = con.cursor()
  db_logger.debug('Inserting values into Database: {0}_events'.format(name))
  cur.executemany("INSERT INTO {0}_events VALUES(?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()
  
def getImageEventsValues(name: str, con):
  cur = con.cursor()
  db_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT * FROM {0}_events".format(name))
  return res.fetchall()

def getImageEventsValuesYear(name: str, year: int ,con):
  cur = con.cursor()
  db_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT * FROM {0}_events where date like '%{1}%'".format(name, year))
  return res.fetchall()

def getImageEventsDelta(names: str, con):
  cur = con.cursor()
  db_logger.debug('Retrieving delta values from database: {0}'.format(names))
  res = cur.execute("SELECT * FROM {0}_events WHERE date NOT IN (SELECT date FROM {1}_events) LIMIT 100".format(names[1], names[0]))
  return res.fetchall()

def getImageEventsDeltaYear(names: str, year: int ,con):
  cur = con.cursor()
  db_logger.debug('Retrieving delta values from database: {0}'.format(names))
  res = cur.execute("SELECT * FROM {0}_events WHERE date NOT IN (SELECT date FROM {1}_events)  and date like '%{2}%' ".format(names[1], names[0], year))
  return res.fetchall()
