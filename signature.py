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

        session_user = SessionManager(request).getSessionUser()
        session_user['page'] = 'signature'

        if session_user['id'] == 0:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()

        Page = pages.Signature('Smart Property Group - Signature', 'signature')
        Page.session_user = session_user
        Page.sessionResponse = sessionResponse

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)
