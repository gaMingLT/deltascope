import hashlib, datetime, logging, codecs
from os import mkdir, path, system

from cli.loger import CustomFormatter
from cli.db import *

# from loger import CustomFormatter
# from db import *

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
  methods_logger.debug('[METHODS] - Image info: {0}'.format(path))
  
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
  methods_logger.debug('[METHODS] - Preparing filesystem: Images:  {0} - Out: {1}'.format(paths,out))
  
  # Create output directory for files used in differentiating
  if not path.exists(out):
    mkdir('{0}'.format(out))
  
  dateTime = str(datetime.datetime.now())
  pathOutPutDir = "{0}/deltascope-{1}".format(out,dateTime.replace(' ', '_').replace('.','-'))
  
  mkdir(pathOutPutDir)
  
  return pathOutPutDir


def executeFls(path: str, out: str) -> str:
  methods_logger.info('[METHODS] - Retrieving files from image using FLS')
  
  bodyFilePath = "{0}/{1}.txt".format(out, path.split('/')[-1].split('.')[0])
  cmd = "{0} {1} {2} {3} > {4}".format("fls", "-r -h -m",'/', path ,bodyFilePath)
  res = system(cmd)
  
  if res == 0:
    methods_logger.info('[METHODS] - FLS Execution - Succes!')
    
  return bodyFilePath


def parseBodyFile(path: str, out: str) -> list:
  methods_logger.info('[METHODS] - Parsing body file')
  
  # f = open(path, "r")
  f = codecs.open(path, encoding='utf-8', errors='ignore')
  
  data = []
  # counter = 0
  for line in f.readlines():
    # print('Counter: ', counter, line)
    # MD5,name,inode,mode_as_string,UID,GID,size,atime,mtime,ctime,crtime
    md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime = line.split('|')
    data.append((md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime))
    # counter = counter + 1
  
  return data

def createMacTimeLineFile(name, out: str):
  methods_logger.info('[METHODS] - Creating MAC Timeline from FLS Body file')
  
  if not path.exists('{0}/{1}'.format(out,'timelines')):
    mkdir('{0}/{1}'.format(out,'timelines'))

  cmd = "mactime -b {1}/{0}.txt > {1}/{2}/tl.{0}.txt".format(name.replace('_','-'), out, 'timelines')
  res = system(cmd)
  
  if res == 0:
    methods_logger.info('[METHODS] - Completed creating mactime line file for {0}'.format(name))


def parseMacTimeLineFile(name, out: str):
  methods_logger.info('[METHODS] - Parsing MAC Timeline file')
  path = "{1}/{2}/tl.{0}-filtered.txt".format(name.replace('_','-'), out, 'timelines')
  
  f = codecs.open(path, encoding='utf-8', errors='ignore')
  
  data = []
  for line in f.readlines():
    # TODO: Improve this!
    date, size, activity, perm, uid, guid, inode, file_name = line[:24], line[24:34], line[34:39], line[39:52], line[52:54], line[61:63], line[71:78], line[78:]
    values = (date.strip(), size.strip(), activity.strip()  ,perm.strip(), uid.strip(), guid.strip(), inode.strip(), file_name.strip())
    data.append(values)
    
  print('Value mac timeline: ', data[0])

  return data


def filterMacTimeline(name, out: str):
  methods_logger.info('[METHODS] - Filtering MAC Timeline file')
  
  path = "{1}/{2}/tl.{0}.txt".format(name.replace('_','-'), out, 'timelines')
  
  cmd = "grep -E '/etc/*' {0} | grep -v '/usr/share' > {2}/{3}/tl.{1}-filtered.txt".format(path, name.replace('_','-'), out, 'timelines')
  res = system(cmd)
  
  if res == 0:
    methods_logger.info('[METHODS] - Filtering MAC Timeline file complete: {0}'.format(name))

def compareHashAndPath(data, con):
  methods_logger.info('[METHODS] - Comparing hash and path')
  hashAndPathImages = []
  
  for img in data:
    hashPathMode = []
    for row in img[1]:
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
      # print('New', nextRow)
      # TODO: Moved files are shown as new here - hash als changes :(
      differences['new'].append(nextRow)
  
  deltaImage['differences'] = differences
  return deltaImage


def retrieveFilesFromImages(deltas, out: str):
  methods_logger.info('[METHODS] - Retrieving ``modified`` files from image')
  modified = deltas['differences']['modified']
  modifiedFilePaths = []
  
  print('Modified: ', modified)
  
  for mod in modified:
    fileOrDir = mod[3].split('/')[0]
    
    if fileOrDir == 'd':
      # print('Directory: ', mod)
      pass
    elif fileOrDir == 'r':
      modifiedFilePaths.append(mod)
      # print('File: ', mod)
    else:
      # print('Else: ', mod)
      pass
  
  
  imageNames = [deltas['delta'], deltas['next']]
  
  if not path.exists('{0}/{1}'.format(out,'icat')):
    mkdir('{0}/{1}'.format(out,'icat'))
  
  print(modifiedFilePaths)
  
  differentPathNames = {}
  
  for name in imageNames:
    for mod in modifiedFilePaths:
      pathName = mod[1].split('/')[-1].split('.')[0]
      fileName = mod[1].split('/')[-1]
      if fileName in differentPathNames:
        differentPathNames[fileName].append("{0}-{2}-{1}.txt".format(name.replace('_','-'), mod[2] ,pathName))
      else:
        differentPathNames[fileName] = ["{0}-{2}-{1}.txt".format(name.replace('_','-'), mod[2] ,pathName)]
      
      # cmd = "icat /home/milan/dev/python-tool/deltascope-1/cli/images/{0}.img {1} > {2}/icat/{0}-{3}-{1}.txt".format(name.replace('_','-'), mod[2], out, pathName)
      srcPath = "/mnt/img-store/scn-1/images"
      cmd = "icat {4}/{0}.img {1} > {2}/icat/{0}-{3}-{1}.txt".format(name.replace('_','-'), mod[2], out, pathName, srcPath)
      
      
      res = system(cmd)
      
      if res == 0:
        methods_logger.debug('[METHODS] - Retrieving file succesfull!')
  
  if not path.exists('{0}/{1}'.format(out,'diff')):
    mkdir('{0}/{1}'.format(out,'diff'))

  for key in differentPathNames.keys():
    paths = differentPathNames[key]
    diffFileName = "{0}.txt".format(key.split('.')[0])
    cmd = "diff -u {0}/icat/{1} {0}/icat/{2} > {0}/diff/{3}".format(out, paths[0], paths[1], diffFileName)
    res = system(cmd)
    if res == 0:
      methods_logger.debug('[METHODS] - Diffing of files succesfull!')

        

def getEventsImages(tablesNames, con):
  methods_logger.info('[METHODS] - Retrieving events from images')
  events = { 'base': [], 'next': [], 'delta': [] }
  
  for index, tableName in enumerate(tablesNames):
    eventsData = getImageEventsValues(name=tableName, con=con)
    if index == 0:
      events['base'] = eventsData
    else:
      events['next'] = eventsData
  
  eventsDelta = getImageEventsDelta(tablesNames, con=con)
  print('Delta', eventsDelta)
  
  events['delta'] = eventsDelta
  print('Events images: ', events)
  
  return events
