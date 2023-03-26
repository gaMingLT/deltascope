import hashlib, datetime, dateparser
from os import mkdir, path, system
from cli.loger import main_logger

def image_info(path: str):
  main_logger.debug('[METHODS] - Image info: {0}'.format(path))
  
  BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
  md5 = hashlib.md5()

  with open(path, 'rb') as f:
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)

  main_logger.info("MD5: {0}".format(md5.hexdigest()))


def prepare_filesystem(paths, out: str) -> str:
  main_logger.debug('[METHODS] - Preparing filesystem: Images:  {0} - Out: {1}'.format(paths,out))
  
  # Create output directory for files used in differentiating
  if not path.exists(out):
    mkdir('{0}'.format(out))
  
  dateTime = str(datetime.datetime.now())
  pathOutPutDir = "{0}/deltascope-{1}".format(out,dateTime.replace(' ', '_').replace('.','-'))
  
  mkdir(pathOutPutDir)
  
  return pathOutPutDir
