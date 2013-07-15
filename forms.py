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


class AddProperty(Element):
    def __init__(self, sessionUser, sessionProperty, sessionResponse):
        self.sellerId = sessionUser['id']
        self.currencyId = sessionUser['currencyId']
        self.sessionProperty = sessionProperty
        self.sessionResponse = sessionResponse
        self.loader = XMLString(FilePath('templates/forms/addProperty.xml').getContent())

    @renderer
    def inputs(self, request, tag):
        sessionProperty = self.sessionProperty

        propertyName = ''
        if sessionProperty.get('name'):
            propertyName = sessionProperty['name']

        propertyDescription = ''
        if sessionProperty.get('description'):
            propertyDescription = sessionProperty['description']

        propertyStock = 1
        if sessionProperty.get('stock'):
            propertyStock = sessionProperty['stock']

        propertyPrice = ''
        if sessionProperty.get('price'):
            propertyPrice = sessionProperty['price']

        sellerNote = ''
        if sessionProperty.get('note'):
            sellerNote = sessionProperty['note']

        slots = {}
        slots['htmlPropertyId'] = str(0)
        slots['htmlTitle'] = str(propertyName)
        slots['htmlDescription'] = str(propertyDescription)
        yield tag.fillSlots(**slots)

    @renderer
    def notification(self, request, tag):
        sessionResponse = self.sessionResponse
        if not sessionResponse['text']:
            return []
        else:
            return Notification(sessionResponse)


class FormBuy(Element):
    def __init__(self, sessionOrder, sessionResponse):
        self.sessionOrder = sessionOrder
        self.sessionResponse = sessionResponse
        product = db.query(PhysicalProduct).filter(PhysicalProduct.id == sessionOrder['productId']).first()

        if product.imageCount == 0:
            template = 'templates/forms/buyProductFormWithoutImage.xml'
        else:
            template = 'templates/forms/buyProductFormWithImage.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.product = product

    @renderer
    def view(self, request, tag):
        product = self.product

        store = db.query(StoreDirectory).filter(StoreDirectory.ownerId == product.sellerId).first()
        profile = db.query(Profile).filter(Profile.userId == product.sellerId).first()

        price = db.query(Price).filter(Price.currencyId == product.currencyId).first()
        price = str(functions.calculate(price.last, product.price))
        
        productImage = '%s/%s_1_m.jpg' % (config.cdn, product.imageHash)


        slots = {}
        slots['htmlProductId'] = str(product.id)
        slots['htmlProductName'] = str(product.name)
        slots['htmlStoreName'] = str(store.name)
        slots['htmlReceivedCount'] = str(profile.receivedSellOrders)
        slots['htmlStoreUrl'] = '../%s' % str(store.name)
        #slots['htmlProductPrice'] = str(price)
        slots['htmlProductImage'] = productImage
        slots['htmlProductPrice'] = "%.4f" % float(price)
        slots['htmlProductPriceFiat'] = str(product.currencyId + " %.2f" % float(product.price))
        slots['htmlProductStock'] = str(product.stock)
        slots['htmlProductQuantity'] = str(self.sessionOrder['quantity'])
        return tag.fillSlots(**slots)

    @renderer
    def country(self, request, tag):
        rates = db.query(Shipping).filter(Shipping.productId == self.product.id).order_by(Shipping.countryId)

        indices = []
        for rate in rates:
            indices.append(rate.countryId)

        index = min(indices)

        for rate in rates:
            countryId = rate.countryId
            thisTagShouldBeChecked = False
            if countryId == index:
                thisTagShouldBeChecked = True

            slots = {}
            slots['inputValue'] = str(countryId)
            slots['inputCaption'] = definitions.countries[int(countryId)]

            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeChecked:
                newTag(selected='yes')
            yield newTag

    @renderer
    def notification(self, request, tag):
        sessionResponse = self.sessionResponse
        if not sessionResponse['text']:
            return []
        else:
            return commonElements.Notification(sessionResponse)

    @renderer
    def description(self, request, tag):
        BlogGrammar = makeGrammar(descriptions.blog_grammar, {"tags": tags})
        output = BlogGrammar(self.product.description).paragraphs()
        return tag(output)

    @renderer
    def image(self, request, tag):
        product = self.product
        imageCount = product.imageCount
        imageId = 1
        while imageId <= imageCount:
            #productImageTiny = '../images/products/%s/%s_%s_tiny.jpg' % (product.sellerId, product.id, imageId)
            #productImage = '../images/products/%s/%s_%s_m.jpg' % (product.sellerId, product.id, imageId)

            productImage = '%s/%s_%s_m.jpg' % (config.cdn, product.imageHash, imageId)
            productImageTiny = '%s/%s_%s_tiny.jpg' % (config.cdn, product.imageHash, imageId)
            slots = {}
            slots['htmlProductImageSwap'] = productImage
            slots['htmlProductImageTiny'] = productImageTiny
            imageId += 1
            newTag = tag.clone().fillSlots(**slots)
            yield newTag

    @renderer
    def escrow(self, request, tag):
        store = db.query(Store).filter(Store.ownerId == self.product.sellerId).first()
        if store.isEscrowOn == 0:
            return []
        else:
            return EscrowCell()

    @renderer
    def soldBy(self, request, tag):
        return SoldBy(self.product)


