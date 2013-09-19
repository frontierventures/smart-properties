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

        session_transaction = SessionManager(request).getSessionTransaction()
        #transactionId = session_transaction['id']

        if session_transaction['id'] == 0:
            return redirectTo('../', request)

        #lenderId = session_transaction['lenderId']

        #transaction = db.query(Transaction).filter(Transaction.id == transactionId).first()

        session_user = SessionManager(request).getSessionUser()
        session_user['page'] = 'receipt'

        Page = pages.Receipt('Smart Property Group - Receipt', 'receipt')
        Page.session_user = session_user
        Page.session_transaction = session_transaction

        print "%ssession_user: %s%s" % (config.color.YELLOW, session_user, config.color.ENDC)
        print "%ssession_transaction: %s%s" % (config.color.YELLOW, session_transaction, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Receipt(Element):
    def __init__(self, session_transaction):
        self.session_transaction = session_transaction
        self.loader = XMLString(FilePath('templates/elements/receipt.xml').getContent())

    @renderer
    def details(self, request, tag):
        slots = {}
        slots['htmlTotal'] = str(self.session_transaction['amount'])
        slots['htmlPaymentAddress'] = str(self.session_transaction['bitcoinAddress'])
        slots['htmlSignature'] = str(self.session_transaction['signature'])
        slots['htmlContractUrl'] = '../files/contract-%s.pdf' % str(self.session_transaction['id'])
        yield tag.fillSlots(**slots)
