import codecs, datetime
from cli.loger import main_logger
from os import system

def execute_fls(path: str, out: str) -> str:
  main_logger.info('[METHODS] - Retrieving files from image using FLS')
  
  bodyFilePath = "{0}/{1}.txt".format(out, path.split('/')[-1].split('.')[0])
  cmd = "{0} {1} {2} {3} > {4}".format("fls", "-r -h -m",'/', path ,bodyFilePath)
  res = system(cmd)
  
  if res == 0:
    main_logger.info('[METHODS] - FLS Execution - Succes!')
    
  return bodyFilePath


def parse_fls_body_file(path: str, out: str) -> list:
  main_logger.info('[METHODS] - Parsing body file')
  
  # f = open(path, "r")
  f = codecs.open(path, encoding='utf-8', errors='ignore')
  
  data = []
  for line in f.readlines():
    # MD5,name,inode,mode_as_string,UID,GID,size,atime,mtime,ctime,crtime
    md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime = line.split('|')
    data.append((md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime))
  
  return data
