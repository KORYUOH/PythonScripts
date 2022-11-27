import os
import re
import sys
import migemo
    

def main(argv):
    path = argv[2]
    files = os.listdir(path)
    if len(argv) > 3:
        path2 = argv[3]
        files2 = os.listdir(path2)
        files.extend(files2)
    migemodict = 'C:\Path\dict\cp932\migemo-dict'

    # print(files)


    migemo_body = migemo.Migemo()
    migemo_search = migemo_body.query(argv[1])
    # print(migemo_search)
    ret = [ s for s in files if re.search(migemo_search, s) ]

    for f in ret:
        print(f);
    
    print("match files: {1}/{0}".format(len(files),len(ret)))

if __name__ == '__main__':
    main(sys.argv)
