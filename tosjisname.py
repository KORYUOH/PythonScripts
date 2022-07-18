import sys
import os

def get_sjis_name( filename: str ) -> str:
    return filename.encode('cp932',errors='ignore').decode('cp932')

def is_sjis_error( filename: str ) -> bool:
    return filename != get_sjis_name(filename)

def rename( path: str ):
    oldpath = path
    newpath = get_sjis_name(path)
    Log(oldpath + '\t' + newpath + '\n')
    os.rename(oldpath,newpath)

def ParseArgv(args) -> dict:
    ret = {}
    for arg in args:
        if arg == 'verbose':
            ret[arg] = True
    return ret

def Log(message: str):
    logfile = open('log.txt' , 'a' , encoding='UTF-8' )
    logfile.write(message)

def VLog(message: str, option: dict):
    if 'verbose' in option:
        Log(message)

def main(argv):
    option = ParseArgv(argv)
    open('log.txt' , 'w' , encoding='UTF-8' )
    files = os.listdir(os.getcwd())
    for file in files:
        if os.path.isfile(file):
            VLog('skip in ' + file + '\n',option)
            continue
        if not is_sjis_error(file):
            VLog('Skip is not SJIS Error : ' + file + '\n' , option)
            continue
        rename(file)

if __name__ == '__main__':
    main(sys.argv)
