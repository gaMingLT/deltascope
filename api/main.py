import os, sys
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from loger import custom_logger

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
 
from cli import binding

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
    """Upload image(s) in to the hardcoded directory - NOT IMPLEMENTED
    
    """
    return {"filenames": [file.filename for file in files]}


# List uploaded Images (name)
@app.get("/images/list")
async def list_images():
    """Returns a list of images that are present in the currently (hardcoded) images directory
    
    
    """
    custom_logger.debug('Retrieving uploaded images')
    imageNames = binding.list_uploaded_images()
    return {"images": imageNames}


# Initiate  delta'ing of images
# - Add options of what should be done
@app.post("/delta")
async def initiate_delta_images(deltaScopeOptions: DeltaScopeOptions):
    """Initiate's the delta between 2 specified images
    
    Args:
        deltaScopeOptions (DeltaScopeOptions): contains images field wich consists of a list of strings which are the names of the images that need to be compaired
        
    Returns:
        returns the path & image names which are compared.
    """
    custom_logger.debug('Initiating delta of images: {0}'.format(deltaScopeOptions.images))
    res = binding.initiate_delta_images(deltaScopeOptions.images)
    return res


# Get Events + Delta events
@app.post("/events/")
async def get_events(deltaScopeEvents: DeltaScopeEvents):
    """Retrieve the events (mac timeline output) from compared images

    Args:
        deltaScopeEvents (DeltaScopeEvents): consists of list of the names of the images that where compared 
        & name of the directory where everything was outputted to

    Returns:
        _type_: _description_
    """
    custom_logger.debug('Retrieving events from latest comparison: {0}'.format(deltaScopeEvents.directoryName))
    events = binding.get_events(imageNames=deltaScopeEvents.images,directoryPath=deltaScopeEvents.directoryName)
    return {"events": events}


# Get files which were modified - get content on web
@app.post("/diff/files")
async def diffing_files(deltaScopeDiffFiles: DeltaScopeDiffFiles):
    """Retrieves the files which where modified between the 2 images
    
    Args:

    
    Returns:
        dictionary: keys consisting of the name of the file with value being the content encoded in base64
    """
    custom_logger.debug('Retrieving files from latest comparison: {0}'.format(deltaScopeDiffFiles.directoryName))
    files = binding.get_different_files(deltaScopeDiffFiles.directoryName)
    return {"diff_files": files}