class EscrowCell(Element):
    html = XMLString('''
                     <a href="../helpEscrow" xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1">
                     <img src="../images/escrow_badge.png" style="margin: 0px;" />
                     </a>
                       ''')

    def __init__(self):
        self.loader = self.html


class FormEdit(Element):
    def __init__(self, sessionUser, sessionProduct, sessionResponse):
        self.sellerId = sessionUser['id']
        self.currencyId = sessionUser['currencyId']
        self.sessionProduct = sessionProduct
        self.sessionResponse = sessionResponse
        self.productId = sessionProduct['id']
        self.product = db.query(PhysicalProduct).filter(PhysicalProduct.id == self.productId).first()
        self.sellerNote = db.query(SellerNote).filter(SellerNote.productId == self.productId).first()
        self.loader = XMLString(FilePath('templates/forms/editProduct.xml').getContent())

    @renderer
    def menu(self, request, tag):
        sellerId = self.sellerId
        store = db.query(StoreDirectory).filter(StoreDirectory.ownerId == sellerId).first()
        profile = db.query(Profile).filter(Profile.userId == sellerId).first()

        slots = {}
        slots['htmlStoreUrl'] = '../%s' % store.name
        slots['htmlUnreadCount'] = str(profile.unreadCount)
        yield tag.clone().fillSlots(**slots)

    @renderer
    def category(self, request, tag):
        sessionProduct = self.sessionProduct
        productId = sessionProduct['id']
        product = db.query(CatalogItem).filter(CatalogItem.productId == productId).first()

        categoryId = product.categoryId
        if sessionProduct.get('categoryId'):
            categoryId = sessionProduct['categoryId']

        categories = definitions.productCategories

        for key in sorted(categories, key=categories.get, reverse=False):
            thisTagShouldBeSelected = False
            if key == categoryId:
                thisTagShouldBeSelected = True
            slots = {}
            slots['inputValue'] = key
            slots['inputCaption'] = categories[key]
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='')
            if key == 'ZZ':
                yield []
            else:
                yield newTag

    @renderer
    def isShowcased(self, request, tag):
        showcase = db.query(Showcase).filter(Showcase.sellerId == self.sellerId).first()

        isChecked = False
        try:
            if showcase.productId == self.productId:
                isChecked = True
            print showcase.productId, showcase.sellerId
        except:
            print "no showcase for product"
        slots = {}
        newTag = tag.clone().fillSlots(**slots)
        if isChecked:
            newTag(checked='yes')
        yield newTag

    @renderer
    def details(self, request, tag):
        sessionProduct = self.sessionProduct
        currencyId = self.currencyId

        productName = self.product.name
        if sessionProduct.get('name'):
            productName = sessionProduct['name']

        productDescription = self.product.description
        if sessionProduct.get('description'):
            productDescription = sessionProduct['description']

        productStock = self.product.stock
        if sessionProduct.get('stock'):
            productStock = sessionProduct['stock']

        price = db.query(Price).filter(Price.currencyId == currencyId).first()

        productPrice = self.product.price
        if sessionProduct.get('price'):
            productPrice = sessionProduct['price']

        sellerNote = ''
        try:
            if self.sellerNote.text:
                sellerNote = self.sellerNote.text
        except:
            sellerNote = ''

        if sessionProduct.get('note'):
            sellerNote = sessionProduct['note']

        slots = {}
        slots['htmlProductId'] = str(self.productId)
        slots['htmlName'] = str(productName)
        slots['htmlDescription'] = str(productDescription)
        slots['htmlStock'] = str(productStock)
        slots['htmlPrice'] = str(productPrice)
        slots['htmlLast'] = str(price.last)
        slots['htmlSellerNote'] = str(sellerNote)
        slots['htmlCurrency'] = currencyId
        yield tag.fillSlots(**slots)

    @renderer
    def formImageEdit(self, request, tag):
        if self.product.imageCount == 0:
            return []
        else:
            return FormEditImage(self.product)

    @renderer
    def notification(self, request, tag):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)
        sessionResponse = self.sessionResponse
        if not sessionResponse['text']:
            return []
        else:
            return Notification(sessionResponse)


