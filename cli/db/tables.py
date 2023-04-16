from cli.loger import main_logger

def create_files_table(name: str, con):
  main_logger.debug('Creating table: {0}_files'.format(name))
  cur = con.cursor()
  cur.execute("CREATE TABLE {0}_files(md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime)".format(name.replace('-','_')))
  con.commit()

def create_events_table(name: str, con):
  main_logger.debug('Creating table: {0}_events'.format(name))
  cur = con.cursor()
  cur.execute("CREATE TABLE {0}_events(date, size, mActivity, aActivity, cActivity, bActivity, fileType, ownerPerm, groupPerm, otherPerm ,uid,guid,inode,name)".format(name.replace('-','_')))
  con.commit()
