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
import explorer
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
        self.profile = db.query(Profile).filter(Profile.id == sessionUser['id']).first()

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
            return redirectTo('../settings', request)

        bitcoinAddress = request.args.get('userBitcoinAddress')[0]
        signature = request.args.get('userSignature')[0]

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['userBitcoinAddress'] = bitcoinAddress
        sessionUser['userSignature'] = signature

        if error.bitcoinAddress(request, bitcoinAddress):
            return redirectTo('../settings', request)

        if error.signature(request, signature):
            return redirectTo('../settings', request)

        if request.args.get('button')[0] == 'Verify':
            timestamp = config.createTimestamp()

            profile = db.query(Profile).filter(Profile.id == sessionUser['id']).first()
            print explorer.summary()
            print explorer.verifyMessage(bitcoinAddress, signature, profile.seed)
            return redirectTo('../', request)
