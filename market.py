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


class Main(Resource):
    topProductCounter = {}
    serverInfo = {"lastReset": 0, "visits": 0}

    def __init__(self, echoFactory):
        Resource.__init__(self)
        self.echoFactory = echoFactory
        self.serverInfo['lastReset'] = config.createTimestamp()

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['page'] = 'home'
        sessionUser['ip'] = request.getClientIP()

        if not sessionUser['seed']:
            self.serverInfo['visits'] += 1
            sessionUser['seed'] = random.randint(0, sys.maxint)

        Page = pages.Home('Home', 'home')
        Page.sessionUser = sessionUser

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        return renderElement(request, Page)
