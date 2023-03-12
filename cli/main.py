import argparse
from delta_scope import delta_images


def main():
  args = parseargs()
  directoryName = delta_images(args.images)


def parseargs():
  parser = argparse.ArgumentParser(
                    prog='Delta Scope',
                    description='What the program does',
                    epilog='Text at the bottom of help')
  
  parser.add_argument('images', metavar='/path', type=str, nargs='+',
                    help='image paths')
  
  args = parser.parse_args()
  
  return args
  

if __name__ == "__main__":
  main()
