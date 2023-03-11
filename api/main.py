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

class DeltaScopeOptions(BaseModel):
    name: str


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
@app.post("/uploadImages/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


# List uploaded Images (name)
@app.get("/images/")
async def list_images():
  custom_logger.debug('Retrieving uploaded images')
  imageNames = binding.list_uploaded_images()
  return {"images": imageNames}


# Initiate  delta'ing of images
# - Add options of what should be done
@app.post("/delta/")
async def initiate_delta_images(deltaScopeOptions: DeltaScopeOptions):
    return { 'options': deltaScopeOptions }


# Get Events + Delta events
@app.get("/events")
async def get_events():
    return {"events": []}


# Get modified - changed - new files & dir
@app.get("/objects")
async def get_objects():
    return {"objects": []}


# Get files which were modified - get content on web
@app.get("/diff/files")
async def diffing_files():
    return {"diff_files": []}
