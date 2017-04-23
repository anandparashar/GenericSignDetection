'''
Created on Apr 23, 2017

@author: Erich O'Saben
'''

"""
Main entry point to the Generic Sign Detection
"""

from evaluate import *
from lineVerification import *
import utils


def main():
    print "global path variables..."
    
    print utils.DATA_ROOT_PATH

    for key, value in utils.IMAGE_DIRS.items():
        print "directory: ", key
        print "all images are in: ", utils.IMAGE_DIRS[key]["path"]
        print "annotation file is at: ", utils.IMAGE_DIRS[key]["aFile"] #annotation file

if __name__ == '__main__':
    main()