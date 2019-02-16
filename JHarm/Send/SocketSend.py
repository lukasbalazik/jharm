#!/usr/bin/env python3


import AnyToJson
import time
import socket
import threading
import json


class SocketSend(AnyToJson.AnyToJson):
    def __init__(self, ):
        super().__init__()

        self.out_host = self.conf.get('connection', 'output_host')
        self.out_port = self.conf.getint('connection', 'output_port')
        
        try:
            self.remote = socket.gethostbyname(self.out_host)
        except Exception as e:
            return False


    def send(self, data):
        if type(data) is not dict:
            return False

        data = json.dumps(data)
        self.socket_connect()

        try:
            self.s.send(data.encode())
            self.s.close()
        except:
            print("Send problem. Trying to resend")
            self.s.close()
            return self.send(data)


    def socket_connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.s.connect((self.remote, int(self.out_port)))
        except Exception as e:
            print(e)
            return False
