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


class Action(Resource):
    def __init__(self, echoFactory):
        self.echoFactory = echoFactory

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../settings', request)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['action'] = 'saveSettings'

        bitcoinAddress = request.args.get('userBitcoinAddress')[0]

        sessionUser['userBitcoinAddress'] = bitcoinAddress

        if error.bitcoinAddress(request, bitcoinAddress):
            return redirectTo('../settings', request)

        if request.args.get('button')[0] == 'Verify':
            timestamp = config.createTimestamp()

            profile = db.query(Profile).filter(Profile.id == sessionUser['id']).first()
            profile.bitcoinAddress = bitcoinAddress

            db.commit()
            return redirectTo('../account', request)
