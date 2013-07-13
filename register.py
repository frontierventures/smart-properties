#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import flattenString
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, User
from data import db
from sessions import SessionManager


import activity
import elements
import config
import definitions
import encryptor
import error
import functions
import hashlib
import inspect
import json
import mailer
import os
import pages
import re

Email = mailer.Email


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['page'] = 'register'

        userId = sessionUser['id']
        if userId >= 1:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()

        Page = pages.Register('Register', 'register')
        Page.sessionUser = sessionUser
        Page.sessionResponse = sessionResponse

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Form(Element):
    loader = XMLString(FilePath('templates/forms/register.xml').getContent())

    def __init__(self, sessionUser, sessionResponse):
        self.sessionUser = sessionUser
        self.sessionResponse = sessionResponse

    @renderer
    def form(self, request, tag):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        sessionUser = self.sessionUser
        sellerEmail = ''
        if sessionUser.get('sellerEmail'):
            sellerEmail = sessionUser['sellerEmail']

        sellerPassword = ''
        if sessionUser.get('sellerPassword'):
            sellerPassword = sessionUser['sellerPassword']

        sellerPasswordRepeat = ''
        if sessionUser.get('sellerPasswordRepeat'):
            sellerPasswordRepeat = sessionUser['sellerPasswordRepeat']

        sellerStorename = ''
        if sessionUser.get('sellerStorename'):
            sellerStorename = sessionUser['sellerStorename']

        sellerBitcoinAddress = ''
        if sessionUser.get('sellerBitcoinAddress'):
            sellerBitcoinAddress = sessionUser['sellerBitcoinAddress']

        slots = {}
        slots['htmlEmail'] = sellerEmail
        slots['htmlPassword'] = sellerPassword
        slots['htmlRepeatPassword'] = sellerPasswordRepeat
        slots['htmlStorename'] = sellerStorename
        slots['htmlBitcoinAddress'] = sellerBitcoinAddress
        yield tag.fillSlots(**slots)

    @renderer
    def currency(self, request, tag):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        sessionUser = self.sessionUser

        sellerCurrencyId = 'USD'
        if sessionUser.get('sellerCurrencyId'):
            sellerCurrencyId = sessionUser['sellerCurrencyId']

        for currency in definitions.currencies:
            thisTagShouldBeSelected = False
            if currency == sellerCurrencyId:
                thisTagShouldBeSelected = True
            slots = {}
            slots['inputValue'] = currency
            slots['inputCaption'] = currency
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='')
            yield newTag

    @renderer
    def notification(self, request, tag):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)
        sessionResponse = self.sessionResponse
        if not sessionResponse['text']:
            return []
        else:
            return commonElements.Notification(sessionResponse)


