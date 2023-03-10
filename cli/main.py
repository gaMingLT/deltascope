import argparse
import logging, json
from methods import executeFls, imageInfo, prepareFilesystem, parseBodyFile, compareHashAndPath, getFilesDiffing
from db import database_con, createTable, inputValues, getTableData
from loger import CustomFormatter

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


def main():
  main_logger.info('Main program')
  
  args = parseargs()
  outPath = prepareFilesystem(args.images, out='./output')
  dbCon = database_con(outPath)
  tablesNames = []
  
  for path in args.images:
    imageInfo(path=path)
    bodyFilePath = executeFls(path=path, out=outPath)
    name = (bodyFilePath.split('/')[-1].split('.')[0]).replace('-','_')
    tablesNames.append(name)
    createTable(name=name, con=dbCon)
    data = parseBodyFile(path=bodyFilePath, out=outPath)
    inputValues(name=name, values=data, con=dbCon)
  
  dataImages = []
  
  for tableName in tablesNames:
    data = getTableData(name=tableName, con=dbCon)
    dataImages.append((tableName,data))
  
  delta  = compareHashAndPath(data=dataImages,con=dbCon)
  
  prettyDelta = json.dumps(delta, indent=4)
  print(prettyDelta)
  
  getFilesDiffing(deltas=delta, out=outPath)
  
  pass


def parseargs():
  parser = argparse.ArgumentParser(
                    prog='Delta Scope',
                    description='What the program does',
                    epilog='Text at the bottom of help')
  
  parser.add_argument('images', metavar='/path', type=str, nargs='+',
                    help='image paths')
  
  args = parser.parse_args()
  # print('Imagse path: ', args.images)
  
  return args
  

if __name__ == "__main__":
  main()
