import sqlite3
from sqlite3 import Connection
from cli.loger import main_logger

def database_con(path: str) -> Connection:
  dbPath = "{0}/images_content.db".format(path)
  con = sqlite3.connect(database=dbPath, check_same_thread=False)
  main_logger.info('Connected to database: {0}'.format(dbPath))
  
  return con


def database_con_loaddb(filePath: str, outPath: str) -> Connection:
  dbPath = "{0}/loaddb/{1}.db".format(outPath, filePath.split('/')[-1].split('.')[0] )
  con = sqlite3.connect(database=dbPath, check_same_thread=False)
  main_logger.info('Connected to database: {0}'.format(dbPath))
  
  return con
 