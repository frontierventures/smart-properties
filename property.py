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
    isLeaf = True

    def __init__(self, propertyId):
        self.propertyId = propertyId

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).getSessionUser()
        userId = session_user['id']

        sessionResponse = SessionManager(request).getSessionResponse()

        try:
            action = request.args.get('action')[0]
        except:
            action = ''

        if not action:
            session_user['page'] = 'buyProperty'

            propertyObject = db.query(Property).filter(Property.id == self.propertyId).first()

            sessionOrder = SessionManager(request).getSessionOrder()
            sessionOrder['propertyId'] = self.propertyId

            if not sessionOrder.get('quantity'):
                sessionOrder['quantity'] = 1

            Page = pages.BuyProperty('Buy Property - %s' % str(propertyObject.title), 'buyProperty')
            Page.sessionResponse = sessionResponse
            Page.session_user = session_user
            Page.sessionOrder = sessionOrder


            print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
            print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
            print "%ssessionOrder: %s%s" % (config.color.BLUE, sessionOrder, config.color.ENDC)
            SessionManager(request).clearSessionResponse()
            request.write('<!DOCTYPE html>\n')
            return renderElement(request, Page)
