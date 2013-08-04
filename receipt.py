#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.server import NOT_DONE_YET
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import db
from data import Order
from sessions import SessionManager

import config
import decimal
import pages
D = decimal.Decimal


class Main(Resource):
    def render(self, request):

        sessionOrder = SessionManager(request).getSessionOrder()
        orderId = sessionOrder['id']

        if not orderId:
            return redirectTo('../', request)

        order = db.query(Order).filter(Order.id == orderId).first()

        sessionUser = SessionManager(request).getSessionUser()
        investorId = sessionOrder['investorId']

        Page = pages.Receipt('Receipt', 'receipt')
        Page.sessionUser = sessionUser
        Page.sessionOrder = sessionOrder

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        print "%ssessionOrder: %s%s" % (config.color.BLUE, sessionOrder, config.color.ENDC)
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
