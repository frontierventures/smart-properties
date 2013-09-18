#!/usr/bin/env python
from twisted.web.template import Element, renderer
from twisted.web.template import XMLString
from twisted.python .filepath import FilePath

import config
import definitions
import inspect

from data import Profile
from data import db


class Address(Element):
    def __init__(self, sessionAddress):
        self.sessionAddress = sessionAddress
        self.loader = XMLString(FilePath(templates['address']).getContent())

    @renderer
    def form(self, request, tag):
        sessionAddress = self.sessionAddress
        addressId = sessionAddress['id']
        buyerFirst = ''
        if sessionAddress.get('buyerFirst'):
            buyerFirst = sessionAddress['buyerFirst']

        buyerLast = ''
        if sessionAddress.get('buyerLast'):
            buyerLast = sessionAddress['buyerLast']

        buyerEmail = ''
        if sessionAddress.get('buyerEmail'):
            buyerEmail = sessionAddress['buyerEmail']

        buyerPhone = ''
        if sessionAddress.get('buyerPhone'):
            buyerPhone = sessionAddress['buyerPhone']

        buyerAddress1 = ''
        if sessionAddress.get('buyerAddress1'):
            buyerAddress1 = sessionAddress['buyerAddress1']

        buyerAddress2 = ''
        if sessionAddress.get('buyerAddress2'):
            buyerAddress2 = sessionAddress['buyerAddress2']

        buyerCity = ''
        if sessionAddress.get('buyerCity'):
            buyerCity = sessionAddress['buyerCity']

        buyerState = ''
        if sessionAddress.get('buyerState'):
            buyerState = sessionAddress['buyerState']

        buyerZip = ''
        if sessionAddress.get('buyerZip'):
            buyerZip = sessionAddress['buyerZip']

        slots = {}
        slots['htmlId'] = addressId
        slots['htmlBuyerFirst'] = buyerFirst
        slots['htmlBuyerLast'] = buyerLast
        slots['htmlBuyerEmail'] = buyerEmail
        slots['htmlBuyerPhone'] = buyerPhone
        slots['htmlBuyerAddress1'] = buyerAddress1
        slots['htmlBuyerAddress2'] = buyerAddress2
        slots['htmlBuyerCity'] = buyerCity
        slots['htmlBuyerState'] = buyerState
        slots['htmlBuyerZip'] = buyerZip
        yield tag.fillSlots(**slots)

    @renderer
    def country(self, request, tag):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        sessionAddress = self.sessionAddress
        countries = definitions.countries

        buyerCountryId = 186
        if sessionAddress.get('buyerCountry'):
            buyerCountryId = int(sessionAddress['buyerCountry'])

        counter = -1

        for country in sorted(countries):
            counter += 1
            thisTagShouldBeSelected = False
            if counter == buyerCountryId:
                thisTagShouldBeSelected = True
            slots = {}
            slots['inputValue'] = str(counter)
            slots['inputCaption'] = country
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='')
            yield newTag


class BecomeAffiliate(Element):
    def __init__(self, session_user):
        self.session_user = session_user
        self.loader = XMLString(FilePath(templates['becomeAffiliate']).getContent())

    @renderer
    def form(self, request, tag):
        slots = {}
        slots['htmlPublisherId'] = str(self.session_user['id'])
        yield tag.fillSlots(**slots)


class CancelOrder(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['cancelOrder']).getContent())

    @renderer
    def reason(self, request, tag):
        reasons = definitions.orderCancelationReasons

        reason = 'AA'
        for key in sorted(reasons, key=reasons.get, reverse=False):
            thisTagShouldBeSelected = False
            if key == reason:
                thisTagShouldBeSelected = True
            slots = {}
            slots['inputValue'] = key
            slots['inputCaption'] = reasons[key]
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='')
            yield newTag


class ContactOwner(Element):
    def __init__(self, receiverId, senderId):
        self.receiverId = receiverId
        self.senderId = senderId
        if senderId == 0:
            template = templates['contactOwner0']
        else:
            template = templates['contactOwner1']
        self.loader = XMLString(FilePath(template).getContent())

    @renderer
    def form(self, request, tag):
        slots = {}
        slots['htmlReceiverId'] = str(self.receiverId)
        slots['htmlSenderId'] = str(self.senderId)
        yield tag.fillSlots(**slots)


class CloseStore(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['closeStore']).getContent())


class DescribeUser(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['describeUser']).getContent())


class EditStore(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['editStore']).getContent())


class GenerateLink(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['generateLink']).getContent())


class Help(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['help']).getContent())


class HelpEscrow(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['helpEscrow']).getContent())


class Message(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['message']).getContent())


class NotifyOwner(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['notifyOwner']).getContent())


class ProductInfo(Element):
    def __init__(self, sessionProduct):
        self.sessionProduct = sessionProduct
        self.loader = XMLString(FilePath(templates['productInfo']).getContent())


class RecoverPassword(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['recoverPassword']).getContent())


