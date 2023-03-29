from cli.loger import main_logger

def get_events_json(name: str, year: int ,con):
  cur = con.cursor()
  main_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT json_group_array(json_object('Date', date,  'Size', size, 'mActivity',  mActivity, 'aActivity',  aActivity,'cActivity',  cActivity,'bActivity',  bActivity,'FileType',  fileType,'OwnerPerm', ownerPerm,'GroupPerm', groupPerm,'OtherPerm', otherPerm,'UUID', uid,'GUID', guid,'Inode', inode, 'Path', name)) FROM (SELECT * From {0}_events where date like '%{1}%' order by date desc limit 200) ".format(name, year))
  return res.fetchmany(size=500)

def get_events_delta(base: str, next: str, year: int ,con):
  cur = con.cursor()
  main_logger.debug('Retrieving delta values from database: {0} - {1}'.format(base, next))
  res = cur.execute("SELECT json_group_array(json_object('Date', date,  'Size', size, 'mActivity',  mActivity, 'aActivity',  aActivity,'cActivity',  cActivity,'bActivity',  bActivity,'FileType',  fileType,'OwnerPerm', ownerPerm,'GroupPerm', groupPerm,'OtherPerm', otherPerm,'UUID', uid,'GUID', guid,'Inode', inode, 'Path', name)) FROM (SELECT * FROM {0}_events where date not in (SELECT date from {1}_events) order by date desc limit 200)".format(next, base))
  return res.fetchall()


# def get_events_loaddb_contentdb(name: str, con):
  