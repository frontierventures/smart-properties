from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Price, Property 
from data import db
from sessions import SessionManager
from sqlalchemy import func

#import reset
import locale
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
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        session_user = SessionManager(request).getSessionUser()
        session_user['page'] = 'market'

        if session_user['id'] == 0:
            return redirectTo('../', request)

        try:
            status = request.args.get('status')[0]
        except:
            status = 'pending'

        Page = pages.Assets('Assets', 'assets', status)
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        return renderElement(request, Page)
    

class Assets(Element):
    def __init__(self, status):
        self.status = status

        assets = db.query(Property)

        if status == 'pending':
            assets = assets.filter(Property.status == 'pending').order_by(Property.updateTimestamp.desc())
        if status == 'closed':
            assets = assets.filter(Property.status == 'closed').order_by(Property.updateTimestamp.desc())
        if status == 'cancelled':
            assets = assets.filter(Property.status == 'cancelled').order_by(Property.updateTimestamp.desc())

        if assets.count() == 0:
            template = 'templates/elements/assets0.xml'
        else:
            template = 'templates/elements/assets1.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.assets = assets

    @renderer
    def count(self, request, tag):
        statuses = {'pending': 'Pending',
                    'cancelled': 'Cancelled',
                    'closed': 'Closed'}

        slots = {}
        slots['htmlAssetStatus'] = statuses[self.status]
        slots['htmlAssetCount'] = str(self.assets.count())
        yield tag.clone().fillSlots(**slots)

    @renderer
    def assetStatus(self, request, tag):
        statuses = {'pending': 'Pending',
                    'cancelled': 'Cancelled',
                    'closed': 'Closed'}

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
        locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8' )
        for asset in self.assets:
            timestamp = float(asset.createTimestamp)

            price = db.query(Price).filter(Price.currencyId == 'USD').first()

            askingPriceFiat = float(asset.askingPrice)
            pricePerUnitFiat = float(asset.askingPrice) / float(asset.totalUnits) 

            askingPriceBTC = float(asset.askingPrice) / float(price.last)
            pricePerUnitBTC = (float(asset.askingPrice) / float(price.last)) / float(asset.totalUnits)

            slots = {}
            slots['htmlAssetId'] = str(asset.id)
            slots['htmlTimestamp'] = config.convertTimestamp(timestamp)
            slots['htmlTitle'] = str(asset.title)
            slots['htmlAssetUrl'] = '../%s' % str(asset.id)
            slots['htmlImageUrl'] = '../images/%s.jpg' % str(asset.id)
            slots['htmlTotalUnits'] = str(asset.totalUnits)

            slots['htmlAskingPriceFiat'] = locale.format("%d", askingPriceFiat, grouping=True) 
            slots['htmlPricePerUnitFiat'] = locale.format("%d", pricePerUnitFiat, grouping=True)
            slots['htmlAskingPriceBTC'] = locale.format("%d", askingPriceBTC, grouping=True)
            slots['htmlPricePerUnitBTC'] = locale.format("%d", pricePerUnitBTC, grouping=True)
            self.asset = asset
            yield tag.clone().fillSlots(**slots)


    #@renderer
    #def action(self, request, tag):
    #    actions = {}
    #    actions[config.createTimestamp()] = ['View', 'ticon view hint hint--top hint--rounded', '../describeProperty']
    #    actions[config.createTimestamp()] = ['Delete', 'ticon delete hint hint--top hint--rounded', '../deleteProperty?id=%s' % self.order.id]

    #    for key in sorted(actions.keys()):
    #        slots = {}
    #        slots['htmlId'] = str(self.order.id)
    #        slots['htmlHint'] = actions[key][0]
    #        slots['htmlClass'] = actions[key][1]
    #        slots['htmlUrl'] = actions[key][2]
    #        newTag = tag.clone().fillSlots(**slots)
    #        yield newTag
