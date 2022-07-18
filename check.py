import sys
import os

# 無視ファイルリスト
def is_excludefiles( filename: str ) -> bool:
    excludefiles = ['convert.py' , 'convert.bat' , 'digits.py' , 'digits.bat','copyandexecute.bat' , 'log.txt'] 
    return filename in excludefiles

# SJIS(CP932) で使えない文字が入っているか
def check_sjis_error( filename: str ) -> bool:
    copy = filename.encode('cp932',errors='ignore').decode('cp932')
    return copy != filename

def main():
    files = os.listdir(os.getcwd())
    logfile = open('log.txt' , 'w' , encoding='UTF-8' )
    sjis_error_count = 0

    for file in files:
        #フォルダを回す
        if is_excludefiles(file):
            continue
        if os.path.isfile(file):
            continue
        
        # フォルダの中身を回す
        infile = os.listdir(file)
        count = {}
        infolder = False
        for filename in infile:
            if os.path.isdir(filename):
                continue
            # print(filename + ' ' + str(len(filename)))
            if not len(filename) in count:
                count[len(filename)]=1
            else:
                count[len(filename)] = count[len(filename)] + 1

        # ファイルの長さがあってないと2つ以上できる
        if len(count) > 1 :
            # print(file)
            logfile.write(file + '\n')
            txt = []
            for key , value in count.items():
                txt.append('\t\tfile length : ')
                txt.append(format(key , ' 4d'))
                txt.append('\tcount : ')
                txt.append(format(value , ' 4d'))
                txt.append('\n')
            logfile.writelines(txt)

        if check_sjis_error(file):
            logfile.write('[SJISERR] ' + file + '\n')

    if sjis_error_count > 0 :
        tk.Tk().withdraw()
        messagebox.showinfo('Error', 'SJISErrorフォルダが{0}件あります'.format(sjis_error_count))

if __name__ == '__main__':
    main()
