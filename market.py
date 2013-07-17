from twisted.web.resource import Resource
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import db
from sessions import SessionManager
from sqlalchemy import func

#import reset
import commonElements
import config
import definitions
import functions
import json
import math
import notFound
import pages
import random
import sys
import collections
import property


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['page'] = 'market'

        try:
            status = request.args.get('status')[0]
        except:
            status = 'pending'

        Page = pages.Market('Market', 'market', status)
        Page.sessionUser = sessionUser

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        return renderElement(request, Page)


class Assets(Element):
    def __init__(self, status):
        self.status = status

        if self.status == 'pending':
            template = 'templates/elements/assets0.xml'

        if self.status == 'trading':
            template = 'templates/elements/assets1.xml'

        self.loader = XMLString(FilePath(template).getContent())
