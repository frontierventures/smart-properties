#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Profile, User, Order
from data import db
from sessions import SessionManager

import config
import json
import forms
import pages


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).getSessionUser()

        if session_user['id'] == 0:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()
        sessionProperty = SessionManager(request).getSessionProperty()

        try:
            status = request.args.get('status')[0]
        except:
            status = 'pending'

        Page = pages.Orders('Orders', 'orders', status)
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "%ssessionProperty: %s%s" % (config.color.BLUE, sessionProperty, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.BLUE, sessionResponse, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Orders(Element):
    def __init__(self, session_user, status):
        self.session_user = session_user
        self.status = status

        orders = db.query(Order).filter(Order.lenderId == session_user['id'])
        if status == 'pending':
            orders = orders.filter(Order.status.in_(['open', 'paid'])).order_by(Order.updateTimestamp.desc())
        if status == 'canceled':
            orders = orders.filter(Order.status == 'canceled').order_by(Order.updateTimestamp.desc())
        if status == 'complete':
            orders = orders.filter(Order.status == 'received').order_by(Order.updateTimestamp.desc())

        if orders.count() == 0:
            template = 'templates/elements/orders0.xml'
        else:
            template = 'templates/elements/orders1.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.orders = orders

    @renderer
    def count(self, request, tag):
        statuses = {'pending': 'Pending',
                    'canceled': 'Canceled',
                    'complete': 'Complete'}

        slots = {}
        slots['htmlOrderStatus'] = statuses[self.status]
        slots['htmlOrderCount'] = str(self.orders.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def orderStatus(self, request, tag):
        statuses = {'pending': 'Pending',
                    'canceled': 'Canceled',
                    'complete': 'Complete'}

        for key in statuses:
            thisTagShouldBeSelected = False

            if key == self.status:
                thisTagShouldBeSelected = True

            slots = {}
            slots['inputValue'] = key
            slots['inputCaption'] = statuses[key]
            newTag = tag.clone().fillSlots(**slots)

            if thisTagShouldBeSelected:
                newTag(selected='yes')
            yield newTag

    @renderer
    def row(self, request, tag):
        for order in self.orders:
            timestamp = float(order.createTimestamp)

            slots = {}
            slots['htmlOrderId'] = str(order.id)
            slots['htmlTimestamp'] = config.convertTimestamp(timestamp)
            slots['htmlTitle'] = str(order.propertyTitle) 
            slots['htmlUnits'] = str(order.units) 
            slots['htmlPricePerUnit'] = str(order.pricePerUnit) 
            slots['htmlTotal'] = str(order.total) 
            self.order = order
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        actions = {}
        actions[config.createTimestamp()] = ['View', 'ticon view hint hint--top hint--rounded', '../describeProperty']
        actions[config.createTimestamp()] = ['Delete', 'ticon delete hint hint--top hint--rounded', '../deleteProperty?id=%s' % self.order.id]

        for key in sorted(actions.keys()):
            slots = {}
            slots['htmlId'] = str(self.order.id)
            slots['htmlHint'] = actions[key][0]
            slots['htmlClass'] = actions[key][1]
            slots['htmlUrl'] = actions[key][2]
            newTag = tag.clone().fillSlots(**slots)
            yield newTag
