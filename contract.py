#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString

from sessions import SessionManager

import config
import pages


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['page'] = 'contract'

        sessionResponse = SessionManager(request).getSessionResponse()

        if sessionUser['id'] == 0:
            return redirectTo('../', request)

        sessionTransaction = SessionManager(request).getSessionTransaction()

        Page = pages.Contract('Smart Property Group - Contract', 'contract')
        Page.sessionUser = sessionUser
        Page.sessionResponse = sessionResponse
        Page.sessionTransaction = sessionTransaction

        print "%ssessionUser: %s%s" % (config.color.YELLOW, sessionUser, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.YELLOW, sessionResponse, config.color.ENDC)
        print "%ssessionTransaction: %s%s" % (config.color.YELLOW, sessionTransaction, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)
