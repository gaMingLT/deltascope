import sqlite3, logging
import datetime
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

def database_con(path: str):
  con = sqlite3.connect("{0}/fls_parse.db".format(path))
  db_logger.info('Connected to database')
  return con

def createTable(name: str, con):
  db_logger.debug('Creating table: {0}'.format(name))
  cur = con.cursor()
  cur.execute("CREATE TABLE {0}(md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime)".format(name.replace('-','_')))
  con.commit()

def inputValues(name: str, values, con):
  cur = con.cursor()
  db_logger.debug('Inserting values into Database: {0}'.format(name))
  cur.executemany("INSERT INTO {0} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()

def getTableData(name: str, con):
  cur = con.cursor()
  db_logger.debug('Retrieving values from database: {0}'.format(name))
  res = cur.execute("SELECT * FROM {0}".format(name))
  return res.fetchall()
