import hashlib
from os import mkdir, path, system
import datetime, logging
from loger import CustomFormatter

def create_methods_logger():
  # Create custom logger logging all five levels
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)

  # Define format for logs
  fmt = '%(asctime)s | %(levelname)8s | %(message)s'

  # Create stdout handler for logging to the console (logs all five levels)
  stdout_handler = logging.StreamHandler()
  stdout_handler.setLevel(logging.DEBUG)
  stdout_handler.setFormatter(CustomFormatter(fmt))

  # Add both handlers to the logger
  logger.addHandler(stdout_handler)
  
  return logger

methods_logger = create_methods_logger()


def imageInfo(path: str):
  methods_logger.debug('Image info: {0}'.format(path))
  
  BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
  md5 = hashlib.md5()

  with open(path, 'rb') as f:
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)

  methods_logger.info("MD5: {0}".format(md5.hexdigest()))

def prepareFilesystem(paths, out: str) -> str:
  methods_logger.debug('Preparing filesystem: Images:  {0} - Out: {1}'.format(paths,out))
  
  # Create output directory for files used in differentiating
  if not path.exists(out):
    mkdir('{0}'.format(out))
  
  dateTime = str(datetime.datetime.now())
  pathOutPutDir = "{0}/deltascope-{1}".format(out,dateTime.replace(' ', '_').replace('.','-'))
  
  mkdir(pathOutPutDir)
  
  return pathOutPutDir

def executeFls(path: str, out: str) -> str:
  methods_logger.info('Retrieving files from image using FLS')
  
  bodyFilePath = "{0}/{1}.txt".format(out, path.split('/')[-1].split('.')[0])
  cmd = "{0} {1} {2} {3} > {4}".format("fls", "-r -h -m",'/', path ,bodyFilePath)
  res = system(cmd)
  
  if res == 0:
    methods_logger.info('FLS Execution - Succes!')
    
  return bodyFilePath

def parseBodyFile(path: str, out: str) -> list:
  methods_logger.info('Parsing body file')
  
  f = open(path, "r")
  data = []
  
  for line in f.readlines():
    # MD5,name,inode,mode_as_string,UID,GID,size,atime,mtime,ctime,crtime
    md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime = line.split('|')
    data.append((md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime))
  
  return data


def compareHashAndPath(data, con):
  methods_logger.info('Comparing hash and path: ')
  hashAndPathImages = []
  
  for img in data:
    # hashAndPath = []
    hashPathMode = []
    for row in img[1]:
      # hashAndPath.append((row[0], row[1]))
      hashPathMode.append((row[0],row[1], row[2] ,row[3]))
    hashAndPathImages.append((img[0], hashPathMode))


  deltas = []
  deltaImage = { 'delta': hashAndPathImages[0][0], 'next': hashAndPathImages[1][0], 'differences': {} }
  differences = { 'same': [] ,'deleted': [], 'modified': [], 'moved': [] , 'new': [], 'swap': [] }
  
  baseImage = hashAndPathImages[0][1]
  nextImage =  hashAndPathImages[1][1]
  basePaths = []
  
  for nextRow in nextImage:
    nextHash = nextRow[0]
    nextPath = nextRow[1]

    # nextPathFileDir = nextPath.split('/')[-1]
    # lengthNextDir = len(nextPathFileDir)
    # nextPathLocation = nextPath[:(len(nextPath)-lengthNextDir)]
    # print(nextPathLocation, nextPathFileDir)

    if 'deleted' in nextPath:
      differences['swap'].append(nextRow)

    for baseRow in baseImage:
      baseHash = baseRow[0]
      basePath = baseRow[1]

      # basePathFileDir = basePath.split('/')[-1]
      # lengthBaseDir = len(basePathFileDir)
      # basePathLocation = basePath[:(len(basePath)-lengthBaseDir)]
      # print(basePathLocation, basePathFileDir)
    
      if baseHash == nextHash and basePath == nextPath:
        # print('Same',baseRow, nextRow)
        differences['same'].append(nextRow)
  
      if baseHash != nextHash and basePath == nextPath:
        # print('Modified',baseRow, nextRow)
        basePaths.append(basePath)
        differences['modified'].append(nextRow)
  
  
    if nextRow not in baseImage and 'deleted' not in nextPath and nextRow[1] not in basePaths:
      print('New', nextRow)
      # TODO: Moved files are shown as new here - hash als changes :(
      differences['new'].append(nextRow)
      

  # for baseRow in baseImage:
  #   # rows = hashAndPath[1]
  #   # Same: nothing changed beteween 2 delta's
  #   # Deleted: not present in new image
  #   # Modified: something was modified - but location is the same
  #   # Moved: location of file changed - nothing else
  #   baseHash = baseRow[0]
  #   basePath = baseRow[1]
    
  #   for nextRow in nextImage:
  #     nextHash = nextRow[0]
  #     nextPath = nextRow[1]
      
  #     if baseHash == nextHash:
  #       if basePath == nextPath:
  #         differences['same'].append(nextRow)
  #       # else:
  #       #   # not correct
  #       #   differences['moved'] = nextRow
  #     elif basePath == nextPath:
  #       differences['modified'].append(nextRow)
  #     else:
  #       pass
  #     # print('Base-row: ', baseRow, 'Next-row: ', nextRow)

  # for nextRow in nextImage:   
  #   nextPath = nextRow[1]
    
  #   if 'deleted' in nextPath:
  #     differences['deleted'].append(nextRow)
    
  #   if nextRow not in baseImage and 'deleted' not in nextPath:
  #     differences['new'].append(nextRow)

  deltaImage['differences'] = differences
  return deltaImage


def getFilesDiffing(deltas, out: str):
  modified = deltas['differences']['modified']
  modifiedFilePaths = []
  
  for mod in modified:
    fileOrDir = mod[3].split('/')[0]
    
    if fileOrDir == 'd':
      print('Directory: ', mod)
    elif fileOrDir == 'r':
      modifiedFilePaths.append(mod)
      print('File: ', mod)
    else:
      print('Else: ', mod)
  
  
  imageNames = [deltas['delta'], deltas['next']]
  
  for name in imageNames:
    for mod in modifiedFilePaths:
      cmd = "icat ./images/{0}.img {1} > {2}/{0}-{1}.txt".format(name.replace('_','-'), mod[2], out)
      res = system(cmd)
      
      if res == 0:
        methods_logger.debug('Retrieving file succesfull!')
        
  
