import AnyToJson
import time
import socket
import sys
import json
import requests


from datetime import datetime, timedelta

class ElasticSend(AnyToJson.AnyToJson):
    def __init__(self, ):
        super().__init__()

        self.out_host = self.conf.get('connection', 'output_host')
        self.out_port = self.conf.get('connection', 'output_port')


    def send(self, data):

        if type(data) is not dict:
            return False

        data["time.source"] = (datetime.today() - timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S')

        data = json.dumps(data)
        print(data)
        req = requests.post('http://'+self.out_host+':'+self.out_port+'/events-'+datetime.today().strftime('%Y.%m.%d')+'/_doc',data=data,headers={"content-type":"application/json"})
        print(req.text)
