#from pprint import pformat
from twisted.internet import reactor, task
from twisted.internet import error
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

import json
import config

from data import Price
from data import db

import definitions


def getLast(data):
    #print data
    data = json.loads(data)
    print data['result']

    timestamp = config.createTimestamp()
    currency = data['data']['last']['currency']
    print currency
    print
    price = db.query(Price).filter(Price.currencyId == currency).first()
    price.timestamp = timestamp
    price.last = data['data']['last']['value']
    db.commit()


class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10
        self._buffer = []

    def dataReceived(self, bytes):
        if self.remaining:
            display = bytes[:self.remaining]
            self._buffer.append(bytes)
            #print 'Some data received:'
            #print display
            self.remaining -= len(display)

    def connectionLost(self, reason):
        print 'Finished receiving body:', reason.getErrorMessage()
        data = ''.join(self._buffer)
        getLast(data)
        self.finished.callback(None)

agent = Agent(reactor)


def get():
    for currency in definitions.currencies:
        url = 'https://data.mtgox.com/api/2/BTC%s/money/ticker' % currency
        d = agent.request(
            'GET',
            url,
            Headers({'User-Agent': ['Pinging Agent']}),
            None)

        d.addCallback(cbRequest, currency)
        reactor.callWhenRunning(setTimeout, d, reactor, currency, 2)


def setTimeout(d, r, currency, timeout):
    def f():
        print 'Cancelling pull request for %s' % currency
        return d.cancel()
    canceler = r.callLater(timeout, f)

    def cancelCanceler(result):
        try:
            canceler.cancel()
        except (error.AlreadyCalled, error.AlreadyCancelled):
            pass
        return result
    d.addBoth(cancelCanceler)


def cbRequest(response, currency):
    print 'Response code:', response.code
    print "Currency: %s" % currency
    finished = Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished

l = task.LoopingCall(get)
l.start(30)
reactor.run()
