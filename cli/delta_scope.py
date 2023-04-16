from cli.methods import * 
from cli.db.conn import database_con
from cli.db.tables import create_events_table, create_files_table
from cli.db.events import input_values_events, get_events_image_values_neariest_date, get_events_json
from cli.db.files import input_values_files, get_files_values_path
from cli.db.delta import get_events_delta

from cli.methods.utils import image_info, prepare_filesystem
from cli.methods.fls import execute_fls, parse_fls_body_file
from cli.methods.mactime import execute_mactime, parse_mactime_file, filter_mactime_file
from cli.methods.files import retrieve_files_from_image, compare_hash_path

from cli.loger import main_logger

from multiprocessing import Pool
from functools import partial
import time, json


# Currently does not work because of module cli not found when executing main.py from inside the cli directory
def delta_images_cli(images: list[str]):
  main_logger.info('Initiating Delta images trough CLI')
  
  start_time = time.time()
  
  outPath = prepare_filesystem(images, out='./output')
  tablesNames = []
  
  with Pool(2) as p:
    res = p.map(partial(retrieve_info_image, outPath), images)
  
  tablesNames = res
  
  main_logger.debug('Finished preprocessing images')
  main_logger.debug('Execution time', time.time() - start_time, ' Seconds')


  # Image Differences
  dbCon = database_con(outPath)
  dataImages = []
  for tableName in tablesNames:
    fileData = get_files_values_path(name=tableName, path='/etc', con=dbCon)
    dataImages.append((tableName, fileData))
  
  fileDelta  = compare_hash_path(data=dataImages,con=dbCon)
  retrieve_files_from_image(deltas=fileDelta, out=outPath)
  
  dbCon.close()
  
  print("Images parsed: ", images)
  print("Files written to directory: ", outPath)


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
  create_events_table(name=name, con=dbCon)

  # Create timeline files
  execute_mactime(name=name, out=outPath)
  
  # Filtering mac timeline file:
  filter_mactime_file(name=name, out=outPath)
  
  # Parse timelines file
  timelineData = parse_mactime_file(name=name, out=outPath)
  
  # Add data to database file
  input_values_events(name=name, values=timelineData, con=dbCon)
  
  dbCon.close()
 
    
  return name
  
  
def delta_image_web(paths: list[str], images: list[str]):
  main_logger.info('Initiating Delta images trough WEB')
  start_time = time.time()
  
  outPath = prepare_filesystem(paths, out='./output')
  tablesNames = []
  
  with Pool(2) as p:
    res = p.map(partial(retrieve_info_image, outPath), paths)
  
  tablesNames = res
  
  main_logger.debug('Finished preprocessing images')
  print('Execution time', {0}, ' Seconds',  time.time() - start_time)


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
