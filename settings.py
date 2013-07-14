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
import random
import re
import sys

Email = mailer.Email


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['page'] = 'settings'

        if sessionUser['id'] == 0:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()

        Page = pages.Settings('Settings', 'settings')
        Page.sessionUser = sessionUser
        Page.sessionResponse = sessionResponse

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Form(Element):
    loader = XMLString(FilePath('templates/forms/settings.xml').getContent())

    def __init__(self, sessionUser, sessionResponse):
        self.sessionUser = sessionUser
        self.sessionResponse = sessionResponse
        self.profile = db.query(Profile).order_by(Profile.id == sessionUser['id']).first()

    @renderer
    def form(self, request, tag):
        sessionUser = self.sessionUser

        userBitcoinAddress = ''
        if sessionUser.get('userBitcoinAddress'):
            userBitcoinAddress = sessionUser['userBitcoinAddress']

        userSignature = ''
        if sessionUser.get('userSignature'):
            userSignature = sessionUser['userSignature']

        slots = {}
        slots['htmlNonce'] = self.profile.seed
        slots['htmlBitcoinAddress'] = userBitcoinAddress
        slots['htmlSignature'] = userSignature
        yield tag.fillSlots(**slots)

    @renderer
    def notification(self, request, tag):
        sessionResponse = self.sessionResponse
        if not sessionResponse['text']:
            return []
        else:
            return commonElements.Notification(sessionResponse)


class Action(Resource):
    def __init__(self, echoFactory):
        self.echoFactory = echoFactory

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../register', request)

        email = request.args.get('userEmail')[0]
        password = request.args.get('userPassword')[0]
        repeatPassword = request.args.get('userRepeatPassword')[0]
        bitcoinAddress = request.args.get('userBitcoinAddress')[0]

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['userEmail'] = email
        sessionUser['userPassword'] = password
        sessionUser['userRepeatPassword'] = repeatPassword
        sessionUser['userBitcoinAddress'] = bitcoinAddress

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

        if error.bitcoinAddress(request, bitcoinAddress):
            return redirectTo('../register', request)

        if not request.args.get('isTermsChecked'):
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.TERMS[0]})
            return redirectTo('../register', request)

        if request.args.get('button')[0] == 'Register':
            timestamp = config.createTimestamp()
            token = hashlib.sha224(str(email)).hexdigest()

            password = encryptor.hashPassword(password)
            newUser = User("active", 2, timestamp, email, password, 0, '')
            
            seed = random.randint(0, sys.maxint)
            newProfile = Profile(timestamp, timestamp, '', '', token, bitcoinAddress, seed, 0)
            newUser.profiles = [newProfile]

            db.add(newUser)
            db.commit()

            url = '../verifyToken?id=%s&token=%s' % (str(newUser.id), token)

            plain = mailer.verificationPlain(url)
            html = mailer.verificationHtml(url)
            Email(mailer.noreply, email, 'Getting Started', plain, html).send()

            email = str(email)
            activity.pushToSocket(self.echoFactory, '%s**** registered' % email[0])
            activity.pushToDatabase('%s registered' % email)

            functions.makeLogin(request, newUser.id)
            #return redirectTo('../settings', request)
            return redirectTo('../', request)
