import sys
import hashlib
from os import mkdir, path, system
import datetime
import pprint
import json

def imageInfo(path: str):
  # print('Image info path: ', path)
  
  # BUF_SIZE is totally arbitrary, change for your app!
  BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
  
  md5 = hashlib.md5()
  # sha1 = hashlib.sha1()

  with open(path, 'rb') as f:
    while True:
        data = f.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)
        # sha1.update(data)

  print("MD5: {0}".format(md5.hexdigest()))
  # print("SHA1: {0}".format(sha1.hexdigest()))
  

def prepareFilesystem(paths, out: str) -> str:
  
  # Create output directory for files used in differentiating
  if not path.exists(out):
    mkdir('{0}'.format(out))
  
  dateTime = str(datetime.datetime.now())
  pathOutPutDir = "{0}/deltascope-{1}".format(out,dateTime.replace(' ', '_').replace('.','-'))
  
  mkdir(pathOutPutDir)
  
  return pathOutPutDir


def executeFls(path: str, out: str) -> str:
  print('Path: ', path, 'Out: ', out)
  
  bodyFilePath = "{0}/{1}.txt".format(out, path.split('/')[-1].split('.')[0])
  cmd = "{0} {1} {2} {3} > {4}".format("fls", "-r -h -m",'/', path ,bodyFilePath)
  res = system(cmd)
  
  if res == 0:
    print('FLS Execution - Succes!')
    
  return bodyFilePath

def parseBodyFile(path: str, out: str) -> list:
  # print('Parsing body file - path: {0} - out: {1}'.format(path, out))
  
  f = open(path, "r")
  data = []
  
  for line in f.readlines():
    # MD5,name,inode,mode_as_string,UID,GID,size,atime,mtime,ctime,crtime
    md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime = line.split('|')
    # print(md5)
    data.append((md5,name,inode,mode_as_string,uid,gid,size,atime,mtime,ctime,crtime))
  
  return data


def compareHashAndPath(data, con):
  hashAndPathImages = []
  
  for img in data:
    # print('Image: ', img[0])
    hashAndPath = []
    for row in img[1]:
      # print('Row: ', row)
      hashAndPath.append((row[0], row[1]))
    hashAndPathImages.append((img[0], hashAndPath))
    
  # hashAndPathImagesPretty = json.dumps(hashAndPathImages, indent=4)
  # print(hashAndPathImagesPretty)

  
  deltas = []
  deltaImage = { 'delta': '', 'next': '', 'differences': {} }
  differences = { 'same': [] ,'deleted': [], 'modified': [], 'moved': [] , 'new': [] }
  
  for baseRow in hashAndPathImages[0][1]:
    # rows = hashAndPath[1]
    # Same: nothing changed beteween 2 delta's
    # Deleted: not present in new image
    # Modified: something was modified - but location is the same
    # Moved: location of file changed - nothing else
    baseHash = baseRow[0]
    basePath = baseRow[1]
    
    for nextRow in hashAndPathImages[1][1]:
      nextHash = nextRow[0]
      nextPath = nextRow[1]
      
      if baseHash == nextHash:
        if basePath == nextPath:
          differences['same'].append(nextRow)
        else:
          # not correct
          differences['moved'] = nextRow
      elif basePath == nextPath:
        differences['modified'].append(nextRow)
      else:
        pass
      print('Base-row: ', baseRow, 'Next-row: ', nextRow)

  for nextRow in hashAndPathImages[1][1]:   
    if nextRow not in hashAndPathImages[0][1]:
      differences['new'].append(nextRow)


  pretty = json.dumps(differences, indent=4)
  print('Pretty', pretty)
