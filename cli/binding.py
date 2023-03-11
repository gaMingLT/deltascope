from fastapi import File
import glob, os

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
  
  print(imageFileNames)
  
  return  imageFileNames


def initiate_delta_images():
  
  
  pass


def get_events():
  pass
