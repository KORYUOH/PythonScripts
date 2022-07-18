import sys
import os

def get_sjis_name( filename ) -> str:
    return filename.encode('cp932',errors='ignore').decode('cp932')

def is_sjis_error( filename ) -> bool:
    return filename != get_sjis_name(filename)

def rename( path ):
    oldpath = path
    newpath = get_sjis_name(path)
    logfile = open('log.txt' , 'a' , encoding='UTF-8' )
    logfile.write(oldpath + '\t' + newpath + '\n')
    os.rename(oldpath,newpath)

open('log.txt' , 'w' , encoding='UTF-8' )
files = os.listdir(os.getcwd())
for file in files:
    if os.path.isfile(file):
        continue
    if not is_sjis_error(file):
        continue
    rename(file)

