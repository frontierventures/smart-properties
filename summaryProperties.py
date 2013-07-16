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
import forms
import pages


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        userType = sessionUser['type']

        if userType != 0:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()
        sessionProperty = SessionManager(request).getSessionProperty()

        try:
            status = request.args.get('status')[0]
        except:
            status = 'available'

        try:
            action = request.args.get('action')[0]
        except:
            action = ''

        if not action:
            Page = pages.SummaryProperties('Property Summary', 'summaryProperties', status)
            Page.sessionUser = sessionUser
            print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)

        if action == 'add':
            Page = pages.AddProperty('Add Property', 'addProperty')
            Page.sessionUser = sessionUser
            Page.sessionResponse = sessionResponse
            Page.sessionProperty = sessionProperty

            print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
            print "%ssessionProperty: %s%s" % (config.color.BLUE, sessionProperty, config.color.ENDC)
            print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
            SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Properties(Element):
    def __init__(self, status):
        self.status = status
        properties = db.query(Property).order_by(Property.createTimestamp.desc())
        properties = properties.filter(Property.status == status)

        if properties.count() == 0:
            template = 'templates/elements/summaryProperties0.xml'
        else:
            template = 'templates/elements/summaryProperties1.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.properties = properties

    @renderer
    def count(self, request, tag):
        statuses = {'available': 'Active',
                    'deleted': 'Deleted'}
        slots = {}
        slots['htmlPropertyStatus'] = statuses[self.status]
        slots['htmlPropertyCount'] = str(self.properties.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def propertyStatus(self, request, tag):
        statuses = ['available', 'deleted']

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
        for property in self.properties:
            timestamp = float(property.createTimestamp)

            slots = {}
            slots['htmlPropertyId'] = str(property.id)
            slots['htmlTimestamp'] = config.convertTimestamp(timestamp)
            slots['htmlTitle'] = str(property.title)
            slots['htmlPropertyUrl'] = '../%s' % str(property.id)
            slots['htmlDownpaymentFiat'] = str(property.downpayment)
            slots['htmlUnits'] = str(property.units)
            slots['htmlPricePerUnitFiat'] = str(float(property.downpayment) / float(property.units))
            slots['htmlPricePerUnitBTC'] = str(float(property.downpayment) / float(property.units))
            self.property = property
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        actions = {}
        actions[config.createTimestamp()] = ['View', 'ticon view hint hint--top hint--rounded', '../describeProperty']
        actions[config.createTimestamp()] = ['Delete', 'ticon delete hint hint--top hint--rounded', '../deleteProperty?id=%s' % self.property.id]

        for key in sorted(actions.keys()):
            slots = {}
            slots['htmlId'] = str(self.property.id)
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
