import sys
import os
import re
import argparse

def main(argv):
    path = os.getcwd()
    files = os.listdir(path)
    ## そろえる桁数
    digits = 3
    ## 変更する数値の位置
    position = 0
    
    parser = argparse.ArgumentParser(description='Digits Style')
    parser.add_argument('--digits' , '-d' , type=int , help='digits of 0 fills' , default=digits)
    parser.add_argument('--position' , '-pos' , '-p' , type=int , help='multi number fix position 0 origin',default=position)
    arg = parser.parse_args()
    digits = arg.digits
    position = arg.position

    #フォーマット用（0埋め)文字列作成
    formater = "{:0"+str(arg.digits)+"d}"

    # 置き換え用辞書
    dic={}
    for index,file in enumerate(files):
        # 数値のみ切り出し
        nums = re.findall("[0-9]+",file)
        if len(nums) == 0:
            continue
        # 数値以外を切り出し
        txts = re.split("[0-9]+",file)

        # 指定位置の数値を整形
        for index2,text in enumerate(nums):
            if index2 == arg.position :
                # 数値が少ないので0埋め
                if len(text) < digits:
                    nums[index2] = formater.format(int(text))
                # 桁が多すぎるので削る
                if len(text) > digits:
                    nums[index2] = text[-1*digits:]
        name=""
        # テキスト + 数値 でファイル名を生成
        for index2,text in enumerate(txts):
            name += text
            if len(nums) > index2:
                name += nums[index2]
        # 元ファイル名を キー 変更後を値とする
        dic[file] = name

    # 置き換え
    for key,value in dic.items():
        print("rename : " + key + " >>> " + value)
        if(os.path.exists(key)):
            if(not os.path.exists(value)):
                os.rename(key,value)

if __name__ == '__main__':
    main(sys.argv)
