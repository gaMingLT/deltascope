from cli.loger import main_logger

def input_values_events(name: str, values ,con):
  cur = con.cursor()
  main_logger.debug('Inserting values into Database: {0}_events'.format(name))
  cur.executemany("INSERT INTO {0}_events VALUES(?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()
  
def input_values_events_2(name: str, values ,con):
  cur = con.cursor()
  main_logger.debug('Inserting values into Database: {0}_events'.format(name))
  cur.executemany("INSERT INTO {0}_events VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()
  
def get_events_values(name: str, con):
  cur = con.cursor()
  main_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT * FROM {0}_events".format(name))
  return res.fetchall()

def get_events_image_values_year_count(name: str, con):
  cur = con.cursor()
  main_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT count(*) FROM {0}_events".format(name))
  return res.fetchall()

def get_events_image_values_neariest_date(name: str, con):
  cur = con.cursor()
  main_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT date FROM {0}_events order by date desc LIMIT 1".format(name))
  return res.fetchall()
