import codecs, datetime
from cli.loger import main_logger
from os import system, mkdir, path


def load_database_from_image(imagePath: str, out: str):
  main_logger.info('[LOADDB] - Creating tsk_loaddb from image')
  
  if not path.exists('{0}/{1}'.format(out,'loaddb')):
    mkdir('{0}/{1}'.format(out,'loaddb'))
  
  outputFileName = imagePath.split('/')[-1].split('.')[0] 
  cmd = "tsk_loaddb {0} -d {1}/loaddb/{2}.db".format(imagePath, out, outputFileName)
  res = system(cmd)
  
  if res == 0:
    main_logger.info('[LOADDB] - Loading database from image - Succes!')

  return
