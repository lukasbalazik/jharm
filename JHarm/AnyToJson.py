import sys
import configparser

from abc import ABC
from abc import abstractmethod

class AnyToJson(ABC):
    def __init__(self):
        super().__init__()
        self.conf = configparser.ConfigParser()
        self.conf.read(sys.argv[1])

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

