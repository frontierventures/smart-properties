#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import db
from sqlalchemy.sql import and_
from data import Transaction
from sessions import SessionManager

import config
import definitions
import error
import explorer
import functions
import pages
import report


def assemble(root):
    root.putChild('lend', Main())
    root.putChild('lendAction', Lend())
    return root

class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).getSessionUser()

        if session_user['id'] == 0:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()

        session_user['page'] = 'lend'

        session_transaction = SessionManager(request).getSessionTransaction()

        if not session_transaction.get('amount'):
            session_transaction['amount'] = 1

        session_user['page'] = 'lend'

        Page = pages.Lend('Smart Property Group - Lend', 'lend')
        Page.session_user = session_user
        Page.sessionResponse = sessionResponse
        Page.session_transaction = session_transaction

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
        print "%ssession_transaction: %s%s" % (config.color.BLUE, session_transaction, config.color.ENDC)

        SessionManager(request).clearSessionResponse()
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Lend(Resource):
    def render(self, request):
        if not request.args:
            return redirectTo('../', request)

        session_user = SessionManager(request).getSessionUser()
        session_user['action'] = 'lend'

        lenderId = session_user['id']

        session_transaction = SessionManager(request).getSessionTransaction()

        btc_amount = request.args.get('btc_loan_amount')[0]

        session_transaction['lenderId'] = lenderId
        session_transaction['amount'] = btc_amount
        bitcoinAddress = explorer.getNewAddress('')['result']

        if error.amount(request, btc_amount):
            return redirectTo('../lend', request)

        btc_amount = float(btc_amount)

        if request.args.get('button')[0] == 'Get Address':
            timestamp = config.createTimestamp()

            data = {
                'status': 'open',
                'createTimestamp': timestamp,
                'updateTimestamp': timestamp,
                'userId': lenderId,
                'amount': btc_amount,
                'bitcoinAddress': bitcoinAddress,
                'statement': '',
                'signature': ''    
                }

            newTransaction = Transaction(data)
            
            db.add(newTransaction)

            db.commit()

            report.createPdf(newTransaction)

            session_transaction['id'] = newTransaction.id
            session_transaction['amount'] = newTransaction.amount
            session_transaction['createTimestamp'] = timestamp
            session_transaction['bitcoinAddress'] = newTransaction.bitcoinAddress
            session_transaction['isSigned'] = 0 

            return redirectTo('../contract', request)
