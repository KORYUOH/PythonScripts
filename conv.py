import pillow_avif
from PIL import Image
import sys
import os
import re

logfilename = 'log.txt'

def is_imgfile( filename: str ) -> bool:
    ext = filename[-4:]
    ext = ext.lower()
    return  (ext == ".png") | (ext == ".jpg") | (ext == ".gif") | (ext == "jpeg") | (ext == "avif")

def Log(message: str):
    logfile = open( logfilename , 'a' , encoding'utf-8' )
    logfile.write(message)

def main():
    files = os.listdir(os.getcwd())

    for file in files :
        try:
            if is_imgfile(file):
                input_im = Image.open('./'+ file)
                if input_im.format != "JPEG":
                    print("convert : " + file)
                    rgb_im = input_im.convert('RGB')
                    savename = file
                    if savename[-4:] != ".jpg":
                        if(savename[-4:] == "avif"):
                            savename = file[:-4]+"jpg"
                        else:
                            savename = file[:-4]+".jpg"
                    rgb_im.save('./'+savename,quality=90)
                else:
                    print("format Jpg : " + file)
                    savename = file
                    if (savename[-4:] == ".jpg" or savename[-4:] == "jpeg") :
                        extention = ".jpg"
                        if savename[-4:] == "jpeg" :
                            extention = "jpeg"

                        savename = file[:-4]+extention
                        print("rename "+file+" -> "+savename)
                        input_im.save('./'+savename)


            else : 
                print(file + " is not image")
        except Image.UnidentifiedImageError as e:
            print(file + "is ErrorFile ---")
            print(e)


if __name__ == '__main__':
    main()
