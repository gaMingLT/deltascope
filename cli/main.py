import argparse, os, sys
from delta_scope import delta_images_cli

# currentdir = os.path.dirname(os.path.realpath(__file__))
# parentdir = os.path.dirname(currentdir)
# sys.path.append(parentdir)

def main():
  args = parseargs()
  directoryName = delta_images_cli(args.images)


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
