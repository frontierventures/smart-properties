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
        sessionUser['page'] = 'legal'

        Page = pages.FAQ('FAQ', 'faq')
        Page.sessionUser = sessionUser

        print "%ssessionUser: %s%s" % (config.color.YELLOW, sessionUser, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)
