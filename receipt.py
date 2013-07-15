#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.server import NOT_DONE_YET
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import db
from data import Order
from sessions import SessionManager

import config
import decimal
import pages
D = decimal.Decimal


class Main(Resource):
    def render(self, request):

        sessionOrder = SessionManager(request).getSessionOrder()
        orderId = sessionOrder['id']

        if not orderId:
            return redirectTo('../', request)

        order = db.query(Order).filter(Order.id == orderId).first()

        sessionUser = SessionManager(request).getSessionUser()
        investorId = sessionOrder['investorId']

        Page = pages.Receipt('Receipt', 'receipt')
        Page.sessionUser = sessionUser
        Page.sessionOrder = sessionOrder

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        print "%ssessionOrder: %s%s" % (config.color.BLUE, sessionOrder, config.color.ENDC)
        SessionManager(request).clearSessionResponse()

        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)

        #request.write("<!DOCTYPE html>\n")
        #request.write("<html>\n")
        #request.write("<head>\n")
        #request.write("<meta charset=\"utf-8\">\n")
        #request.write("<title>Welcome to Coingig.com!</title>\n")
        #request.write("<meta name=\"description\" content=\"Coingig website description here\">\n")
        #request.write("<link rel=\"stylesheet\" href=\"../styles/normalize.min.css\">\n")
        #request.write("<link rel=\"stylesheet\" href=\"../styles/main.css\">\n")
        #request.write("<!--[if lt IE 9]>\n")
        #request.write("<script src=\"http://html5shiv.googlecode.com/svn/trunk/html5.js\"></script>\n")
        #request.write("<script>window.html5 || document.write('<script src=\"../scripts/vendor/html5shiv.js\"><\/script>')</script>\n")
        #request.write("<![endif]-->\n")
        #request.write("<script type=\"text/javascript\" src=\"//use.typekit.net/uis4jqg.js\"></script>\n")
        #request.write("<script type=\"text/javascript\">try{Typekit.load();}catch(e){}</script>\n")
        #request.write("</head>\n")
        #request.write("<body>\n")

        #request.write("<div class=\"wfull headbg\">\n")
        #flattenString(request, commonElements.Header(sessionUser)).addCallback(request.write)
        #flattenString(request, search.Form(sessionSearch)).addCallback(request.write)
        #request.write("</div>\n")

        ##storename = str(directoryData.get_By_Id(sellerId)['storename'])
        #store = db.query(Store).filter(Store.ownerId == sellerId).first()
        #request.write("<div class=\"grid w980\">\n")
        #request.write("<div class=\"content-full\">\n")
        #flattenString(request, Receipt(order, store)).addCallback(request.write)
        #request.write("</div>\n")
        #request.write("</div>\n")

        #flattenString(request, commonElements.Footer()).addCallback(request.write)
        #request.write("<script src=\"http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js\"></script>\n")
        #request.write("<script>window.jQuery || document.write('<script src=\"js/vendor/jquery-1.9.1.min.js\"><\/script>')</script>\n")
        #request.write("<script src=\"../scripts/jquery-ui.js\"></script>\n")
        #request.write("<script src=\"../scripts/jquery.bxslider.min.js\"></script>\n")
        #request.write("<script src=\"../scripts/main.js\"></script>\n")
        ##request.write("<?php include("status.php"); /* delete this include and status.php file */ ?>\n")
        #request.write("</body>\n")
        #request.write("</html>\n")
        #request.finish()
        #print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        #print "sessionSearch: %s" % sessionSearch
        #print "sessionOrder: %s" % sessionOrder
        #SessionManager(request).clearSessionResponse()
        #SessionManager(request).clearSessionOrder()
        #return NOT_DONE_YET


class Receipt(Element):
    def __init__(self, order):
        self.order = order
        self.loader = XMLString(FilePath('templates/elements/receipt.xml').getContent())

    @renderer
    def details(self, request, tag):
        slots = {}
        #slots['htmlTotal'] = str(D(self.order.subTotal) + D(self.order.shippingCost))
        #slots['htmlBitcoinAddress'] = str(self.order.paymentAddress)
        #slots['htmlStorename'] = str(self.store.name)
        #slots['htmlStoreUrl'] = "../%s" % self.store.name
        yield tag.fillSlots(**slots)
