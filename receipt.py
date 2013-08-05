#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import db
from data import Order, Transaction
from sessions import SessionManager

import config
import decimal
import pages
D = decimal.Decimal


class Main(Resource):
    def render(self, request):

        sessionTransaction = SessionManager(request).getSessionTransaction()
        #transactionId = sessionTransaction['id']

        if sessionTransaction['id'] == 0:
            return redirectTo('../', request)

        #investorId = sessionTransaction['investorId']

        #transaction = db.query(Transaction).filter(Transaction.id == transactionId).first()

        sessionUser = SessionManager(request).getSessionUser()

        Page = pages.Receipt('Smart Property Group - Receipt', 'receipt')
        Page.sessionUser = sessionUser
        Page.sessionTransaction = sessionTransaction

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        print "%ssessionTransaction: %s%s" % (config.color.BLUE, sessionTransaction, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Receipt(Element):
    def __init__(self, sessionTransaction):
        self.sessionTransaction = sessionTransaction
        self.loader = XMLString(FilePath('templates/elements/receipt.xml').getContent())

    @renderer
    def details(self, request, tag):
        slots = {}
        slots['htmlTotal'] = str(self.sessionTransaction['amount'])
        slots['htmlPaymentAddress'] = str(self.sessionTransaction['bitcoinAddress'])
        yield tag.fillSlots(**slots)
