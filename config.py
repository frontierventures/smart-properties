#!/usr/bin/env python
import os
import time
from datetime import datetime


class color:
    HEADER = '\033[1;45m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.RED = ''
        self.ENDC = ''


def createTimestamp():
    return time.time()


def convertTimestamp(timestamp):
    utc = datetime.utcfromtimestamp(timestamp)
    format = "%a %e %b %Y %r %Z"
    timestamp = utc.strftime(format)
    return timestamp


def convertTimestampToHours(timestamp):
    utc = datetime.utcfromtimestamp(timestamp)
    format = "%H:%M:%S"
    timestamp = utc.strftime(format)
    #timestamp = time.strftime('%H:%M:%S', timestamp)
    return timestamp


def convertTimestampToDays(timestamp):
    utc = datetime.utcfromtimestamp(timestamp)
    format = "%j:%H:%M:%S"
    timestamp = utc.strftime(format)
    #timestamp = time.strftime('%H:%M:%S', timestamp)
    return timestamp


cdn = 'http://images.coingig.com';