class FormEditImage(Element):
    loader = XMLString('''
                       <div class="c12" xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1" t:render="image">
                       <img><t:attr name="src"><t:slot name="htmlProductImage" /></t:attr></img>
                       </div>
                       ''')

    def __init__(self, product):
        self.product = product

    @renderer
    def image(self, request, tag):
        slots = {}
        slots['htmlProductImage'] = '../images/products/%s/%s_%s_m.jpg' % (self.product.sellerId, self.product.id, 1)
        return tag.fillSlots(**slots)


class Notification(Element):
    def __init__(self, sessionResponse):
        self.sessionResponse = sessionResponse
        self.loader = XMLString(FilePath('templates/notificationProductEdit0.xml').getContent())

    @renderer
    def message(self, request, tag):
        sessionResponse = self.sessionResponse
        index = sessionResponse['class']
        messageClass = ['alert alert-block',
                        'alert alert-error',
                        'alert alert-success',
                        'alert alert-info']

        slots = {}
        slots['htmlMessageClass'] = messageClass[index]
        slots['htmlMessageText'] = sessionResponse['text']
        return tag.fillSlots(**slots)


class SoldBy(Element):
    xml =  [''] * 2
    xml[0] = XMLString('''
                       <small t:render="soldBy" xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1">Sold By <a><t:attr name="href"><t:slot name="htmlStoreUrl" /></t:attr><t:slot name="htmlStoreName" /></a></small>
                       ''')
    xml[1] = XMLString('''
                       <small t:render="soldBy" xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1">Sold By <a><t:attr name="href"><t:slot name="htmlStoreUrl" /></t:attr><t:slot name="htmlStoreName" /></a> (<t:slot name="htmlReceivedCount" />)</small>
                       ''')

    def __init__(self, product):
        self.profile = db.query(Profile).filter(Profile.userId == product.sellerId).first()
        self.store = db.query(StoreDirectory).filter(StoreDirectory.ownerId == product.sellerId).first()

        if self.profile.receivedSellOrders == 0:
            self.loader = self.xml[0]
        else:
            self.loader = self.xml[1]

    @renderer
    def soldBy(self, request, tag):
        slots = {}

        slots['htmlStoreName'] = str(self.store.name)
        if self.profile.receivedSellOrders != 0:
            slots['htmlStoreName'] = str(self.store.name)
            slots['htmlReceivedCount'] = str(self.profile.receivedSellOrders)

        slots['htmlStoreUrl'] = '../%s' % str(self.store.name)
        yield tag.fillSlots(**slots)




