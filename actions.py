#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python .filepath import FilePath
from parsley import makeGrammar
from twisted.web.template import XMLString, Element, renderer, tags

from data import db
from data import Order, Property, Transaction
from sqlalchemy import func
from sessions import SessionManager

#import Image
import cgi
#import cloud
import commonElements
import config
import decimal
import definitions
#import descriptions
import error
import receipt
import functions
import hashlib
import inspect
import itertools
import os

D = decimal.Decimal


class AddProperty(Resource):
    def render(self, request):
        if not request.args:
            return redirectTo('../', request)

        sessionUser = SessionManager(request).getSessionUser()

        if sessionUser['type'] != 0:
            return redirectTo('../', request)

        sessionProperty = SessionManager(request).getSessionProperty()
        propertyId = sessionProperty['id']

        url = '../summaryProperties?action=add'
        url = str(url)

        title = request.args.get('propertyTitle')[0]
        description = request.args.get('propertyDescription')[0]
        address = request.args.get('propertyAddress')[0]
        totalUnits = request.args.get('propertyTotalUnits')[0]
        askingPrice = request.args.get('propertyAskingPrice')[0]

        sessionProperty['title'] = title
        sessionProperty['description'] = description
        sessionProperty['address'] = address
        sessionProperty['totalUnits'] = totalUnits
        sessionProperty['askingPrice'] = askingPrice

        #if error.propertyTitle(request, propertyTitle):
        #    return redirectTo(url, request)

        #if error.propertyDescription(request, propertyDescription):
        #    return redirectTo(url, request)

        if request.args.get('button')[0] == 'Save':
            status = 'pending'

            timestamp = config.createTimestamp()

            #(self, status, createTimestamp, updateTimestamp, title, description, address, mls, siteSize, totalUnits, askingPrice, imageHash, imageCount):
            propertyObject = Property(status, timestamp, timestamp, title, description, address, '', '',  totalUnits, askingPrice, '', 0)

            db.add(propertyObject)
            db.commit()

            #image = ProductImage(request, product.imageCount, product.imageHash).save()

            #product.imageCount = image['count']

            #product.imageHash = image['hash']
            #db.commit()
            return redirectTo('../summaryProperties', request)


class BuyProperty(Resource):
    def render(self, request):
        if not request.args:
            return redirectTo('../', request)

        sessionUser = SessionManager(request).getSessionUser()
        investorId = sessionUser['id']

        #if sessionUser['type'] != 0:
        #    return redirectTo('../', request)

        sessionOrder = SessionManager(request).getSessionOrder()
        propertyId = sessionOrder['propertyId']

        #url = '../summaryProperties?action=add'
        #url = str(url)

        quantity = int(request.args.get('propertyQuantity')[0])

        sessionOrder['quantity'] = quantity
        sessionOrder['investorId'] = investorId

        #if error.propertyTitle(request, propertyTitle):
        #    return redirectTo(url, request)

        #if error.propertyDescription(request, propertyDescription):
        #    return redirectTo(url, request)

        if request.args.get('button')[0] == 'Buy':
            propertyObject = db.query(Property).filter(Property.id == propertyId).first()
            
            propertyObject.units -= quantity

            status = 'open'

            timestamp = config.createTimestamp()
            
            total = quantity * float(propertyObject.pricePerUnit)
            order = Order(status, timestamp, timestamp, propertyId, propertyObject.title, quantity, propertyObject.pricePerUnit, investorId, total, '')
            #def __init__(self, status, createTimestamp, updateTimestamp, propertyId, propertyTitle, units, pricePerUnit, total, paymentAddress):

            db.add(order)
            db.commit()

            sessionOrder['id'] = order.id

            return redirectTo('../receipt', request)


class LendAmount(Resource):
    def render(self, request):
        if not request.args:
            return redirectTo('../', request)

        sessionUser = SessionManager(request).getSessionUser()
        investorId = sessionUser['id']

        #if sessionUser['type'] != 0:
        #    return redirectTo('../', request)

        sessionTransaction = SessionManager(request).getSessionTransaction()
        #propertyId = sessionOrder['propertyId']

        #url = '../summaryProperties?action=add'
        #url = str(url)

        amount = request.args.get('investmentAmount')[0]

        sessionTransaction['investorId'] = investorId
        sessionTransaction['amount'] = amount
        bitcoinAddress = 'XXXXX'

        #if error.propertyTitle(request, propertyTitle):
        #    return redirectTo(url, request)

        #if error.propertyDescription(request, propertyDescription):
        #    return redirectTo(url, request)

        #if not request.args.get('isTermsChecked'):
        #    SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.TERMS[0]})
        #    return redirectTo('../register', request)

        if request.args.get('button')[0] == 'Get Address':
            timestamp = config.createTimestamp()

            #def __init__(self, status, createTimestamp, updateTimestamp, userId, amount):
            transaction = Transaction('pending', timestamp, timestamp, investorId, amount, bitcoinAddress)
            
            db.add(newTransaction)
            db.commit()

            #url = '../verifyToken?id=%s&token=%s' % (str(newUser.id), token)

            #plain = mailer.verificationPlain(url)
            #html = mailer.verificationHtml(url)
            #Email(mailer.noreply, email, 'Getting Started', plain, html).send()

            #email = str(email)
            #activity.pushToSocket(self.echoFactory, '%s**** registered' % email[0])
            #activity.pushToDatabase('%s registered' % email)

            #functions.makeLogin(request, newUser.id)
            #return redirectTo('../settings', request)
            #propertyObject = db.query(Property).filter(Property.id == propertyId).first()
            #
            #propertyObject.units -= quantity

            #status = 'open'

            #timestamp = config.createTimestamp()
            #
            #total = quantity * float(propertyObject.pricePerUnit)
            #order = Order(status, timestamp, timestamp, propertyId, propertyObject.title, quantity, propertyObject.pricePerUnit, investorId, total, '')
            ##def __init__(self, status, createTimestamp, updateTimestamp, propertyId, propertyTitle, units, pricePerUnit, total, paymentAddress):

            #db.add(order)
            #db.commit()

            sessionTransaction['id'] = transaction.id

            return redirectTo('../receipt', request)
