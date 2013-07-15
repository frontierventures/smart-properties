#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import db
from sqlalchemy.sql import and_
from data import Property
from sessions import SessionManager

import config
import definitions
import functions
import pages


class Main(Resource):
    isLeaf = True

    def __init__(self, sellerId, productId):
        self.sellerId = sellerId
        self.productId = productId

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        userId = sessionUser['id']

        sessionSearch = SessionManager(request).getSessionSearch()
        sessionResponse = SessionManager(request).getSessionResponse()

        try:
            linkId = request.args.get('linkId')[0]
        except:
            linkId = 0

        try:
            action = request.args.get('action')[0]
        except:
            action = ''

        if not action:
            sessionUser['page'] = 'buyProperty'

            product = db.query(CatalogItem).filter(CatalogItem.productId == self.productId).first()

            sessionOrder = SessionManager(request).getSessionOrder()
            sessionOrder['productId'] = self.productId
            sessionOrder['sellerId'] = self.sellerId
            sessionOrder['categoryId'] = product.categoryId 
            sessionSearch['categoryId'] = product.categoryId

            if linkId > 0:
                affiliateLink = db.query(AffiliateLink).filter(AffiliateLink.id == linkId).first()
                affiliateLink.visits += 1
                affiliateLink.updateTimestamp = config.createTimestamp()
                publisherId = affiliateLink.publisherId
                db.commit()

            sessionOrder['linkId'] = linkId

            if not sessionOrder.get('quantity'):
                sessionOrder['quantity'] = 1

            Page = pages.BuyProduct('Coingig.com - %s' % str(product.name), 'buyProduct')
            Page.sessionUser = sessionUser
            Page.sessionResponse = sessionResponse
            Page.sessionOrder = sessionOrder

            view = db.query(View).filter(View.productId == self.productId).first()
            view.count += 1
            db.commit()

            print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
            print "sessionSearch: %s" % sessionSearch
            print "sessionResponse: %s" % sessionResponse
            SessionManager(request).clearSessionResponse()
            request.write('<!DOCTYPE html>\n')
            return renderElement(request, Page)

        if userId == 0:
            return redirectTo('../', request)

        if action == 'editDetails':
            product = db.query(CatalogItem).filter(CatalogItem.productId == self.productId).first()

            sessionProduct = SessionManager(request).getSessionProduct()
            sessionProduct['id'] = self.productId
            sessionProduct['categoryId'] = product.categoryId
            sessionProduct['name'] = product.name
            #sessionProduct['description'] = product.description
            sessionProduct['price'] = product.price

            if product.sellerId != sessionUser['id']:
                return redirectTo('../', request)

            Page = pages.EditProduct('Edit Product', 'editProduct')
            Page.sessionUser = sessionUser
            Page.sessionResponse = sessionResponse
            Page.sessionProduct = sessionProduct

            print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
            print "sessionProduct: %s" % sessionProduct
            print "sessionResponse: %s" % sessionResponse
            SessionManager(request).clearSessionResponse()
            request.write('<!DOCTYPE html>\n')
            return renderElement(request, Page)


class Reviews(Element):
    def __init__(self, sessionOrder):
        productId = sessionOrder['productId']
        reviews = db.query(Review).filter(Review.productId == productId).order_by(Review.timestamp.desc())
        if reviews.count() == 0:
            template = 'templates/reviews0.xml'
        else:
            template = 'templates/reviews1.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.reviews = reviews

    @renderer
    def review(self, request, tag):
        for review in self.reviews:
            buyerId = review.buyerId
            buyer = db.query(Profile).filter(Profile.userId == buyerId).first()

            slots = {}
            slots['htmlStarsStyle'] = 'width:%s%%;' % review.rating
            slots['htmlBuyerFirst'] = buyer.first
            slots['htmlBuyerLast'] = buyer.last
            slots['htmlReviewHeadline'] = review.headline
            slots['htmlReviewBody'] = review.body
            yield tag.clone().fillSlots(**slots)


class Related(Element):
    def __init__(self, sessionOrder):
        catalogItem = db.query(CatalogItem).filter(CatalogItem.productId == sessionOrder['productId']).first()
        products = db.query(CatalogItem).filter(and_(
            CatalogItem.status == 'available',
            CatalogItem.sellerId == catalogItem.sellerId,
            CatalogItem.categoryId == catalogItem.categoryId)).order_by(CatalogItem.updateTimestamp)

        if products.count() == 0:
            template = 'templates/related0.xml'
        else:
            template = 'templates/related1.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.products = products

    @renderer
    def product(self, request, tag):
        for product in self.products:

            price = db.query(Price).filter(Price.currencyId == product.currencyId).first()
            price = str(functions.calculate(price.last, product.price))

            store = db.query(StoreDirectory).filter(StoreDirectory.ownerId == product.sellerId).first()
            if product.imageCount == 0:
                productImageThumb = '../%s_t.jpg' % definitions.NULL_IMAGE
            else:
                #productImageThumb = '../images/products/%s/%s_%s_t.jpg' % (product.sellerId, product.productId, 1)
                productImageThumb = '%s/%s_1_t.jpg' % (config.cdn, product.imageHash)

            slots = {}
            slots['htmlProductImage'] = productImageThumb
            slots['htmlProductName'] = product.name
            slots['htmlProductUrl'] = '../%s/%s' % (store.name, str(product.productId))
            #slots['htmlPrice'] = str(price)
            slots['htmlProductPrice'] = "%.4f" % float(price)
            slots['htmlProductPriceFiat'] = str(product.currencyId + " %.2f" % float(product.price))
            yield tag.clone().fillSlots(**slots)
