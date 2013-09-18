from twisted.web.resource import Resource
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import db
from sessions import SessionManager
from sqlalchemy import func

#import reset
import elements
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
    topProductCounter = {}
    serverInfo = {"lastReset": 0, "visits": 0}

    def __init__(self, echoFactory):
        Resource.__init__(self)
        self.echoFactory = echoFactory
        self.serverInfo['lastReset'] = config.createTimestamp()

    def getChild(self, name, request):
        #storeDirectoryItem = db.query(StoreDirectory).filter(StoreDirectory.name == name).first()

        #if storeDirectoryItem:
        #    ownerId = storeDirectoryItem.ownerId
        return property.Main(name)
        #else:
        #    return notFound.Main(0)

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        session_user = SessionManager(request).getSessionUser()
        session_user['page'] = 'home'
        session_user['ip'] = request.getClientIP()

        if not session_user['seed']:
            self.serverInfo['visits'] += 1
            session_user['seed'] = random.randint(0, sys.maxint)

        Page = pages.Home('Welcome to Smart Property Group Website!', 'home')
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        return renderElement(request, Page)
