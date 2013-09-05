#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString

from sessions import SessionManager

import config
import locale
import pages

from data import db
from sqlalchemy.sql import and_
from data import Profile, Price, Transaction
from sessions import SessionManager


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['page'] = 'account'

        if sessionUser['id'] == 0:
            return redirectTo('../', request)

        Page = pages.Account('Smart Property Group - Account', 'account')
        Page.sessionUser = sessionUser

        print "%ssessionUser: %s%s" % (config.color.YELLOW, sessionUser, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Details(Element):
    def __init__(self, sessionUser):
        self.sessionUser = sessionUser

        self.lender = db.query(Profile).filter(Profile.id == sessionUser['id']).first()
        self.solicitor = db.query(Profile).filter(Profile.id == 1).first()

        if sessionUser['status'] == 'verified':
            template = 'templates/elements/account0.xml'
        else:
            template = 'templates/elements/account1.xml'

        self.loader = XMLString(FilePath(template).getContent())

    @renderer
    def details(self, request, tag):
        locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')

        price = db.query(Price).filter(Price.currencyId == 'USD').first()

        lenderBalanceBTC = float(self.lender.balance) / float(price.last)
        solicitorBalanceBTC = float(self.solicitor.balance) / float(price.last)

        slots = {}
        slots['htmlPaymentAddress'] = str(self.lender.bitcoinAddress) 
        slots['htmlAvailableBalanceFiat'] = str(self.solicitor.balance) 
        slots['htmlLoanBalanceFiat'] = str(self.lender.balance) 

        slots['htmlAvailableBalanceBtc'] = str(solicitorBalanceBTC) 
        slots['htmlLoanBalanceBtc'] = str(lenderBalanceBTC) 

        slots['htmlNextPaymentDate'] = str(config.convertTimestamp(float(config.createTimestamp())))
        slots['htmlReturnRate'] = str('0.85%') 
        yield tag.clone().fillSlots(**slots)

    @renderer
    def transaction(self, request, tag):
        transactions = db.query(Transaction).filter(Transaction.userId == self.sessionUser['id'])
        transactions = transactions.filter(Transaction.status == 'complete')
        transactions = transactions.order_by(Transaction.createTimestamp.desc())

        for transaction in transactions: 
            slots = {}
            slots['htmlContractName'] = 'Contract #%s' % str(transaction.id)
            slots['htmlContractUrl'] = '../files/contract-%s.pdf' % str(transaction.id)
            yield tag.clone().fillSlots(**slots)

