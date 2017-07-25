#!/usr/bin/python
# This function takes the name of a directory and prints out the paths files within that directory 
# as well as any files contained in contained directories. 
# To use the script, set variable 'path' to the pathname of the directory of your choice.

import os                                       
path='/home'

def print_dir_contents(path):
    for child in os.listdir(path):                
        child_path = os.path.join(path,child)
        if os.path.isdir(child_path):
            print_dir_contents(child_path)
        else:
            print(child_path)

print_dir_contents(path)
