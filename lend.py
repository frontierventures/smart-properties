#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import db
from sqlalchemy.sql import and_
from data import Property
from sessions import SessionManager

import config
import definitions
import functions
import pages


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).getSessionUser()

        if session_user['id'] == 0:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()

        session_user['page'] = 'lend'

        sessionTransaction = SessionManager(request).getSessionTransaction()

        if not sessionTransaction.get('amount'):
            sessionTransaction['amount'] = 1

        session_user['page'] = 'lend'

        Page = pages.Lend('Smart Property Group - Lend', 'lend')
        Page.session_user = session_user
        Page.sessionResponse = sessionResponse
        Page.sessionTransaction = sessionTransaction

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
        print "%ssessionTransaction: %s%s" % (config.color.BLUE, sessionTransaction, config.color.ENDC)

        SessionManager(request).clearSessionResponse()
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)
