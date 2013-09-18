#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, User
from data import db
from sessions import SessionManager
from sqlalchemy import not_

import config
import json
import pages


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).getSessionUser()
        userType = session_user['type']
        if userType != 0:
            return redirectTo('../', request)

        try:
            status = request.args.get('status')[0]
        except:
            status = 'verified'

        filters = {'status': status}

        Page = pages.SummaryUsers('User Summary', 'summaryUsers', filters)
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.YELLOW, session_user, config.color.ENDC)
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Users(Element):
    def __init__(self, filters):
        self.status = filters['status']

        users = db.query(User)
        if self.status == 'verified':
            users = users.filter(User.status == 'verified').order_by(User.loginTimestamp.desc())
        elif self.status == 'deleted':
            users = users.filter(User.status == 'deleted').order_by(User.loginTimestamp.desc())
        else: 
            users = users.filter(not_(User.status.in_(['verified', 'deleted']))).order_by(User.loginTimestamp.desc())


        if users.count() == 0:
            template = 'templates/elements/summaryUsers0.xml'
        else:
            template = 'templates/elements/summaryUsers1.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.users = users

    @renderer
    def count(self, request, tag):
        statuses = {'verified': 'Verified',
                    'unverified': 'Unverified',
                    'deleted': 'Deleted'}
        slots = {}
        slots['htmlUserStatus'] = statuses[self.status]
        slots['htmlUserCount'] = str(self.users.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def userStatus(self, request, tag):
        statuses = ['verified', 'unverified', 'deleted']

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
            slots['htmlUserShares'] = str(profile.balance)
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
    def __initdads__(self, topProductCounter):
        self.topProductCounter = topProductCounter

    def render(self, request):
        session_user = SessionManager(request).getSessionUser()
        userType = session_user['type']
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
        return redirectTo('../summaryUsers', request)


class LoadUser(Resource):
    def render(self, request):

        session_user = SessionManager(request).getSessionUser()
        userType = session_user['type']
        if userType != 0:
            return redirectTo('../', request)

        try:
            userId = int(request.args.get('id')[0])
        except:
            return redirectTo('../', request)

        profile = db.query(Profile).filter(Profile.userId == userId).first()
        user = db.query(User).filter(User.id == userId).first()
        store = db.query(Store).filter(Store.ownerId == userId).first()

        jsonUser = {}
        jsonUser['id'] = str(userId)
        jsonUser['email'] = str(user.email)
        jsonUser['first'] = str(profile.first)
        jsonUser['last'] = str(profile.last)
        jsonUser['currencyId'] = str(profile.currencyId)
        jsonUser['unreadCount'] = str(profile.unreadCount)
        jsonUser['bitcoinAddress'] = str(profile.bitcoinAddress)
        jsonUser['type'] = str(user.type)
        jsonUser['loginTimestamp'] = str(user.loginTimestamp)
        jsonUser['isEmailVerified'] = str(user.isEmailVerified)
        jsonUser['createTimestamp'] = str(profile.createTimestamp)
        jsonUser['updateTimestamp'] = str(profile.updateTimestamp)
        jsonUser['receivedSellOrders'] = str(profile.receivedSellOrders)
        jsonUser['receivedBuyOrders'] = str(profile.receivedBuyOrders)
        jsonUser['ip'] = str(user.ip)
        jsonUser['store'] = str(store.name)
        return json.dumps(jsonUser)


from datetime import datetime
import collections


def convert(timestamp):
    utc = datetime.utcfromtimestamp(timestamp)
    format = "%Y %b %e"
    return utc.strftime(format)


class LoadUserSummary(Resource):
    def render(self, request):

        request.setHeader('Access-Control-Allow-Origin', '*')
        users = db.query(User.loginTimestamp).distinct()
        timestamps = [user.loginTimestamp for user in users]
        dates = [convert(float(timestamp)) for timestamp in timestamps]
        dateCounter = collections.Counter(dates)
        print dates, dateCounter

        sessionData = []
        for key in sorted(dateCounter.keys()):
            sessionData.append({"letter": key, "frequency": dateCounter[key]})
            print key
        return json.dumps(sessionData)
