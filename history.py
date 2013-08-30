#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, User, Transaction, Transaction
from data import db
from sessions import SessionManager

import config
import json
import forms
import pages


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()

        if sessionUser['id'] == 0:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()

        try:
            status = request.args.get('status')[0]
        except:
            status = 'pending'

        filters = {'status': status}

        Page = pages.History('Smart Property Group - Transaction History', 'history', filters)
        Page.sessionUser = sessionUser
        Page.sessionResponse = sessionResponse

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Transactions(Element):
    def __init__(self, filters, sessionUser):
        self.status = filters['status']
        self.sessionUser = sessionUser

        transactions = db.query(Transaction)
        transactions = transactions.filter(Transaction.userId == sessionUser['id'])
        if self.status == 'pending':
            transactions = transactions.filter(Transaction.status.in_(['open'])).order_by(Transaction.updateTimestamp.desc())
        if self.status == 'canceled':
            transactions = transactions.filter(Transaction.status == 'canceled').order_by(Transaction.updateTimestamp.desc())
        if self.status == 'complete':
            transactions = transactions.filter(Transaction.status == 'complete').order_by(Transaction.updateTimestamp.desc())

        if transactions.count() == 0:
            template = 'templates/elements/history0.xml'
        else:
            template = 'templates/elements/history1.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.transactions = transactions

    @renderer
    def count(self, request, tag):
        statuses = {'pending': 'Pending',
                    'canceled': 'Canceled',
                    'complete': 'Complete'}

        slots = {}
        slots['htmlTransactionStatus'] = statuses[self.status]
        slots['htmlTransactionCount'] = str(self.transactions.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def transactionStatus(self, request, tag):
        statuses = {'pending': 'Pending',
                    'canceled': 'Canceled',
                    'complete': 'Complete'}

        for key in statuses:
            thisTagShouldBeSelected = False

            if key == self.status:
                thisTagShouldBeSelected = True

            slots = {}
            slots['inputValue'] = key
            slots['inputCaption'] = statuses[key]
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag

    @renderer
    def row(self, request, tag):
        for transaction in self.transactions:
            timestamp = float(transaction.createTimestamp)

            slots = {}
            #slots['htmlStatus'] = str(transaction.status)
            slots['htmlTransactionCreateTimestamp'] = config.convertTimestamp(timestamp)
            slots['htmlTransactionUpdateTimestamp'] = config.convertTimestamp(timestamp)
            slots['htmlTransactionId'] = str(transaction.id)
            slots['htmlTransactionAmount'] = str(transaction.amount) 
            slots['htmlTransactionBitcoinAddress'] = str(transaction.bitcoinAddress) 
            self.transaction = transaction
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        actions = {}
        actions[config.createTimestamp()] = ['View', 'ticon view hint hint--top hint--rounded', '../describeProperty']
        actions[config.createTimestamp()] = ['Delete', 'ticon delete hint hint--top hint--rounded', '../deleteProperty?id=%s' % self.transaction.id]

        for key in sorted(actions.keys()):
            slots = {}
            slots['htmlId'] = str(self.transaction.id)
            slots['htmlHint'] = actions[key][0]
            slots['htmlClass'] = actions[key][1]
            slots['htmlUrl'] = actions[key][2]
            newTag = tag.clone().fillSlots(**slots)
            yield newTag
