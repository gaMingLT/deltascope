from cli.loger import main_logger

def input_values_files(name: str, values, con):
  cur = con.cursor()
  main_logger.debug('Inserting values into Database: {0}'.format(name))
  cur.executemany("INSERT INTO {0}_files VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()

def get_files_values_path(name: str, path: str, con):
  cur = con.cursor()
  main_logger.debug('Retrieving values from database: {0}'.format(name))
  res = cur.execute("SELECT * FROM {0}_files where name like '{1}%' ORDER BY mtime DESC".format(name, path))
  return res.fetchall()
