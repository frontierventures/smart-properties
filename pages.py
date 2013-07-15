#!/usr/bin/env python
from twisted.web.template import Element, renderer, XMLString
from twisted.python.filepath import FilePath


import elements
import forms
import inbox
import login
import market
import orders
import popups
import register
import settings
import summaryOrders
import summaryProperties
import summaryUsers


class Page(Element):
    sessionOrder = {}
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


class AddProperty(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def addPropertyForm(self, request, tag):
        return forms.AddProperty(self.sessionUser, self.sessionProperty, self.sessionResponse)


class BuyProperty(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def buyPropertyForm(self, request, tag):
        return forms.BuyProperty(self.sessionResponse, self.sessionOrder)


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


class Login(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def loginForm(self, request, tag):
        return login.Form(self.sessionUser, self.sessionResponse)

    @renderer
    def recoverPasswordPopup(self, request, tag):
        return popups.RecoverPassword()


class Register(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def registerForm(self, request, tag):
        return register.Form(self.sessionUser, self.sessionResponse)


class Home(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle


class Orders(Page):
    def __init__(self, pageTitle, template, status):
        Page.__init__(self, pageTitle, template)
        self.status = status

    @renderer
    def orders(self, request, tag):
        return orders.Orders(self.sessioUser, self.status)


class Settings(Page):
    def __init__(self, pageTitle, template):
        Page.__init__(self, pageTitle, template)
        self.pageTitle = pageTitle

    @renderer
    def settingsForm(self, request, tag):
        return settings.Form(self.sessionUser, self.sessionResponse)


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
    def __init__(self, pageTitle, template, status):
        Page.__init__(self, pageTitle, template)
        self.status = status

    @renderer
    def users(self, request, tag):
        return summaryUsers.Users(self.status)


templates = {'inbox': 'templates/pages/inbox.xml',
             'login': 'templates/pages/login.xml',
             'home': 'templates/pages/home.xml',
             'addProperty': 'templates/pages/addProperty.xml',
             'buyProperty': 'templates/pages/buyProperty.xml',
             'orders': 'templates/pages/orders.xml',
             'register': 'templates/pages/register.xml',
             'settings': 'templates/pages/settings.xml',
             'summaryProperties': 'templates/pages/summaryProperties.xml',
             'summaryOrders': 'templates/pages/summaryOrders.xml',
             'summaryUsers': 'templates/pages/summaryUsers.xml'}
