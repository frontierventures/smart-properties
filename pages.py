#!/usr/bin/env python
from twisted.web.template import Element, renderer, XMLString
from twisted.python.filepath import FilePath


import elements
import inbox
import login
import market
import popups
import register
import summaryUsers


class Page(Element):
    sessionOrder = {}
    sessionProduct = {}
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


class SummaryUsers(Page):
    def __init__(self, pageTitle, template, status):
        Page.__init__(self, pageTitle, template)
        self.status = status

    @renderer
    def users(self, request, tag):
        return summaryUsers.Users(self.status)

    @renderer
    def describeUserPopup(self, request, tag):
        return popups.DescribeUser()

    @renderer
    def summaryUsersPopup(self, request, tag):
        return popups.SummaryUsers()


templates = {'inbox': 'templates/pages/inbox.xml',
             'login': 'templates/pages/login.xml',
             'home': 'templates/pages/home.xml',
             'register': 'templates/pages/register.xml',
             'summaryUsers': 'templates/pages/summaryUsers.xml'}
