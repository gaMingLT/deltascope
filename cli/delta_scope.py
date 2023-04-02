from cli.methods import * 
from cli.db.conn import database_con, database_con_loaddb
from cli.db.tables import create_timeline_image_table_2, create_files_table, create_loaddb_events_table
from cli.db.events import input_values_events_2, get_events_image_values_neariest_date, get_events_image_values_neariest_date
from cli.db.files import input_values_files, get_files_values_path
from cli.db.delta import get_events_json, get_events_delta
from cli.db.loaddb import get_events_loaddb, input_values_contentdb

from cli.methods.utils import image_info, prepare_filesystem
from cli.methods.fls import execute_fls, parse_fls_body_file
from cli.methods.mactime import execute_mactime, parse_mactime_file, filter_mactime_file
from cli.methods.files import retrieve_files_from_image
from cli.methods.delta import compare_hash_path
from cli.methods.loaddb import load_database_from_image

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
    bodyFilePath = execute_fls(imagePath=path, out=outPath)
    
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
  image_info(path=path)
  bodyFilePath = execute_fls(imagePath=path, out=outPath)
  name = (bodyFilePath.split('/')[-1].split('.')[0]).replace('-','_')


  create_files_table(name=name, con=dbCon)
  fileData = parse_fls_body_file(filePath=bodyFilePath, out=outPath)
  input_values_files(name=name, values=fileData, con=dbCon)
  
  # Timeline creation
  create_timeline_image_table_2(name=name, con=dbCon)

  # Create timeline files
  execute_mactime(name=name, out=outPath)
  
  # Filtering mac timeline file:
  filter_mactime_file(name=name, out=outPath)
  
  # Parse timelines file
  timelineData = parse_mactime_file(name=name, out=outPath)
  
  # Add data to database file
  input_values_events_2(name=name, values=timelineData, con=dbCon)
  
  # dbCon.close()
  
  
  # Events 2.0? -
  # load_database_from_image(imagePath=path, out=outPath)
  # dbConLoaded = database_con_loaddb(filePath=path, outPath=outPath)
  
  # create_loaddb_events_table(name=name, con=dbCon)
  
  # eventsLoadeddb = get_events_loaddb(name='', con=dbConLoaded)
  # input_values_contentdb(name=name, values=eventsLoadeddb, con=dbCon)

  # dbCon.close
    
  return name
  
  
def delta_image_web(paths: list[str], images: list[str]):
  main_logger.info('Initiating Delta images trough WEB')
  start_time = time.time()
  
  outPath = prepare_filesystem(paths, out='./output')
  tablesNames = []
  
  with Pool(2) as p:
    res = p.map(partial(retrieve_info_image, outPath), paths)
  
  tablesNames = res
  print('Finished preprocessing images')

  print('Execution time', time.time() - start_time, ' Seconds')


  # Image Differences
  dbCon = database_con(outPath)
  dataImages = []
  for tableName in tablesNames:
    fileData = get_files_values_path(name=tableName, path='/etc', con=dbCon)
    dataImages.append((tableName, fileData))
  
  fileDelta  = compare_hash_path(data=dataImages,con=dbCon)
  retrieve_files_from_image(deltas=fileDelta, out=outPath)
  
  dbCon.close()
  
  
  return { 'images': images, 'directoryName': outPath }


def get_events_images(tablesNames: list[str], directoryPath: str):
  main_logger.info('[DELTASCOPE] - Retrieving events from images')
  dbCon = database_con(path=directoryPath)
  baseImageTableName = ()
  nextImageTableName = ()
  
  newNames = []
  for name in tablesNames:
    newName = name.replace('.img','').replace('-','_')
    newNames.append(newName)
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
  
  baseEvents = json.loads(get_events_json(baseImageTableName[1], 2023, dbCon)[0][0])[:100]
  nextEvents = json.loads(get_events_json(nextImageTableName[1], 2023, dbCon)[0][0])[:100]
  deltaEvents = json.loads(get_events_delta(base=baseImageTableName[1], next=nextImageTableName[1], year=2023 ,con=dbCon)[0][0])
  
  events = { 'delta': deltaEvents, 'base': baseEvents, 'next': nextEvents }
  
  return events