class ProductImage():
    def __init__(self, request, oldImageCount, oldImageHash):
        self.request = request
        self.oldImageCount = oldImageCount
        self.oldImageHash = oldImageHash

    def save(self):
        fieldStorage = cgi.FieldStorage(
            fp=self.request.content,
            headers=self.request.getAllHeaders(),
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.request.getAllHeaders()['content-type'], }
        )

        imagesToSave = []
        imageToRemove = []

        fieldKeys = [x for x in fieldStorage.keys() if 'imageField' in x]
        fieldKeys.sort(reverse=True)

        fileKeys = [x for x in fieldStorage.keys() if 'imageFile' in x]
        fileKeys.sort(reverse=True)

        oldImageHash = self.oldImageHash
        
        timestamp = config.createTimestamp()
        newImageHash = hashlib.sha224(str(timestamp)).hexdigest()

        temp = 'images/products'
        CloudManager = cloud.Cloud()
        if not oldImageHash:
            values = []
            for key in fileKeys:
                value = fieldStorage[key].value
                if value:
                     values.append(value)
 
            imageCount = len(values) 
            i = 1
            while values:
                filename = str(newImageHash) + '_' + str(i)
                filepath = temp + '/' + filename + '.jpg'

                out = open(filepath, 'wb')
                out.write(values.pop())
                out.close()

                filepaths = [filepath]
                filepaths += self.create(filepath)
                for filepath in filepaths:
                    CloudManager.upload(filepath)
                    os.remove(filepath)

                i += 1
        else: 
            imagesToKeep = [] 
            imagesToSave = [] 

            for key in fieldKeys:
                value = fieldStorage[key].value
                if value:
                    imagesToKeep.append(value)

            values = {}
            for key in fileKeys:
                value = fieldStorage[key].value
                if value:
                    index = key.replace('imageFile', '')
                    values[index] = value 
                    imagesToSave.append(index)

            imagesToKeep = map(int, imagesToKeep)
            imagesToKeep = [index for index in imagesToKeep if index != 0]

            imagesToSave = map(int, imagesToSave)

            print 'imagesToKeep', imagesToKeep
            print 'imagesToSave', imagesToSave

            imagesToKeep += imagesToSave
            imagesToKeep = list(set(imagesToKeep))

            imagesToConsolidate = imagesToKeep + imagesToSave
            imagesToConsolidate = list(set(imagesToConsolidate))
            print 'imagesToConsolidate', imagesToConsolidate

            while imagesToSave:
                index = str(imagesToSave.pop())
                prefix = '%s_%s' % (oldImageHash, index)
                filepath = temp + '/' + prefix + '.jpg'

                out = open(filepath, 'wb')
                out.write(values[index])
                out.close()

                filepaths = [filepath]
                filepaths += self.create(filepath)
                for filepath in filepaths:
                    #cloud.upload(filepath)
                    CloudManager.upload(filepath)
                    os.remove(filepath)

            #print 'oldImageHash', cloud.get(oldImageHash)
            CloudManager.consolidate(imagesToConsolidate, oldImageHash, newImageHash)
            #print 'newImageHash', cloud.get(newImageHash)

            imageCount = len(imagesToKeep)
            imageCount = len(imagesToConsolidate)

        image = {}
        image['count'] = imageCount
        image['hash'] = newImageHash
        return image

    def create(self, sourcepath):
        tails = ['_m.jpg', '_t.jpg', '_tiny.jpg', '_small.jpg']
        sizes = [420, 128, 90, 80]

        print sourcepath

        filepaths = []
        for index, tail in enumerate(tails):
            imageSize = sizes[index], sizes[index]
            filepath = sourcepath.split(".")[0] + tail

            try:
                im = Image.open(sourcepath)
                im.thumbnail(imageSize, Image.ANTIALIAS)
                im.save(filepath, "JPEG")
                print "%s %s created" % (imageSize, filepath)
                filepaths.append(filepath)
                
            except IOError as e:
                print "cannot create %s %s" % (imageSize, filepath)
                print e
       
        return filepaths
       
    def rename(self):
        path = 'images/products'
        start = "%s_" % self.productId

        imageIds = []
        for filename in os.listdir(path):
            if filename.startswith(start) and filename.endswith("_t.jpg"):
                parts = filename.split('.')
                parts = parts[0].split('_')
                imageId = parts[1]
                imageIds.append(imageId)
                print filename

        imageIds.sort()

        tails = ['.jpg', '_m.jpg', '_t.jpg', '_tiny.jpg', '_small.jpg']
        for index, imageId in enumerate(imageIds):
            index += 1
            for tail in tails:
                i = os.path.join(path, '%s%s%s' % (start, imageId, tail))
                o = os.path.join(path, '%s%s%s' % (start, index, tail))
                os.rename(i, o)
                print "%s%s created%s" % (config.color.BLUE, i, config.color.ENDC)


class DeleteOne(Resource):
    def __init__(self, productViews):
        self.productViews = productViews

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        userId = sessionUser['id']
        if userId == 0:
            return redirectTo('../', request)

        productId = 0
        try:
            productId = int(request.args.get('id')[0])
        except:
            return redirectTo('../', request)

        product = db.query(PhysicalProduct).filter(PhysicalProduct.id == productId).first()
        if product.sellerId != userId:
            return redirectTo('../', request)

        catalogItem = db.query(CatalogItem).filter(CatalogItem.productId == productId).first()

        product.status = 'deleted'
        catalogItem.status = 'deleted'

        if product.id in self.productViews.keys():
            del self.productViews[product.id]

        store = db.query(Store).filter(Store.ownerId == userId).first()
        store.productCount -= 1
        store.updateTimestamp = config.createTimestamp()

        if store.productCount <= 0:
            store.status = 'closed'

        url = '../%s' % str(store.name)

        db.commit()
        return redirectTo(url, request)


class DeleteMany(Resource):
    def __init__(self, productViews):
        self.productViews = productViews

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        if not request.args:
            return redirectTo('../inbox', request)

        sessionUser = SessionManager(request).getSessionUser()
        userId = sessionUser['id']
        if userId == 0:
            return redirectTo('../', request)

        productIds = request.args.get('productIds')

        store = db.query(Store).filter(Store.ownerId == userId).first()
        for productId in productIds:
            product = db.query(PhysicalProduct).filter(PhysicalProduct.id == productId).first()
            if product.sellerId != userId:
                return redirectTo('../', request)

            catalogItem = db.query(CatalogItem).filter(CatalogItem.productId == productId).first()

            product.status = 'deleted'
            catalogItem.status = 'deleted'

            if product.id in self.productViews.keys():
                del self.productViews[product.id]

            store.productCount -= 1
            store.updateTimestamp = config.createTimestamp()

            if store.productCount <= 0:
                store.status = 'closed'
            db.commit()

        url = '../%s' % str(store.name)

        return redirectTo(url, request)
