#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import can


host = "192.168.1.3" #お使いのサーバーのホスト名を入れます
port = 19227 #クライアントと同じPORTをしてあげます

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversock.bind((host,port)) #IPとPORTを指定してバインドします
serversock.listen(10) #接続の待ち受けをします（キューの最大数を指定）
print('Waiting for client connections...')
clientsock, client_address = serversock.accept() #接続されればデータを格納
print('connected')

bus = can.interface.Bus(channel = 'can0', bustype='socketcan_native', bitrate=500000, canfilters=None)

class CallBackFunction(can.Listener):
    def on_message_received(self, msg):
        eth_send_msg = 'M SD' + str(msg.dlc) + ' ' + \
                   format(msg.arbitration_id, 'x').zfill(3) + ' ' + \
                   format(msg.data[0], 'X').zfill(2) + ' ' + \
                   format(msg.data[1], 'X').zfill(2) + ' ' + \
                   format(msg.data[2], 'X').zfill(2) + ' ' + \
                   format(msg.data[3], 'X').zfill(2) + ' ' + \
                   format(msg.data[4], 'X').zfill(2) + ' ' + \
                   format(msg.data[5], 'X').zfill(2) + ' ' + \
                   format(msg.data[6], 'X').zfill(2) + ' ' + \
                   format(msg.data[7], 'X').zfill(2) + ' ' + \
                   '\r\n'

#        print(eth_send_msg)
        clientsock.send(eth_send_msg.encode())

call_back_function = CallBackFunction()
can.Notifier(bus, [call_back_function, ])

data = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
can_send_msg = can.Message(arbitration_id=0x1, dlc=8, data=data)

while True:
    while True:
        can_recv_msg = clientsock.recv(1024)

        can_recv_msgs = can_recv_msg.decode('UTF-8').split(' ')

        can_send_msg.dlc = int(can_recv_msgs[1][2])
        can_send_msg.arbitration_id = int(can_recv_msgs[2], 16)
        can_send_msg.data[0] = int(can_recv_msgs[3], 16)
        can_send_msg.data[1] = int(can_recv_msgs[4], 16)
        can_send_msg.data[2] = int(can_recv_msgs[5], 16)
        can_send_msg.data[3] = int(can_recv_msgs[6], 16)
        can_send_msg.data[4] = int(can_recv_msgs[7], 16)
        can_send_msg.data[5] = int(can_recv_msgs[8], 16)
        can_send_msg.data[6] = int(can_recv_msgs[9], 16)
        can_send_msg.data[7] = int(can_recv_msgs[10], 16)

        bus.send(can_send_msg)
#        print(can_recv_msgs)

    clientsock.close()
    print('client is disconnected')
    print('Waiting for next connections...')
    clientsock, client_address = serversock.accept() #接続されればデータを格納

clientsock.close()
