from cli.loger import main_logger

def input_values_events(name: str, values ,con):
  cur = con.cursor()
  main_logger.debug('Inserting values into Database: {0}_events'.format(name))
  cur.executemany("INSERT INTO {0}_events VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(name.replace('-','_')), values)
  con.commit()

def get_events_json(name: str, year: int ,con):
  cur = con.cursor()
  main_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT json_group_array(json_object('Date', date,  'Size', size, 'mActivity',  mActivity, 'aActivity',  aActivity,'cActivity',  cActivity,'bActivity',  bActivity,'FileType',  fileType,'OwnerPerm', ownerPerm,'GroupPerm', groupPerm,'OtherPerm', otherPerm,'UUID', uid,'GUID', guid,'Inode', inode, 'Path', name)) FROM (SELECT * From {0}_events where date like '%{1}%' order by date desc limit 200) ".format(name, year))
  return res.fetchmany(size=500)

def get_events_image_values_neariest_date(name: str, con):
  cur = con.cursor()
  main_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT date FROM {0}_events order by date desc LIMIT 1".format(name))
  return res.fetchall()
