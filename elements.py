#!/usr/bin/env python
from twisted.web.template import Element, renderer
from twisted.web.template import XMLString
from twisted.python .filepath import FilePath

from data import Profile
from data import db

import config
import math


class Caption(Element):
    loader = XMLString('''
                       <div xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1" t:render="caption" class="caption">
                       <t:slot name="text" />
                       </div>
                       ''')

    def __init__(self, text):
        self.text = text

    @renderer
    def caption(self, request, tag):
        return tag.fillSlots(text=self.text)


class Footer(Element):
    def __init__(self):
        self.loader = XMLString(FilePath('templates/elements/footer0.xml').getContent())


class Header(Element):
    html = [XMLString(FilePath('templates/elements/header0.xml').getContent()),
            XMLString(FilePath('templates/elements/header1.xml').getContent()),
            XMLString(FilePath('templates/elements/header2.xml').getContent())]

    def __init__(self, sessionUser):
        self.sessionUser = sessionUser
        
        if self.sessionUser['id'] == 0:
            self.loader = self.html[0]
        else:
            self.loader = self.html[1]

        if self.sessionUser['type'] == 0:
            self.loader = self.html[2]

    @renderer
    def first(self, request, tag):
        slots = {}
        slots['htmlUserFirst'] = self.sessionUser['email']
        return tag.fillSlots(**slots)


class Invite(Element):
    def __init__(self):
        self.loader = XMLString('''
                                <a href="../becomeAffiliate" xmlns:t="http://twistedmatrix.com/ns/twisted.web.template/0.1">
                                <img src="../images/affiliate-banner-small.gif" style="margin-left: 35px;"/>
                                </a>
                                ''')


class Alert(Element):
    def __init__(self, sessionResponse):
        self.sessionResponse = sessionResponse
        self.loader = XMLString(FilePath('templates/elements/notification0.xml').getContent())

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


class Options(Element):
    def __init__(self):
        self.loader = XMLString(FilePath('templates/options0.xml').getContent())


class ServerDownPage(Element):
    sessionUser = {}
    sessionSearch = {}

    def __init__(self, pageTitle):
        self.pageTitle = pageTitle
        self.loader = XMLString(FilePath('templates/pages/serverDown2.xml').getContent())
        self.loader = XMLString(FilePath('templates/pages/serverDown1.xml').getContent())

    @renderer
    def title(self, request, tag):
        slots = {}
        slots['htmlPageTitle'] = self.pageTitle
        return tag.fillSlots(**slots)