class ReviewOrder(Element):
    def __init__(self, sessionReview):
        self.sessionReview = sessionReview
        self.loader = XMLString(FilePath(templates['reviewOrder']).getContent())

    @renderer
    def question(self, request, tag):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        for index, question in enumerate(definitions.questions):
            self.reviewAnswerIndex = index
            slots = {}
            slots['htmlQuestion'] = question

            newTag = tag.clone().fillSlots(**slots)
            yield newTag

    @renderer
    def radioYes(self, request, tag):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        index = self.reviewAnswerIndex
        sessionReview = self.sessionReview

        reviewAnswers = [1, 1, 1, 1, 1]
        if sessionReview.get('answers'):
            reviewAnswers = sessionReview['answers']

        thisTagShouldBeChecked = False
        if reviewAnswers[index] == 1:
            thisTagShouldBeChecked = True

        slots = {}
        slots['htmlYesId'] = 'ryes%s' % index
        slots['htmlInputName'] = 'reviewAnswer%s' % index
        slots['htmlInputValue'] = '1'

        newTag = tag.clone().fillSlots(**slots)
        if thisTagShouldBeChecked:
            newTag(checked='')
        yield newTag

    @renderer
    def radioNo(self, request, tag):
        print "%s%s %s%s" % (config.color.RED, __name__, inspect.stack()[0][3], config.color.ENDC)

        index = self.reviewAnswerIndex
        sessionReview = self.sessionReview

        reviewAnswers = [1, 1, 1, 1, 1]
        if sessionReview.get('answers'):
            reviewAnswers = sessionReview['answers']

        thisTagShouldBeChecked = False
        if reviewAnswers[index] == 0:
            thisTagShouldBeChecked = True

        slots = {}
        slots['htmlNoId'] = 'rno%s' % index
        slots['htmlInputName'] = 'reviewAnswer%s' % index
        slots['htmlInputValue'] = '0'

        newTag = tag.clone().fillSlots(**slots)
        if thisTagShouldBeChecked:
            newTag(checked='')
        yield newTag


class SellerInfo(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['sellerInfo']).getContent())


class SendMessage(Element):
    def __init__(self, session_user):
        self.session_user = session_user
        self.profile = db.query(Profile).filter(Profile.userId == session_user['id']).first()
        self.loader = XMLString(FilePath(templates['sendMessage']).getContent())

    @renderer
    def form(self, request, tag):
        slots = {}
        #slots['htmlSenderId'] = str(self.session_user['id'])
        slots['htmlSenderName'] = str(self.profile.first)
        yield tag.fillSlots(**slots)


class StoreInfo(Element):
    def __init__(self, session_user):
        self.session_user = session_user
        self.loader = XMLString(FilePath(templates['storeInfo']).getContent())

    @renderer
    def currency(self, request, tag):
        session_user = self.session_user

        userCurrency = session_user['currencyId']

        for currency in definitions.currencies:
            thisTagShouldBeSelected = False
            if currency == userCurrency:
                thisTagShouldBeSelected = True
            slots = {}
            slots['inputValue'] = currency
            slots['inputCaption'] = currency
            newTag = tag.clone().fillSlots(**slots)
            if thisTagShouldBeSelected:
                newTag(selected='')
            yield newTag

    @renderer
    def bitcoinAddress(self, request, tag):
        session_user = self.session_user
        userId = session_user['id']

        #profile = profileData.get_By_Id(userId)
        profile = db.query(Profile).filter(Profile.userId == userId).first()

        slots = {}
        slots['htmlBitcoinAddress'] = profile.bitcoinAddress
        yield tag.clone().fillSlots(**slots)


class SummaryUsers(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['summaryUsers']).getContent())


class VerifyEmail(Element):
    def __init__(self):
        self.loader = XMLString(FilePath(templates['verifyEmail']).getContent())


templates = {'address': 'templates/popups/address.xml',
             'becomeAffiliate': 'templates/popups/becomeAffiliate.xml',
             'cancelOrder': 'templates/popups/cancelOrder.xml',
             'closeStore': 'templates/popups/closeStore.xml',
             'contactOwner0': 'templates/popups/contactOwner0.xml',
             'contactOwner1': 'templates/popups/contactOwner1.xml',
             'describeUser': 'templates/popups/describeUser.xml',
             'editStore': 'templates/popups/editStore.xml',
             'generateLink': 'templates/popups/generateLink.xml',
             'help': 'templates/popups/help.xml',
             'helpEscrow': 'templates/popups/helpEscrow.xml',
             'message': 'templates/popups/message.xml',
             'notifyOwner': 'templates/popups/notifyOwner.xml',
             'productInfo': 'templates/popups/productInfo.xml',
             'recoverPassword': 'templates/popups/recoverPassword.xml',
             'reviewOrder': 'templates/popups/reviewOrder.xml',
             'sellerInfo': 'templates/popups/sellerInfo.xml',
             'sendMessage': 'templates/popups/sendMessage.xml',
             'storeInfo': 'templates/popups/storeInfo.xml',
             'summaryUsers': 'templates/popups/summaryUsers.xml',
             'verifyEmail': 'templates/popups/verifyEmail.xml'}
