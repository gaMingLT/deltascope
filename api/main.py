from typing import Union
import os, sys, logging
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.logger import logger as fastapi_logger
from fastapi.middleware.cors import CORSMiddleware
from logging.handlers import RotatingFileHandler
from loger import custom_logger

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
 
from cli import binding
# from api.cli import binding

class DeltaScopeDiffFiles(BaseModel):
    directoryName: str

class DeltaScopeOptions(BaseModel):
    images: list[str]

class DeltaScopeEvents(BaseModel):
    images: list[str]
    directoryName: str

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
  return {"Hello": "World"}


# Upload images
@app.post("/images/upload")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


# List uploaded Images (name)
@app.get("/images/list")
async def list_images():
  custom_logger.debug('Retrieving uploaded images')
  imageNames = binding.list_uploaded_images()
  return {"images": imageNames}


# Initiate  delta'ing of images
# - Add options of what should be done
@app.post("/delta")
async def initiate_delta_images(deltaScopeOptions: DeltaScopeOptions):
    custom_logger.debug('Initiating delta of images: {0}'.format(deltaScopeOptions.images))
    res = binding.initiate_delta_images(deltaScopeOptions.images)
    return res


# Get Events + Delta events
@app.post("/events/")
async def get_events(deltaScopeEvents: DeltaScopeEvents):
    custom_logger.debug('Retrieving events from latest comparison: {0}'.format(deltaScopeEvents.directoryName))
    events = binding.get_events(imageNames=deltaScopeEvents.images,directoryPath=deltaScopeEvents.directoryName)
    return {"events": events}


# Get modified - changed - new files & dir
# @app.get("/objects/{directoryName}")
# async def get_objects(directoryName: str):
#     custom_logger.debug('Retrieving objects from latest comparison: {0}'.format(directoryName))
#     return {"objects": []}


# Get files which were modified - get content on web
@app.post("/diff/files")
async def diffing_files(deltaScopeDiffFiles: DeltaScopeDiffFiles):
    custom_logger.debug('Retrieving files from latest comparison: {0}'.format(deltaScopeDiffFiles.directoryName))
    files = binding.get_different_files(deltaScopeDiffFiles.directoryName)
    return {"diff_files": files}
