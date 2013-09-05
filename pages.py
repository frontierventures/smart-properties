#!/usr/bin/env python
from twisted.web.template import Element, renderer, XMLString
from twisted.python.filepath import FilePath

import account
import assets
import contract
import elements
import faq
import forms
import history
import inbox
import legal
import lend
import login
import orders
import popups
import profile
import receipt
import register
import settings
import signature
import summaryOrders
import summaryProperties
import summaryUsers
import summaryTransactions


class Page(Element):
    sessionOrder = {}
    sessionTransaction = {}
    sessionProperty = {}
    sessionResponse = {}
    sessionReview = {}
    sessionUser = {}

    def __init__(self, pageTitle, template):
        self.pageTitle = pageTitle
        self.loader = XMLString(FilePath(templates[template]).getContent())

    @renderer
    def title(self, request, tag):
        slots = {}
        slots['htmlPageTitle'] = self.pageTitle
        return tag.fillSlots(**slots)

    @renderer
    def header(self, request, tag):
        return elements.Header(self.sessionUser)

    @renderer
    def footer(self, request, tag):
        return elements.Footer()

    @renderer
    def helpPopup(self, request, tag):
        return popups.Help()


class Account(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def details(self, request, tag):
        return account.Details(self.sessionUser)


class AddProperty(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def addPropertyForm(self, request, tag):
        return forms.AddProperty(self.sessionUser, self.sessionProperty, self.sessionResponse)


class Assets(Page):
    def __init__(self, pageTitle, template, status):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle
        self.status = status

    @renderer
    def assets(self, request, tag):
        return assets.Assets(self.status)


class BuyProperty(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def buyPropertyForm(self, request, tag):
        return forms.BuyProperty(self.sessionResponse, self.sessionOrder)


class Contract(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def contractForm(self, request, tag):
        return forms.Contract(self.sessionUser, self.sessionResponse, self.sessionTransaction)


class FAQ(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def details(self, request, tag):
        return faq.Details(self.sessionUser)


class Inbox(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)

    @renderer
    def messages(self, request, tag):
        return inbox.Form(self.sessionUser)

    @renderer
    def messagePopup(self, request, tag):
        return popups.Message()

    @renderer
    def sendMessagePopup(self, request, tag):
        return popups.SendMessage(self.sessionUser)


class History(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def transactions(self, request, tag):
        return history.Transactions(self.filters, self.sessionUser)


class Home(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle


class Lend(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def loanAmountForm(self, request, tag):
        return forms.LendAmount(self.sessionResponse, self.sessionTransaction)


class Legal(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def details(self, request, tag):
        return legal.Details(self.sessionUser)


class Login(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def loginForm(self, request, tag):
        return forms.Login(self.sessionUser, self.sessionResponse)

    @renderer
    def recoverPasswordPopup(self, request, tag):
        return popups.RecoverPassword()


class Orders(Page):
    def __init__(self, pageTitle, template, status):
        Page.__init__(self, pageTitle, template)
        self.status = status

    @renderer
    def orders(self, request, tag):
        return orders.Orders(self.sessionUser, self.status)


class Profile(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)

    @renderer
    def details(self, request, tag):
        return profile.Details(self.sessionUser)


class Register(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def registerForm(self, request, tag):
        return forms.Register(self.sessionUser, self.sessionResponse)


class Settings(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def settingsForm(self, request, tag):
        return settings.Form(self.sessionUser, self.sessionResponse)


class Signature(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def signatureForm(self, request, tag):
        return forms.Signature(self.sessionUser, self.sessionResponse)


class Receipt(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)

    @renderer
    def receipt(self, request, tag):
        return receipt.Receipt(self.sessionTransaction)


class SummaryProperties(Page):
    def __init__(self, pageTitle, template, status):
        Page.__init__(self, pageTitle, template)
        self.status = status

    @renderer
    def users(self, request, tag):
        return summaryProperties.Properties(self.status)


class SummaryOrders(Page):
    def __init__(self, pageTitle, template, status):
        Page.__init__(self, pageTitle, template)
        self.status = status

    @renderer
    def orders(self, request, tag):
        return summaryOrders.Orders(self.status)


class SummaryUsers(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def users(self, request, tag):
        return summaryUsers.Users(self.filters)


class SummaryTransactions(Page):
    def __init__(self, pageTitle, template, filters):
        Page.__init__(self, pageTitle, template)
        self.filters = filters

    @renderer
    def transactions(self, request, tag):
        return summaryTransactions.Transactions(self.filters, self.sessionUser)


templates = {'inbox': 'templates/pages/inbox.xml',
             'contract': 'templates/pages/contract.xml',
             'legal': 'templates/pages/legal.xml',
             'faq': 'templates/pages/faq.xml',
             'lend': 'templates/pages/lend.xml',
             'login': 'templates/pages/login.xml',
             'account': 'templates/pages/account.xml',
             'history': 'templates/pages/history.xml',
             'home': 'templates/pages/home.xml',
             'assets': 'templates/pages/assets.xml',
             'addProperty': 'templates/pages/addProperty.xml',
             'buyProperty': 'templates/pages/buyProperty.xml',
             'orders': 'templates/pages/orders.xml',
             'profile': 'templates/pages/profile.xml',
             'register': 'templates/pages/register.xml',
             'receipt': 'templates/pages/receipt.xml',
             'settings': 'templates/pages/settings.xml',
             'signature': 'templates/pages/signature.xml',
             'summaryProperties': 'templates/pages/summaryProperties.xml',
             'summaryOrders': 'templates/pages/summaryOrders.xml',
             'summaryTransactions': 'templates/pages/summaryTransactions.xml',
             'summaryUsers': 'templates/pages/summaryUsers.xml'}