class Save(Resource):
    def __init__(self, echoFactory):
        self.echoFactory = echoFactory

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../seller', request)

        email = request.args.get('sellerEmail')[0]
        password = request.args.get('sellerPassword')[0]
        repeatPassword = request.args.get('sellerPasswordRepeat')[0]
        storeName = request.args.get('sellerStorename')[0]
        bitcoinAddress = request.args.get('sellerBitcoinAddress')[0]
        currencyId = request.args.get('sellerCurrencyId')[0]

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['sellerEmail'] = email
        sessionUser['sellerPassword'] = password
        sessionUser['sellerPasswordRepeat'] = repeatPassword
        sessionUser['sellerStorename'] = storeName
        sessionUser['sellerCurrencyId'] = currencyId
        sessionUser['sellerBitcoinAddress'] = bitcoinAddress

        if error.email(request, email):
            return redirectTo('../seller', request)

        users = db.query(User).filter(User.status == 'active')
        user = users.filter(User.email == email).first()
        if user:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[3]})
            return redirectTo('../seller', request)

        if error.password(request, password):
            return redirectTo('../seller', request)

        if error.repeatPassword(request, repeatPassword):
            return redirectTo('../seller', request)

        if error.mismatchPassword(request, password, repeatPassword):
            return redirectTo('../seller', request)

        if error.storeName(request, storeName):
            return redirectTo('../seller', request)

        storeDirectory = db.query(StoreDirectory).filter(StoreDirectory.name == storeName).first()
        if storeDirectory:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.STORE_NAME[3]})
            return redirectTo('../seller', request)

        if error.bitcoinAddress(request, bitcoinAddress):
            return redirectTo('../seller', request)

        if not request.args.get('isTermsChecked'):
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.TERMS[0]})
            return redirectTo('../seller', request)

        if request.args.get('button')[0] == 'Register':
            timestamp = config.createTimestamp()
            token = hashlib.sha224(str(email)).hexdigest()

            password = encryptor.hashPassword(password)
            newUser = User("active", 2, timestamp, email, password, 0, '')
            newProfile = Profile(timestamp, timestamp, '', '', token, currencyId, bitcoinAddress, 0, 0, 0, 0, 0)
            newUser.profiles = [newProfile]
            newUser.stores = [Store("closed", timestamp, timestamp, 0, 0, newUser.id, storeName, '', '', 186, '', '', '', 1)]
            newUser.storeDirectory = [StoreDirectory(storeName)]

            db.add(newUser)
            db.commit()

            path = 'images/products/%s' % newUser.id 
            if not os.path.exists(path):
                os.makedirs(path)
                print "%s%s created%s" % (config.color.BLUE, path, config.color.ENDC)

            url = 'http://www.coingig.com/verifyToken?id=%s&token=%s' % (str(newUser.id), token)

            plain = mailer.verificationPlain(url)
            html = mailer.verificationHtml(url)
            Email(mailer.noreply, email, 'Getting Started with Coingig', plain, html).send()

            email = str(email)
            activityLog.pushToSocket(self.echoFactory, '%s**** registered as seller' % email[0])
            activityLog.pushToDatabase('%s registered as seller' % email)

            functions.makeLogin(request, newUser.id)
            return redirectTo('../settings', request)


class SaveSellerInfo(Resource):
    def render(self, request):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../seller', request)

        storeName = request.args.get('sellerStorename')[0]
        sellerBitcoinAddress = request.args.get('sellerBitcoinAddress')[0]
        sellerCurrencyId = request.args.get('sellerCurrencyId')[0]

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['sellerStorename'] = storeName
        sessionUser['sellerCurrencyId'] = sellerCurrencyId
        sessionUser['sellerBitcoinAddress'] = sellerBitcoinAddress
        #SessionManager(request).setSessionUser(sessionUser)

        sellerId = sessionUser['id']
        #storename = str(directoryData.get_By_Id(sellerId)['storename'])
        #url = '../%s' % storename

        if not storeName:
            return json.dumps(dict(response=0, text=definitions.STORE_NAME[0]))
        elif not re.match(definitions.REGEX_STORENAME, storeName):
            return json.dumps(dict(response=0, text=definitions.STORE_NAME[1]))

        if storeName in definitions.restrictedStoreNames:
            return json.dumps(dict(response=0, text=definitions.STORE_NAME[2]))

        if not sellerBitcoinAddress:
            return json.dumps(dict(response=0, text=definitions.BITCOIN_ADDRESS[0]))
        elif not re.match(definitions.REGEX_BITCOIN_ADDRESS, sellerBitcoinAddress):
            return json.dumps(dict(response=0, text=definitions.BITCOIN_ADDRESS[1]))

        profile = db.query(Profile).filter(Profile.userId == sellerId).first()
        profile.bitcoingAddress = sellerBitcoinAddress
        profile.currencyId = sellerCurrencyId

        user = db.query(User).filter(User.id == sellerId).first()
        user.type = 2

        timestamp = config.createTimestamp()
        store = db.query(Store).filter(Store.ownerId == sellerId).first()
        store.updateTimestamp = timestamp
        store.name = storeName

        storeDirectoryItem = db.query(StoreDirectory).filter(StoreDirectory.ownerId == sellerId).first()
        storeDirectoryItem.name = storeName

        db.commit()
        sessionUser['type'] = 2
        return json.dumps(dict(response=1, text=definitions.UPDATE_SUCCESS))
