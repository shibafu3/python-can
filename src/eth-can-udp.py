#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import can
import RPi.GPIO as GPIO


recv_ip = "192.168.5.10" #お使いのサーバーのホスト名を入れます
send_ip = "192.168.5.4" #お使いのサーバーのホスト名を入れます
port = 19227 #クライアントと同じPORTをしてあげます

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((recv_ip, port)) #IPとPORTを指定してバインドします

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
        sock.sendto(eth_send_msg.encode(), (send_ip, port))

call_back_function = CallBackFunction()
can.Notifier(bus, [call_back_function, ])

data = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
can_send_msg = can.Message(arbitration_id=0x1, dlc=8, data=data)
eth_recv_msg = 'M SD8 123 01 23 45 67 89 AB CD EF \r\n'
can_itr = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, 0)

while True:
    data = sock.recv(1024)
    eth_recv_msg = str(data.decode('UTF-8'))

    eth_recv_msgs = eth_recv_msg.split(' ')

    can_send_msg.dlc = int(eth_recv_msgs[1][2])
    can_send_msg.arbitration_id = int(eth_recv_msgs[2], 16)
    can_send_msg.data[0] = int(eth_recv_msgs[3], 16)
    can_send_msg.data[1] = int(eth_recv_msgs[4], 16)
    can_send_msg.data[2] = int(eth_recv_msgs[5], 16)
    can_send_msg.data[3] = int(eth_recv_msgs[6], 16)
    can_send_msg.data[4] = int(eth_recv_msgs[7], 16)
    can_send_msg.data[5] = int(eth_recv_msgs[8], 16)
    can_send_msg.data[6] = int(eth_recv_msgs[9], 16)
    can_send_msg.data[7] = int(eth_recv_msgs[10], 16)

    bus.flush_tx_buffer()
    bus.send(can_send_msg)
    print(eth_recv_msgs)

sock.close()

