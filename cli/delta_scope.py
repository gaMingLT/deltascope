from cli.methods import * 
from cli.db import * 
from cli.loger import CustomFormatter

# from methods import * 
# from db import * 
# from loger import CustomFormatter


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""
    green = '\x1b[0;32m'
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.green + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def create_main_logger():
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

main_logger = create_main_logger()

def delta_images_cli(images: list[str]):
  main_logger.info('Main program')
  
  outPath = prepareFilesystem(images, out='./output')
  dbCon = database_con(outPath)
  tablesNames = []
  
  for path in images:
    imageInfo(path=path)
    bodyFilePath = executeFls(path=path, out=outPath)
    
    name = (bodyFilePath.split('/')[-1].split('.')[0]).replace('-','_')
    tablesNames.append(name)
    
    createImageFilesTable(name=name, con=dbCon)
    fileData = parseBodyFile(path=bodyFilePath, out=outPath)
    inputValuesImageFilesTable(name=name, values=fileData, con=dbCon)
    
    # Timeline creation
    createImageTimelineTable(name,con=dbCon)
  
    # Create timeline files
    createMacTimeLineFile(name=name, out=outPath)
    
    # Parse timelines file
    timelineData = parseMacTimeLineFile(name=name, out=outPath)
    
    # Add data to database file
    inputValuesImageTimelineTable(name=name, values=timelineData, con=dbCon)

  dataImages = []
  
  for tableName in tablesNames:
    fileData = getImageFilesValues(name=tableName, con=dbCon)
    dataImages.append((tableName,fileData))
  
  fileDelta  = compareHashAndPath(data=dataImages,con=dbCon)
  retrieveFilesFromImages(deltas=fileDelta, out=outPath)
  
  
  events = { 'base': [], 'next': [], 'delta': [] }
  
  for index, tableName in enumerate(tablesNames):
    eventsData = getImageEventsValues(name=tableName, con=dbCon)
    if index == 0:
      events['base'] = eventsData
    else:
      events['next'] = eventsData
  
  # createTimelineDeltaTable(names=tablesNames, con=dbCon)
  eventsDelta = getImageEventsDelta(tablesNames, con=dbCon)
  # print('Delta', eventsDelta)
  
  events['delta'] = eventsDelta
  # print('Events images: ', events)
 
  # print('Outpath: ', outPath)
 
  return outPath


def delta_image_web(paths: list[str], images: list[str]):
  main_logger.info('Main program')
  
  outPath = prepareFilesystem(paths, out='./output')
  dbCon = database_con(outPath)
  tablesNames = []
  
  for path in paths:
    imageInfo(path=path)
    bodyFilePath = executeFls(path=path, out=outPath)
    
    name = (bodyFilePath.split('/')[-1].split('.')[0]).replace('-','_')
    tablesNames.append(name)
    
    createImageFilesTable(name=name, con=dbCon)
    fileData = parseBodyFile(path=bodyFilePath, out=outPath)
    inputValuesImageFilesTable(name=name, values=fileData, con=dbCon)
    
    # Timeline creation
    createImageTimelineTable(name,con=dbCon)
  
    # Create timeline files
    createMacTimeLineFile(name=name, out=outPath)
    
    # Parse timelines file
    timelineData = parseMacTimeLineFile(name=name, out=outPath)
    
    # Add data to database file
    inputValuesImageTimelineTable(name=name, values=timelineData, con=dbCon)

  # Image Differences
  dataImages = []
  for tableName in tablesNames:
    fileData = getImageFilesValues(name=tableName, con=dbCon)
    dataImages.append((tableName,fileData))
  
  fileDelta  = compareHashAndPath(data=dataImages,con=dbCon)
  retrieveFilesFromImages(deltas=fileDelta, out=outPath)
  
  return { 'images': images, 'directoryName': outPath }


def getEventsImages(tablesNames: list[str], directoryPath: str):
  dbCon = database_con(path=directoryPath)
  newNames = []
  for name in tablesNames:
    newNames.append(name.replace('.img','').replace('-','_'))
  
  baseEvents =  getImageEventsValues(newNames[0],dbCon)
  nextEvents = getImageEventsValues(newNames[1], dbCon)
  deltaEvents = getImageEventsDelta(newNames, dbCon)
  
  events = { 'delta': deltaEvents, 'base': baseEvents, 'next': nextEvents }
  
  return events


def getDifferentFiles(tablesNames: list[str], directoryPath: str):
  pass
