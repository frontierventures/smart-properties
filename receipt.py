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
        transactionId = sessionTransaction['id']
        investorId = sessionTransaction['investorId']

        if not transactionId:
            return redirectTo('../', request)

        transaction = db.query(Transaction).filter(Transaction.id == transactionId).first()

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
    def __init__(self, order):
        self.order = order
        self.loader = XMLString(FilePath('templates/elements/receipt.xml').getContent())

    @renderer
    def details(self, request, tag):
        slots = {}
        #slots['htmlTotal'] = str(D(self.order.subTotal) + D(self.order.shippingCost))
        #slots['htmlBitcoinAddress'] = str(self.order.paymentAddress)
        #slots['htmlStorename'] = str(self.store.name)
        #slots['htmlStoreUrl'] = "../%s" % self.store.name
        yield tag.fillSlots(**slots)
