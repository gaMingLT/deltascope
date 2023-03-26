from cli.loger import main_logger
from os import mkdir, path, system

def retrieve_files_from_image(deltas, out: str):
  main_logger.info('[METHODS] - Retrieving ``modified`` files from image')
  print('New files: ', deltas['differences']['new'])
  modified = deltas['differences']['modified']
  modifiedFilePaths = []
  
  print('Modified: ', modified)
  
  for mod in modified:
    fileOrDir = mod[3].split('/')[0]
    
    if fileOrDir == 'd':
      pass
    elif fileOrDir == 'r':
      modifiedFilePaths.append(mod)
    else:
      pass
  
  
  imageNames = [deltas['delta'], deltas['next']]
  
  if not path.exists('{0}/{1}'.format(out,'icat')):
    mkdir('{0}/{1}'.format(out,'icat'))

  
  differentPathNames = {}
  
  for name in imageNames:
    for mod in modifiedFilePaths:
      pathName = mod[1].split('/')[-1].split('.')[0]
      fileName = mod[1].split('/')[-1]
      if fileName in differentPathNames:
        differentPathNames[fileName].append("{0}-{2}-{1}.txt".format(name.replace('_','-'), mod[2] ,pathName))
      else:
        differentPathNames[fileName] = ["{0}-{2}-{1}.txt".format(name.replace('_','-'), mod[2] ,pathName)]
      
      srcPath = "/mnt/img-store/scn-1/images"
      cmd = "icat {4}/{0}.img {1} > {2}/icat/{0}-{3}-{1}.txt".format(name.replace('_','-'), mod[2], out, pathName, srcPath)
      
      
      res = system(cmd)
      
      if res == 0:
        main_logger.debug('[METHODS] - Retrieving file succesfull!')
  
  if not path.exists('{0}/{1}'.format(out,'diff')):
    mkdir('{0}/{1}'.format(out,'diff'))

  for key in differentPathNames.keys():
    paths = differentPathNames[key]
    diffFileName = "{0}.txt".format(key.split('.')[0])
    cmd = "diff -u {0}/icat/{1} {0}/icat/{2} > {0}/diff/{3}".format(out, paths[0], paths[1], diffFileName)
    res = system(cmd)
    if res == 0:
      main_logger.debug('[METHODS] - Diffing of files succesfull!')
