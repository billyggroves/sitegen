from textnode import *
from os import path, listdir, mkdir
from shutil import rmtree, copytree
import time

path_to_static = "./static/"
path_to_public = "./public/"

def delete_public():
    if path.exists(path_to_public) and len(listdir(path_to_public)) > 0:
        print(listdir(path_to_public))
        rmtree(path_to_public)
    return

def copy_files():
    if path.exists(path_to_static) and len(listdir(path_to_static)) > 0:
        print(listdir(path_to_static))
        copytree(path_to_static,path_to_public)
    return

def main():
    delete_public()
    copy_files()

main()