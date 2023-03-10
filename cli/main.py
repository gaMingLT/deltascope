import argparse
from methods import executeFls, imageInfo, prepareFilesystem, parseBodyFile, compareHashAndPath
from db import database_con, createTable, inputValues, getTableData

def main():
  args = parseargs()
  
  outPath = prepareFilesystem(args.images, out='./output')
  
  dbCon = database_con(outPath)
  
  tablesNames = []
  
  for path in args.images:
    # print('Path: ', path)
    imageInfo(path=path)
    bodyFilePath = executeFls(path=path, out=outPath)
    name = (bodyFilePath.split('/')[-1].split('.')[0]).replace('-','_')
    tablesNames.append(name)
    createTable(name=name, con=dbCon)
    data = parseBodyFile(path=bodyFilePath, out=outPath)
    inputValues(name=name, values=data, con=dbCon)
  
  dataImages = []
  
  # print('Tablesnames: ', tablesNames)
  
  for tableName in tablesNames:
    data = getTableData(name=tableName, con=dbCon)
    dataImages.append((tableName,data))
  
  compareHashAndPath(data=dataImages,con=dbCon)
  
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
