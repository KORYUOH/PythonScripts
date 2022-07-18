﻿# Readme
Python Files.
ファイルを扱う上でのパイソンコンバータファイルとか

# file descriptions

## conv
convert to avif , png , gif to jpg file
AVIFとかpngをjpgに変換する

### require
Pillow
Pillow-avif-plugin

## copyandexecure
copy and execute 'conv'
conv関係を同じフォルダの仮想にコピーし実行する
### require
conv

## digits
fix number
ex.
1   -> 001

09  -> 009

010 -> 010

ファイルの桁数合わせ
とりあえず0埋め3桁で指定


## tosjisname
check filename unicode folder name to sjis foler name
ex.
test ⑨ -> test

UnicodeでSJISに変換できないフォルダ名を変更する

## check
check file name length check

仮想フォルダのファイル名の長さチェック
桁数合わせなどでずれているとかをログファイルに出力

