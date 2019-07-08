# -*- coding:utf-8 -*-
import socket
import time

host = "127.0.0.1" #お使いのサーバーのホスト名を入れます
port = 19277 #適当なPORTを指定してあげます

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成をします

client.connect((host, port)) #これでサーバーに接続します

while True:
    client.send(b'M SD8 100 01 23 45 67 89 AB CD EF \r\n') #適当なデータを送信します（届く側にわかるように）
    
    response = client.recv(128) #レシーブは適当な2の累乗にします（大きすぎるとダメ）

    print(response)
    time.sleep(0.001)
