from cli.methods import * 
from cli.db.conn import database_con
from cli.db.tables import create_timeline_image_table_2, create_files_table
from cli.db.events import input_values_events_2, get_events_image_values_neariest_date, get_events_image_values_neariest_date
from cli.db.files import input_values_files, get_files_values_path
from cli.db.delta import get_events_deltas

from cli.loger import main_logger

from multiprocessing import Pool
from functools import partial
import time, json


def delta_images_cli(images: list[str]):
  main_logger.info('Initiating Delta images trough CLI')
  
  outPath = prepareFilesystem(images, out='./output')
  dbCon = database_con(outPath)
  tablesNames = []
  
  for path in images:
    imageInfo(path=path)
    bodyFilePath = executeFls(path=path, out=outPath)
    
    name = (bodyFilePath.split('/')[-1].split('.')[0]).replace('-','_')
    tablesNames.append(name)
    
    create_files_table(name=name, con=dbCon)
    fileData = parseBodyFile(path=bodyFilePath, out=outPath)
    input_values_files(name=name, values=fileData, con=dbCon)
    
    # Timeline creation
    create_timeline_image_table_2(name,con=dbCon)
  
    # Create timeline files
    createMacTimeLineFile(name=name, out=outPath)
    
    # Parse timelines file
    timelineData = parseMacTimeLineFile(name=name, out=outPath)
    
    # Add data to database file
    input_values_files(name=name, values=timelineData, con=dbCon)

  # dataImages = []
  
  # for tableName in tablesNames:
  #   fileData = getImageFilesValues(name=tableName, con=dbCon)
  #   dataImages.append((tableName,fileData))
  
  # fileDelta  = compareHashAndPath(data=dataImages,con=dbCon)
  # retrieveFilesFromImages(deltas=fileDelta, out=outPath)
  
  
  events = { 'base': [], 'next': [], 'delta': [] }
  
  for index, tableName in enumerate(tablesNames):
    eventsData = get_events_images(name=tableName, con=dbCon)
    if index == 0:
      events['base'] = eventsData
    else:
      events['next'] = eventsData
  
  # createTimelineDeltaTable(names=tablesNames, con=dbCon)
  eventsDelta = get_events_deltas(tablesNames, con=dbCon)
  # print('Delta', eventsDelta)
  
  events['delta'] = eventsDelta
  # print('Events images: ', events)
 
  # print('Outpath: ', outPath)
 
  return outPath


def retrieve_info_image(outPath, iterable: str):
  path = iterable
  
  dbCon = database_con(outPath)
  imageInfo(path=path)
  bodyFilePath = executeFls(path=path, out=outPath)
  name = (bodyFilePath.split('/')[-1].split('.')[0]).replace('-','_')


  create_files_table(name=name, con=dbCon)
  fileData = parseBodyFile(path=bodyFilePath, out=outPath)
  input_values_files(name=name, values=fileData, con=dbCon)
  
  # Timeline creation
  create_timeline_image_table_2(name=name, con=dbCon)

  # Create timeline files
  createMacTimeLineFile(name=name, out=outPath)
  
  # Filtering mac timeline file:
  filterMacTimeline(name=name, out=outPath)
  
  # Parse timelines file
  timelineData = parseMacTimeLineFile(name=name, out=outPath)
  
  # Add data to database file
  input_values_events_2(name=name, values=timelineData, con=dbCon)
  
  dbCon.close()
  
  return name
  
  
def delta_image_web(paths: list[str], images: list[str]):
  main_logger.info('Initiating Delta images trough WEB')
  start_time = time.time()
  
  outPath = prepareFilesystem(paths, out='./output')
  tablesNames = []
  
  with Pool(2) as p:
    res = p.map(partial(retrieve_info_image, outPath), paths)
    print('Result: ', res)
  
  tablesNames = res
  print('Finished preprocessing images')

  print('Execution time', time.time() - start_time, ' Seconds')


  # Image Differences
  dbCon = database_con(outPath)
  dataImages = []
  for tableName in tablesNames:
    fileData = get_files_values_path(name=tableName, path='/etc', con=dbCon)
    dataImages.append((tableName, fileData))
  
  fileDelta  = compareHashAndPath(data=dataImages,con=dbCon)
  retrieveFilesFromImages(deltas=fileDelta, out=outPath)
  
  dbCon.close()
  
  
  return { 'images': images, 'directoryName': outPath }


def get_events_images(tablesNames: list[str], directoryPath: str):
  methods_logger.info('[DELTASCOPE] - Retrieving events from images')
  dbCon = database_con(path=directoryPath)
  baseImageTableName = ()
  nextImageTableName = ()
  
  newNames = []
  for name in tablesNames:
    newName = name.replace('.img','').replace('-','_')
    newNames.append(newName)
    # count = get_events_image_values_year_count(name=newName, con=dbCon)[0][0]
    date = get_events_image_values_neariest_date(name=newName, con=dbCon)[0][0]
    
    if len(baseImageTableName) == 0:
      baseImageTableName = (date, newName)
    elif date > baseImageTableName[0]:
      nextImageTableName = (date, newName)
    elif date < baseImageTableName[0]:
      nextImageTableName = baseImageTableName
      baseImageTableName = (date, newName)
    else:
      pass
  
  baseEvents = json.loads(get_events_deltas(baseImageTableName[1], 2023, dbCon)[0][0])[:100]
  nextEvents = json.loads(get_events_deltas(nextImageTableName[1], 2023, dbCon)[0][0])[:100]
  deltaEvents = json.loads(get_events_deltas(base=baseImageTableName[1], next=nextImageTableName[1], year=2023 ,con=dbCon)[0][0])
  
  events = { 'delta': deltaEvents, 'base': baseEvents, 'next': nextEvents }
  
  return events
