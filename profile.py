#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import db
from sqlalchemy.sql import and_
from data import Profile
from sessions import SessionManager

import config
import definitions
import functions
import pages


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        if sessionUser['id'] == 0:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()

        sessionUser['page'] = 'profile'

        Page = pages.Profile('Profile', 'profile')
        Page.sessionResponse = sessionResponse
        Page.sessionUser = sessionUser

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
        SessionManager(request).clearSessionResponse()
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Details(Element):
    def __init__(self, sessionUser):
        self.sessionUser = sessionUser

        self.profile = db.query(Profile).filter(Profile.id == sessionUser['id']).first()
        template = 'templates/elements/profile0.xml'

        self.loader = XMLString(FilePath(template).getContent())

    @renderer
    def details(self, request, tag):
        slots = {}
        slots['htmlFirst'] = str(self.profile.first)
        slots['htmlLast'] = str(self.profile.last) 
        slots['htmlBitcoinAddress'] = str(self.profile.bitcoinAddress) 
        slots['htmlShares'] = str(self.profile.shares) 
        yield tag.clone().fillSlots(**slots)
