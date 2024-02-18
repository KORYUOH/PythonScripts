import os
import sys
import argparse

logfilename = "log.txt"

def parse_mls(filepath):
    mls = open(filepath , 'r' , encoding='cp932')
    data = [s.rstrip() for s in mls.readlines() ]
    disp = data[::2]
    path = [s.removeprefix('@') for s in data[1::2]]
    return dict(zip(disp,path))

def Log(text : str):
    logfile = open( logfilename , 'a' , encoding='utf-8' )
    logfile.write(text)
    logfile.write('\n')

def main(argv):

    folder = ""
    mls = ""

    # initialize log
    open(logfilename , 'w' , encoding='cp932')

    parser = argparse.ArgumentParser(description='folder and Target Files')
    parser.add_argument('--folder', '-f' , type=str , help='check folder' , default=folder)
    parser.add_argument('--mls' , '-m' , type=str , help='check mls' , default=mls)
    arg = parser.parse_args();
    check_folder = arg.folder
    mlsFilePath = arg.mls
    if(not os.path.isfile(arg.mls)):
        print("Not Found {0}".format(art.mls))
        return

    paths = parse_mls(mlsFilePath)

    files = os.listdir(check_folder)

    missmatchlist = list()

    for fpath in files:
        if os.path.isdir(check_folder + '/' +fpath):
            if fpath not in paths.keys():
                missmatchlist.append(fpath)
                Log('missmatch : ' + fpath)

    print('no hit folder {0}'.format(len(missmatchlist)))
    for s in missmatchlist:
        print(s)


if __name__ == '__main__':
    main(sys.argv)
