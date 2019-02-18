import AnyToJson
import time
import socket
import sys
import zmq
import json

class ZeroMQSend(AnyToJson.AnyToJson):
    def __init__(self, ):
        super().__init__()

        self.out_host = self.conf.get('connection', 'output_host')
        self.out_port = self.conf.get('connection', 'output_port')


    def send(self, data):
        if type(data) is not dict:
            return False

        data = json.dumps(data)
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://"+self.out_host+":"+self.out_port)
        socket.send_string(data)

