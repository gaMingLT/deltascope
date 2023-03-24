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


def createFilesImageTable(name: str, con):
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
  
def create_timeline_image_table_2(name: str, con):
  db_logger.debug('Creating table: {0}_events'.format(name))
  cur = con.cursor()
  cur.execute("CREATE TABLE {0}_events(date, size, mActivity, aActivity, cActivity, bActivity, fileType, ownerPerm, groupPerm, otherPerm ,uid,guid,inode,name)".format(name.replace('-','_')))
  con.commit()
  

def inputValuesImageTimelineTable(name: str, values ,con):
  cur = con.cursor()
  db_logger.debug('Inserting values into Database: {0}_events'.format(name))
  cur.executemany("INSERT INTO {0}_events VALUES(?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()
  
def input_values_timeline_image_table_2(name: str, values ,con):
  cur = con.cursor()
  db_logger.debug('Inserting values into Database: {0}_events'.format(name))
  cur.executemany("INSERT INTO {0}_events VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()
  
def getImageEventsValues(name: str, con):
  cur = con.cursor()
  db_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT * FROM {0}_events".format(name))
  return res.fetchall()

def get_events_image_values_year_count(name: str, con):
  cur = con.cursor()
  db_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT count(*) FROM {0}_events".format(name))
  return res.fetchall()

def get_events_image_values_year(name: str, year: int ,con):
  cur = con.cursor()
  db_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT json_group_array(json_object('Date', date,  'Size', size, 'mActivity',  mActivity, 'aActivity',  aActivity,'cActivity',  cActivity,'bActivity',  bActivity,'FileType',  fileType,'OwnerPerm', ownerPerm,'GroupPerm', groupPerm,'OtherPerm', otherPerm,'UUID', uid,'GUID', guid,'Inode', inode, 'Path', name)) FROM (SELECT * From {0}_events where date like '%{1}%' order by date desc limit 100) ".format(name, year))
  return res.fetchmany(size=500)

def get_events_image_delta(names: str, con):
  cur = con.cursor()
  db_logger.debug('Retrieving delta values from database: {0}'.format(names))
  res = cur.execute("SELECT * FROM {0}_events WHERE date NOT IN (SELECT date FROM {1}_events) LIMIT 100".format(names[1], names[0]))
  return res.fetchall()

def get_events_image_delta_year(base: str, next: str, year: int ,con):
  cur = con.cursor()
  db_logger.debug('Retrieving delta values from database: {0} - {1}'.format(base, next))
  # res = cur.execute("SELECT json_group_array(json_object('Date', date,  'Size', size, 'mActivity',  mActivity, 'aActivity',  aActivity,'cActivity',  cActivity,'bActivity',  bActivity,'FileType',  fileType,'OwnerPerm', ownerPerm,'GroupPerm', groupPerm,'OtherPerm', otherPerm,'UUID', uid,'GUID', guid,'Inode', inode, 'Path', name)) FROM (SELECT * From {0}_events where date like '%{1}%' order by date desc limit 100) WHERE date NOT IN(SELECT date FROM (SELECT * From {1}_events where date like '%{2}%' order by date desc limit 100)) and date like '%{2}%' ORDER BY date".format(next, base, year))
  res = cur.execute("SELECT json_group_array(json_object('Date', date,  'Size', size, 'mActivity',  mActivity, 'aActivity',  aActivity,'cActivity',  cActivity,'bActivity',  bActivity,'FileType',  fileType,'OwnerPerm', ownerPerm,'GroupPerm', groupPerm,'OtherPerm', otherPerm,'UUID', uid,'GUID', guid,'Inode', inode, 'Path', name)) FROM (SELECT * FROM {0}_events where date not in (SELECT date from {1}_events) order by date desc limit 100)".format(next, base))
  return res.fetchall()
