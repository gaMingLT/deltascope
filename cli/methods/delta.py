from cli.loger import main_logger

def compare_hash_path(data, con):
  main_logger.info('[METHODS] - Comparing hash and path')
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

    if 'deleted' in nextPath:
      differences['swap'].append(nextRow)

    for baseRow in baseImage:
      baseHash = baseRow[0]
      basePath = baseRow[1]
    
      if baseHash == nextHash and basePath == nextPath:
        differences['same'].append(nextRow)
  
      if baseHash != nextHash and basePath == nextPath:
        basePaths.append(basePath)
        differences['modified'].append(nextRow)
  
  
    if nextRow not in baseImage and 'deleted' not in nextPath and nextRow[1] not in basePaths:
      # TODO: Moved files are shown as new here - hash als changes :(
      differences['new'].append(nextRow)
  
  deltaImage['differences'] = differences
  return deltaImage
