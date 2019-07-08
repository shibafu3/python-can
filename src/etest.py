#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, 1)

host = "192.168.5.10" #お使いのサーバーのホスト名を入れます
port = 19227          #クライアントと同じPORTをしてあげます


serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # TCP通信用にソケットを設定
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 2)  # ソケットのオプション
serversock.bind((host,port)) #IPとPORTを指定してバインドします
serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）
print('Waiting for client connections...')
clientsock, client_address = serversock.accept() #接続されればデータを格納
print('connected')
GPIO.output(21, 0)

eth_send_msg = 'M SD8 123 01 23 45 67 89 AB CD EF \r\n'
while True:
    clientsock.send(eth_send_msg.encode())

clientsock.close()
serversock.close()
