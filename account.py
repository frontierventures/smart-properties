#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString

from sessions import SessionManager

import config
import pages

from data import db
from sqlalchemy.sql import and_
from data import Profile
from sessions import SessionManager


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['page'] = 'account'

        if sessionUser['id'] == 0:
            return redirectTo('../', request)

        Page = pages.Account('Smart Property Group - Account', 'account')
        Page.sessionUser = sessionUser

        print "%ssessionUser: %s%s" % (config.color.YELLOW, sessionUser, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Details(Element):
    def __init__(self, sessionUser):
        self.sessionUser = sessionUser

        self.profile = db.query(Profile).filter(Profile.id == sessionUser['id']).first()
        template = 'templates/elements/account0.xml'

        self.loader = XMLString(FilePath(template).getContent())

    @renderer
    def details(self, request, tag):
        slots = {}
        slots['htmlInvestedBalance'] = str(self.profile.balance) 
        slots['htmlNextPaymentDate'] = str(config.convertTimestamp(float(config.createTimestamp())))
        slots['htmlReturnRate'] = str('0.85%') 
        yield tag.clone().fillSlots(**slots)