from fastapi import File
from cli.delta_scope import delta_image_web, getEventsImages

import os

# TODO: Scrappe for now - while require streaming
def place_uploaded_images(files: list[bytes], outPath: str):
  
  for file in files:
    with open("", "wb") as file:
      file.write(file)
  
  pass


def list_uploaded_images():
  imageFileNames = []
  for file in os.listdir('/home/milan/dev/python-tool/deltascope-1/cli/images/'):
      imageFileNames.append(file)
  
  # main_logger.debug('Listing uploaded images!')
  
  return  imageFileNames


def initiate_delta_images(images: list[str]) -> str:
  paths = []
  for image in images:
    paths.append("/home/milan/dev/python-tool/deltascope-1/cli/images/{0}".format(image))
  
  res = delta_image_web(paths, images)
  
  return res


def get_events(imageNames: list[str], directoryPath: str):
  # directoryPath = "/home/milan/dev/python-tool/deltascope-1/web/" + directoryPath.replace('./','')
  events = getEventsImages(tablesNames=imageNames, directoryPath=directoryPath)
  
  return events
