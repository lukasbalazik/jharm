import sys
import configparser
import logging
import json
import datetime
import time

from abc import ABC
from abc import abstractmethod

class AnyToJson(ABC):
    def __init__(self):
        super().__init__()
        self.conf = configparser.ConfigParser()
        self.conf.read(sys.argv[1])
        self.set_exclude()
        self.set_include()
        self.setup_logging() 
        self.received_lines = 0
        self.incident_count = 0
        self.source = self.conf.get('detection', 'source')


    def setup_logging(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('/var/log/JHarm.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger


    def set_exclude(self):
        self.exclude = []
        if 'exclude' in self.conf.options('detection'):
            self.exclude = self.conf.get('detection', 'exclude').split(',')


    def set_include(self):
        self.include = []
        if 'include' in self.conf.options('detection'):
            self.include = self.conf.get('detection', 'include').split(',')


    def check_exclude(self, event_id):
        if event_id in self.exclude:
            return False


    def check_include(self, event_id):
        if event_id not in self.include and self.include != []:
            return False
         

    def create_stats(self):
        while True:
            output = {}
            output["Received Lines"] = self.received_lines
            output["Incidents"] = self.incident_count
            output["Timestamp"] = datetime.datetime.fromtimestamp(time.time()).strftime('%d.%m.%Y %H:%M:%S')

            file='/run/jh_'+self.source+'.stats' 
            with open(file, 'w') as f:
                f.write(json.dumps(output))

            self.received_lines = 0
            self.incident_count = 0
            time.sleep(600)

    @abstractmethod
    def run(self):
        # receive events
        # call parse() on them
        pass

    @abstractmethod
    def parse(self, row):
        # parse a row
        # eventually, call send() on a completed event
        pass

    @abstractmethod
    def send(self, event):
        # send a single event out
        pass

