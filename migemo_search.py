import os
import re
import sys
import migemo
import yaml
    
def read_config(yaml_path):
    if not os.path.isfile(yaml_path):
        print(yaml_path + " is not exists")
        exit()
    with open(yaml_path) as file:
        return yaml.safe_load(file.read())

def main(argv):
    files = []
    if( len(argv)< 2 ):
        return
    config = read_config(argv[2])
    for arg in config['folders']:
        path = arg
        print(path)
        files.extend(os.listdir(path))
        migemodict = 'C:\Path\dict\cp932\migemo-dict'
    if os.path.isfile(config['dictionary']):
        migemodict = config['dictionary']

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
