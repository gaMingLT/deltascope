from fastapi import File
import base64, os
from cli.delta_scope import delta_image_web, getEventsImages


# TODO: Scrap for now - while require streaming
def place_uploaded_images(files: list[bytes], outPath: str):
  
  for file in files:
    with open("", "wb") as file:
      file.write(file)
  
  pass


def list_uploaded_images():
  
  imageFileNames = []
  # path = '/home/milan/dev/python-tool/deltascope-1/cli/images/'
  path = '/mnt/img-store/scn-1/images'
  for file in os.listdir(path):
      imageFileNames.append(file)

  return  imageFileNames


def initiate_delta_images(images: list[str]) -> str:
    # path = '/home/milan/dev/python-tool/deltascope-1/cli/images/'
  path = '/mnt/img-store/scn-1/images/'
  paths = []
  for image in images:
    paths.append("{0}{1}".format(path,image))
  
  res = delta_image_web(paths, images)
  
  return res


def get_events(imageNames: list[str], directoryPath: str):
  events = getEventsImages(tablesNames=imageNames, directoryPath=directoryPath)
  
  return events


def get_different_files(directoryPath: str):
  imageFileNames = []
  for file in os.listdir('{0}/diff'.format(directoryPath)):
      imageFileNames.append(file)
  
  diffFiles = {}
  
  for filePath in imageFileNames:
    f = open("{0}/diff/{1}".format(directoryPath, filePath),"rb")
    fileContent = f.read()
    fileContentBase = base64.b64encode(fileContent)
    diffFiles[filePath] = fileContentBase
  
  return diffFiles
