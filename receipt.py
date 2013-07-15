#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.template import flattenString
from twisted.web.util import redirectTo
from twisted.web.server import NOT_DONE_YET
from twisted.web.template import Element, renderer
from twisted.web.template import XMLString
from twisted.python .filepath import FilePath

from data import db
from data import AffiliateLink, Order, Publisher, Store
from sessions import SessionManager

import commonElements
import config
import inspect
import search
import decimal
D = decimal.Decimal


class Main(Resource):
    def render(self, request):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        sessionOrder = SessionManager(request).getSessionOrder()
        orderId = sessionOrder['id']

        if not orderId:
            return redirectTo('../', request)

        order = db.query(Order).filter(Order.id == orderId).first()

        sessionUser = SessionManager(request).getSessionUser()
        sessionSearch = SessionManager(request).getSessionSearch()
        sellerId = sessionOrder['sellerId']

        linkId = sessionOrder['linkId']
        if linkId > 0:
            affiliateLink = db.query(AffiliateLink).filter(AffiliateLink.id == linkId).first()
            affiliateLink.visits += 1
            affiliateLink.updateTimestamp = config.createTimestamp()
            print order.subTotal
            earnings = float(order.subTotal) * 0.01 
            affiliateLink.earnings += earnings 
#            publisherId = affiliateLink.publisherId
#            db.commit()
#            publisher = db.query(Publisher).filter(Publisher.id == publisherId).first()
#            publisher.earnings += order.subTotal * 0.01
            db.commit()

        request.write("<!DOCTYPE html>\n")
        request.write("<html>\n")
        request.write("<head>\n")
        request.write("<meta charset=\"utf-8\">\n")
        request.write("<title>Welcome to Coingig.com!</title>\n")
        request.write("<meta name=\"description\" content=\"Coingig website description here\">\n")
        request.write("<link rel=\"stylesheet\" href=\"../styles/normalize.min.css\">\n")
        request.write("<link rel=\"stylesheet\" href=\"../styles/main.css\">\n")
        request.write("<!--[if lt IE 9]>\n")
        request.write("<script src=\"http://html5shiv.googlecode.com/svn/trunk/html5.js\"></script>\n")
        request.write("<script>window.html5 || document.write('<script src=\"../scripts/vendor/html5shiv.js\"><\/script>')</script>\n")
        request.write("<![endif]-->\n")
        request.write("<script type=\"text/javascript\" src=\"//use.typekit.net/uis4jqg.js\"></script>\n")
        request.write("<script type=\"text/javascript\">try{Typekit.load();}catch(e){}</script>\n")
        request.write("</head>\n")
        request.write("<body>\n")

        request.write("<div class=\"wfull headbg\">\n")
        flattenString(request, commonElements.Header(sessionUser)).addCallback(request.write)
        flattenString(request, search.Form(sessionSearch)).addCallback(request.write)
        request.write("</div>\n")

        #storename = str(directoryData.get_By_Id(sellerId)['storename'])
        store = db.query(Store).filter(Store.ownerId == sellerId).first()
        request.write("<div class=\"grid w980\">\n")
        request.write("<div class=\"content-full\">\n")
        flattenString(request, Receipt(order, store)).addCallback(request.write)
        request.write("</div>\n")
        request.write("</div>\n")

        flattenString(request, commonElements.Footer()).addCallback(request.write)
        request.write("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js\"></script>\n")
        request.write("<script>window.jQuery || document.write('<script src=\"js/vendor/jquery-1.9.1.min.js\"><\/script>')</script>\n")
        request.write("<script src=\"../scripts/jquery-ui.js\"></script>\n")
        request.write("<script src=\"../scripts/jquery.bxslider.min.js\"></script>\n")
        request.write("<script src=\"../scripts/main.js\"></script>\n")
        #request.write("<?php include("status.php"); /* delete this include and status.php file */ ?>\n")
        request.write("</body>\n")
        request.write("</html>\n")
        request.finish()
        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        print "sessionSearch: %s" % sessionSearch
        print "sessionOrder: %s" % sessionOrder
        SessionManager(request).clearSessionResponse()
        SessionManager(request).clearSessionOrder()
        return NOT_DONE_YET


class Receipt(Element):
    def __init__(self, order, store):
        self.order = order
        self.store = store
        self.loader = XMLString(FilePath('templates/elementReceipt0.xml').getContent())

    @renderer
    def view(self, request, tag):
        slots = {}
        slots['htmlTotal'] = str(D(self.order.subTotal) + D(self.order.shippingCost))
        slots['htmlBitcoinAddress'] = str(self.order.paymentAddress)
        slots['htmlStorename'] = str(self.store.name)
        slots['htmlStoreUrl'] = "../%s" % self.store.name
        yield tag.fillSlots(**slots)
