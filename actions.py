#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python .filepath import FilePath
from parsley import makeGrammar
from twisted.web.template import XMLString, Element, renderer, tags

from data import db
from data import Order, Profile, Property, Transaction, User
from sqlalchemy import func
from sessions import SessionManager

import activity
import cgi
import elements
import encryptor
import config
import decimal
import definitions
import error
import explorer
import receipt
import functions
import hashlib
import inspect
import itertools
import login
import mailer
import os
import random
import sys

D = decimal.Decimal
Email = mailer.Email


#FORM ACTIONS
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


class Invest(Resource):
    def render(self, request):
        if not request.args:
            return redirectTo('../', request)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['action'] = 'invest'

        investorId = sessionUser['id']

        sessionTransaction = SessionManager(request).getSessionTransaction()

        amount = request.args.get('investmentAmountFiat')[0]

        sessionTransaction['investorId'] = investorId
        sessionTransaction['amount'] = amount
        bitcoinAddress = explorer.getNewAddress('')['result']

        if error.amount(request, amount):
            return redirectTo('../invest', request)

        amount = float(amount)

        if request.args.get('button')[0] == 'Get Address':
            timestamp = config.createTimestamp()

            transaction = Transaction('open', timestamp, timestamp, investorId, amount, bitcoinAddress, 0)
            
            db.add(transaction)

            db.commit()

            sessionTransaction['id'] = transaction.id
            sessionTransaction['amount'] = transaction.amount
            sessionTransaction['bitcoinAddress'] = transaction.bitcoinAddress
            sessionTransaction['isSigned'] = 0 

            return redirectTo('../contract', request)


class Login(Resource):
    def __init__(self, echoFactory):
        self.echoFactory = echoFactory

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['action'] = 'login'

        userEmail = request.args.get('userEmail')[0]
        userPassword = request.args.get('userPassword')[0]

        sessionUser['email'] = userEmail
        sessionUser['password'] = userPassword

        if error.email(request, userEmail):
            return redirectTo('../login', request)

        if error.password(request, userPassword):
            return redirectTo('../login', request)

        users = db.query(User).filter(User.email == userEmail)
        user = users.filter(User.status != 'deleted').first()
        if not user:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[2]})
            return redirectTo('../login', request)
        
        if not encryptor.checkPassword(user.password, userPassword):
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD[2]})
            return redirectTo('../login', request)

        if request.args.get('button')[0] == 'Login':
            url = '../account'
            if user.type == 0:
                url = '../summaryTransactions'

            if user.isEmailVerified == 1:
                isEmailVerified = True
            else:
                isEmailVerified = False

            #if not isEmailVerified:
            #    url = '../settings'

            login.makeSession(request, user.id)

            email = str(user.email)

            activity.pushToSocket(self.echoFactory, '%s**** logged in' % email[0])
            activity.pushToDatabase('%s logged in' % email)

            url = str(url)
            return redirectTo(url, request)


class Register(Resource):
    def __init__(self, echoFactory):
        self.echoFactory = echoFactory

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../register', request)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['action'] = 'register'

        email = request.args.get('userEmail')[0]
        password = request.args.get('userPassword')[0]
        repeatPassword = request.args.get('userRepeatPassword')[0]

        sessionUser['email'] = email
        sessionUser['password'] = password
        sessionUser['repeatPassword'] = repeatPassword

        if error.email(request, email):
            return redirectTo('../register', request)

        users = db.query(User).filter(User.status == 'active')
        user = users.filter(User.email == email).first()

        if user:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[3]})
            return redirectTo('../register', request)

        if error.password(request, password):
            return redirectTo('../register', request)

        if error.repeatPassword(request, repeatPassword):
            return redirectTo('../register', request)

        if error.mismatchPassword(request, password, repeatPassword):
            return redirectTo('../register', request)

        if not request.args.get('isTermsChecked'):
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.TERMS[0]})
            return redirectTo('../register', request)

        if request.args.get('button')[0] == 'Register':
            timestamp = config.createTimestamp()
            token = hashlib.sha224(str(email)).hexdigest()

            password = encryptor.hashPassword(password)
            newUser = User('unverified', 2, timestamp, email, password, 0, '')
            
            seed = random.randint(0, sys.maxint)
            newProfile = Profile(timestamp, timestamp, '', '', token, '', seed, 0, 0)
            newUser.profiles = [newProfile]

            db.add(newUser)
            db.commit()

            plain = mailer.verificationPlain(seed)
            html = mailer.verificationHtml(seed)
            Email(mailer.noreply, email, 'Getting Started', plain, html).send()

            email = str(email)
            activity.pushToSocket(self.echoFactory, '%s**** registered' % email[0])
            activity.pushToDatabase('%s registered' % email)

            login.makeSession(request, newUser.id)
            return redirectTo('../account', request)


