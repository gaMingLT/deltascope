from cli.loger import main_logger
from os import mkdir, path, system
import dateparser, codecs


def execute_mactime(name, out: str):
  main_logger.info('[METHODS] - Creating MAC Timeline from FLS Body file')
  
  if not path.exists('{0}/{1}'.format(out,'timelines')):
    mkdir('{0}/{1}'.format(out,'timelines'))

  cmd = "mactime -b {1}/{0}.txt -d > {1}/{2}/tl.{0}.txt".format(name.replace('_','-'), out, 'timelines')
  res = system(cmd)
  
  if res == 0:
    main_logger.info('[METHODS] - Completed creating mactime line file for {0}'.format(name))


def parse_mactime_file(name, out: str):
  main_logger.info('[METHODS] - Parsing MAC Timeline file')
  path = "{1}/{2}/tl.{0}-filtered.txt".format(name.replace('_','-'), out, 'timelines')
  
  f = codecs.open(path, encoding='utf-8', errors='ignore')
  
  data = []
  for line in f.readlines():
    # TODO: Improve this!
    tempLine = line.split(',')
    date, size, activity, perm, uid, guid, inode, file_name = tempLine[0], tempLine[1], tempLine[2], tempLine[3], tempLine[4], tempLine[5], tempLine[6], tempLine[7]
    # date, size, activity, perm, uid, guid, inode, file_name = line[:24], line[24:34], line[34:39], line[39:52], line[52:54], line[61:63], line[71:78], line[78:]
    dateMili = dateparser.parse(date)
    
    fileType = perm[:3]
    ownerPerm = perm[3:6]
    groupPerm = perm[6:9]
    otherPerm = perm[9:12]
    # print(fileType, ownerPerm, groupPerm, otherPerm)
    
    mActivity, aActivity, cActivity, bActivity = activity[0], activity[1], activity[2], activity[3] 
    # print(mActivity, aActivity, cActivity, bActivity)
    
    # values = (date.strip(), size.strip(), activity.strip()  , perm.strip(), uid.strip(), guid.strip(), inode.strip(), file_name.strip())
    values = (dateMili, size, mActivity, aActivity, cActivity, bActivity  , fileType, ownerPerm, groupPerm, otherPerm , uid, guid, inode, file_name.replace('"', ''))
    
    data.append(values)
    
  print('Value mac timeline: ', data[0])

  return data


def filter_mactime_file(name, out: str):
  main_logger.info('[METHODS] - Filtering MAC Timeline file')
  
  path = "{1}/{2}/tl.{0}.txt".format(name.replace('_','-'), out, 'timelines')
  
  cmd = "grep -E '/etc/*' {0} | grep -v '/usr/share' > {2}/{3}/tl.{1}-filtered.txt".format(path, name.replace('_','-'), out, 'timelines')
  res = system(cmd)
  
  if res == 0:
    main_logger.info('[METHODS] - Filtering MAC Timeline file complete: {0}'.format(name))
