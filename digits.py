import sys
import os
import re

def main():
    path = os.getcwd()
    files = os.listdir(path)
    ## そろえる桁数
    digits = 3
    ## 変更する数値の位置
    position = 0

    #フォーマット用（0埋め)文字列作成
    formater = "{:0"+str(digits)+"d}"

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
            if index2 == position :
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
    main()
