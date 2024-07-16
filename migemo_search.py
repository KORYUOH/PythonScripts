import os
import re
import sys
import migemo
import yaml
import glob
    
def read_config(yaml_path):
    if not os.path.isfile(yaml_path):
        print(yaml_path + " is not exists")
        exit()
    with open(yaml_path , encoding='utf-8') as file:
        return yaml.safe_load(file.read())

def main(argv):
    files = []
    
    if( len(argv)< 2 ):
        return
    config = read_config(argv[2])
    
    if 'verbose' in config :
        Verbose = config['verbose']
    else:
        Verbose = False

    if 'recursive' in config :
        Recursive = config['recursive']
    else:
        Recursive = False
    
    if Verbose:
        print("=====================================")
    
    for arg in config['folders']:
        path = arg
        if Verbose: 
            print(path)

        if os.path.isdir(path):
            files.extend(os.listdir(path))
        else:
            files.extend(glob.glob(path,recursive=Recursive))
        migemodict = 'C:\Path\dict\cp932\migemo-dict'
    files = [ os.path.basename(f) for f in files ]
    files = list(dict.fromkeys(files))
    if 'dictionary' in config:
        if os.path.isfile(config['dictionary']):
            migemodict = config['dictionary']

    # print(files)

    print("=====================================")

    migemo_body = migemo.Migemo()
    migemo_search = migemo_body.query(argv[1])
    # print(migemo_search)
    ret = [ s for s in files if re.search(migemo_search, s) ]

    for f in ret:
        print(f);
    
    print("match files: {1}/{0}".format(len(files),len(ret)))

if __name__ == '__main__':
    main(sys.argv)
