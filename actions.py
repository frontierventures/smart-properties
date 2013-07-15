#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python .filepath import FilePath
from parsley import makeGrammar
from twisted.web.template import XMLString, Element, renderer, tags

from data import db
from data import Property 
from sqlalchemy import func
from sessions import SessionManager

#import Image
import cgi
#import cloud
import commonElements
import config
import decimal
import definitions
#import descriptions
import error
import functions
import hashlib
import inspect
import itertools
import os

D = decimal.Decimal


class AddProperty(Resource):
    def render(self, request):
        if not request.args:
            return redirectTo('../', request)

        sessionUser = SessionManager(request).getSessionUser()

        if sessionUser['type'] != 0:
            return redirectTo('../', request)

        sessionProperty = SessionManager(request).getSessionProperty()
        propertyId = sessionProperty['id']

        url = '../summaryProperties?action=add'
        url = str(url)

        title = request.args.get('propertyTitle')[0]
        description = request.args.get('propertyDescription')[0]

        sessionProperty['title'] = title
        sessionProperty['description'] = description

        #if error.propertyTitle(request, propertyTitle):
        #    return redirectTo(url, request)

        #if error.propertyDescription(request, propertyDescription):
        #    return redirectTo(url, request)

        if request.args.get('button')[0] == 'Save':
            status = 'available'

            timestamp = config.createTimestamp()

            propertyObject = Property(status, timestamp, timestamp, title, description, '', '', 0, 0)

            db.add(propertyObject)
            db.commit()

            #image = ProductImage(request, product.imageCount, product.imageHash).save()

            #product.imageCount = image['count']

            #product.imageHash = image['hash']
            #db.commit()
            return redirectTo('../summaryProperties', request)
