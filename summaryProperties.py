#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, User, Property
from data import db
from sessions import SessionManager

import config
import json
import pages


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        userType = sessionUser['type']
        if userType != 0:
            return redirectTo('../', request)

        try:
            status = request.args.get('status')[0]
        except:
            status = 'active'

        Page = pages.SummaryProperties('Property Summary', 'summaryProperties', status)
        Page.sessionUser = sessionUser

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Properties(Element):
    def __init__(self, status):
        self.status = status
        users = db.query(User).order_by(User.loginTimestamp.desc())
        users = users.filter(User.status == status)

        if users.count() == 0:
            template = 'templates/elements/summaryUsers0.xml'
        else:
            template = 'templates/elements/summaryUsers1.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.users = users

    @renderer
    def count(self, request, tag):
        statuses = {'active': 'Active',
                    'deleted': 'Deleted'}
        slots = {}
        slots['htmlUserStatus'] = statuses[self.status]
        slots['htmlUserCount'] = str(self.users.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def userStatus(self, request, tag):
        statuses = ['active', 'deleted']

        for status in statuses:
            thisTagShouldBeSelected = False
            if status == self.status:
                thisTagShouldBeSelected = True
            slots = {}
            slots['inputValue'] = status
            slots['inputCaption'] = status
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag

    @renderer
    def row(self, request, tag):
        for user in self.users:
            timestamp = float(user.loginTimestamp)

            profile = db.query(Profile).filter(Profile.id == user.id).first()

            slots = {}
            slots['htmlUserId'] = str(user.id)
            slots['htmlUserTimestamp'] = config.convertTimestamp(timestamp)
            slots['htmlUserEmail'] = str(user.email)
            slots['htmlUserIp'] = str(user.ip)
            slots['htmlUserSeed'] = str(profile.seed)
            slots['htmlUserBitcoinAddress'] = str(profile.bitcoinAddress)
            self.user = user
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        actions = {}
        actions[config.createTimestamp()] = ['View', 'ticon view hint hint--top hint--rounded', '../describeUser']
        actions[config.createTimestamp()] = ['Delete', 'ticon delete hint hint--top hint--rounded', '../deleteUser?id=%s' % self.user.id]

        for key in sorted(actions.keys()):
            slots = {}
            slots['htmlId'] = str(self.user.id)
            slots['htmlHint'] = actions[key][0]
            slots['htmlClass'] = actions[key][1]
            slots['htmlUrl'] = actions[key][2]
            newTag = tag.clone().fillSlots(**slots)
            yield newTag


class Delete(Resource):
    def __init__(self, topProductCounter):
        self.topProductCounter = topProductCounter

    def render(self, request):
        sessionUser = SessionManager(request).getSessionUser()
        userType = sessionUser['type']
        if userType != 0:
            return redirectTo('../', request)

        if not request.args:
            return redirectTo('../', request)

        try:
            userId = request.args.get('id')
            userId = int(userId[0])
        except:
            return redirectTo('../', request)

        user = db.query(User).filter(User.id == userId).first()
        user.status = 'deleted'

        profile = db.query(Profile).filter(Profile.userId == userId).first()
        profile.status = 'deleted'

        db.commit()
        summaryStores.close(self.topProductCounter, userId)
        return redirectTo('../summaryProperties', request)
