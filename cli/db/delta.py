from cli.loger import main_logger

def get_events_deltas(name: str, year: int ,con):
  cur = con.cursor()
  main_logger.debug("Retrieving values from database: {0}_events".format(name))
  res = cur.execute("SELECT json_group_array(json_object('Date', date,  'Size', size, 'mActivity',  mActivity, 'aActivity',  aActivity,'cActivity',  cActivity,'bActivity',  bActivity,'FileType',  fileType,'OwnerPerm', ownerPerm,'GroupPerm', groupPerm,'OtherPerm', otherPerm,'UUID', uid,'GUID', guid,'Inode', inode, 'Path', name)) FROM (SELECT * From {0}_events where date like '%{1}%' order by date desc limit 200) ".format(name, year))
  return res.fetchmany(size=500)
