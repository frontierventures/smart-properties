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
        sessionUser['page'] = 'register'

        if sessionUser['id'] >= 1:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()

        Page = pages.Register('Register', 'register')
        Page.sessionUser = sessionUser
        Page.sessionResponse = sessionResponse

        print "%ssessionUser: %s%s" % (config.color.YELLOW, sessionUser, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.YELLOW, sessionResponse, config.color.ENDC)

        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Form(Element):
    loader = XMLString(FilePath('templates/forms/register.xml').getContent())

    def __init__(self, sessionUser, sessionResponse):
        self.sessionUser = sessionUser
        self.sessionResponse = sessionResponse
        print 
        print sessionUser

    @renderer
    def form(self, request, tag):
        sessionUser = self.sessionUser

        userEmail = ''
        if sessionUser.get('email'):
            userEmail = sessionUser['email']

        userPassword = ''
        if sessionUser.get('password'):
            userPassword = sessionUser['password']

        userRepeatPassword = ''
        if sessionUser.get('repeatPassword'):
            userRepeatPassword = sessionUser['repeatPassword']

        slots = {}
        slots['htmlEmail'] = userEmail
        slots['htmlPassword'] = userPassword
        slots['htmlRepeatPassword'] = userRepeatPassword
        yield tag.fillSlots(**slots)

    @renderer
    def alert(self, request, tag):
        sessionResponse = self.sessionResponse
        if sessionResponse['text']:
            return elements.Alert(sessionResponse)
        else:
            return []