class SignContract(Resource):
    def render(self, request):
        if not request.args:
            return redirectTo('../', request)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['action'] = 'signContract'
        investorId = sessionUser['id']

        sessionTransaction = SessionManager(request).getSessionTransaction()
        transactionId = sessionTransaction['id']

        signature = request.args.get('contractSignature')[0]

        if error.signature(request, signature):
            return redirectTo('../contract', request)

        if request.args.get('button')[0] == 'Sign Contract':
            timestamp = config.createTimestamp()
            
            transaction = db.query(Transaction).filter(Transaction.id == transactionId).first()

            transaction.updateTimestamp = timestamp
            transaction.isSigned = 1
            db.commit()
        
            user = db.query(User).filter(User.id == transaction.userId).first()
            plain = mailer.transactionPendingMemoPlain(transaction)
            html = mailer.transactionPendingMemoHtml(transaction)
            Email(mailer.noreply, user.email, 'Your have a pending Smart Property Group transaction!', plain, html).send()
            Email(mailer.noreply, 'transactions@sptrust.co', 'Your have a pending Smart Property Group transaction!', plain, html).send()

            sessionTransaction['isSigned'] = transaction.isSigned

            return redirectTo('../receipt', request)


class ValidateBitcoinAddress(Resource):
    def __init__(self, echoFactory):
        self.echoFactory = echoFactory

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../settings', request)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['action'] = 'validateOwnership'

        nonce = request.args.get('userNonce')[0]
        bitcoinAddress = request.args.get('userBitcoinAddress')[0]
        signature = request.args.get('userSignature')[0]

        sessionUser['userNonce'] = nonce
        sessionUser['userBitcoinAddress'] = bitcoinAddress
        sessionUser['userSignature'] = signature

        if error.bitcoinAddress(request, bitcoinAddress):
            return redirectTo('../signature', request)

        #if error.signature(request, signature):
        #    return redirectTo('../signature', request)

        print explorer.summary()
        
        output = explorer.verifyMessage(bitcoinAddress, signature, nonce)
        print output
        print output['error']

        if output['error']:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': output['error']['message']})
        else:
            if output['result']:
                timestamp = config.createTimestamp()

                user = db.query(User).filter(User.id == sessionUser['id']).first()
                user.status = 'verified'

                profile = db.query(Profile).filter(Profile.id == sessionUser['id']).first()
                profile.updateTimestamp = timestamp
                profile.bitcoinAddress = bitcoinAddress
                
                db.commit()
                sessionUser['status'] = 'verified'
            else:
                SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.SIGNATURE[2]})

        return redirectTo('../account', request)


#POST ACTIONS
class UpdateTransaction(Resource):
    def render(self, request):
        sessionUser = SessionManager(request).getSessionUser()

        if sessionUser['type'] != 0:
            return redirectTo('../', request)

        if not request.args:
            return redirectTo('../', request)

        try:
            transactionId = request.args.get('id')[0]
            transactionStatus = request.args.get('status')[0]
        except:
            return redirectTo('../summaryTransactions', request)
        

        transaction = db.query(Transaction).filter(Transaction.id == transactionId).first()
        transaction.status = transactionStatus 
        transaction.updateTimestamp = config.createTimestamp()
        
        investor = db.query(Profile).filter(Profile.id == transaction.userId).first()
        investor.balance = float(investor.balance) + float(transaction.amount)

        solicitor = db.query(Profile).filter(Profile.id == 1).first()
        solicitor.balance = float(solicitor.balance) - float(transaction.amount)

        db.commit()

        user = db.query(User).filter(User.id == transaction.userId).first()
        
        if transactionStatus == 'complete':
            plain = mailer.transactionApprovalMemoPlain(transaction)
            html = mailer.transactionApprovalMemoHtml(transaction)
            Email(mailer.noreply, user.email, 'Your Smart Property Group transaction was marked complete!', plain, html).send()

        if transactionStatus == 'canceled':
            plain = mailer.transactionCancelationMemoPlain(transaction)
            html = mailer.transactionCancelationMemoHtml(transaction)
            Email(mailer.noreply, user.email, 'Your Smart Property Group transaction was canceled!', plain, html).send()

        return redirectTo('../summaryTransactions', request)
