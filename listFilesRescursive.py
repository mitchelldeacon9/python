#!/usr/bin/python
# This script traverses a directory tree and lists interior dirs/files recursively
# To run the script, pass in full path name of directory as argument

import sys
import os

def drillFiles(dir,files):
    fileList = []
    for file in files:
        fileName = os.path.join(dir,file)  #make full pathname of files
        fileList.append(fileName)          #append filenames to list
    return fileList

def traverse(rootDir):
    fileList = []
    for root, subDirs, files in os.walk(rootDir): #traverse dir tree recursively
        fileList.append(root)                     #append directories to list
        fileList += drillFiles(root,files)
    fileList.sort                                 #sort list alphabetically
    for file in fileList: print file              #print directories and filenames

def main(rootDir):
    if os.path.isdir(rootDir): #verify arg passed to script is valid directory pathname
        traverse(os.path.abspath(rootDir))
    else: 
        print '\nThe directory you entered is not a valid pathname on this system.'
        print 'Please verify correct pathname of the directory and try again.\n'

if __name__ == '__main__':
    if len(sys.argv) != 1:  #verify at least one argument passed to script
        main(sys.argv[1])
    else:
        print '\nPlease enter a directory name as the first and only argument to this script.\n'
        raise SystemExit(1) #if no arg passed to script, throw error and exit
