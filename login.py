#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString

from data import User
from data import db
from sessions import SessionManager

import activity
import elements
import config
import definitions
import functions
import encryptor
import error
import json
import mailer
import pages
import random
import re
import string

Email = mailer.Email


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        sessionUser = SessionManager(request).getSessionUser()
        userId = sessionUser['id']

        if userId >= 1:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()
        if request.args.get('verify'):
            verify = request.args.get('verify')[0]
            if verify == 'ok':
                sessionResponse = {'class': 2, 'form': 0, 'text': definitions.VERIFY_SUCCESS}

        Page = pages.Login('Login', 'login')
        Page.sessionUser = sessionUser
        Page.sessionResponse = sessionResponse

        print "%ssessionUser: %s%s" % (config.color.BLUE, sessionUser, config.color.ENDC)
        print "sessionResponse: %s" % sessionResponse
        SessionManager(request).clearSessionResponse()
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Form(Element):
    def __init__(self, sessionUser, sessionResponse):
        self.sessionUser = sessionUser
        self.sessionResponse = sessionResponse
        self.loader = XMLString(FilePath('templates/forms/loginForm.xml').getContent())

    @renderer
    def form(self, request, tag):
        sessionUser = self.sessionUser
        userEmail = ''
        if sessionUser.get('email'):
            userEmail = sessionUser['email']

        userPassword = ''
        if sessionUser.get('password'):
            userPassword = sessionUser['password']

        slots = {}
        slots['htmlEmail'] = userEmail
        slots['htmlPassword'] = userPassword
        yield tag.fillSlots(**slots)

    @renderer
    def notification(self, request, tag):
        sessionResponse = self.sessionResponse
        if not sessionResponse['text']:
            return []
        else:
            return commonElements.Notification(sessionResponse)


class Action(Resource):
    def __init__(self, echoFactory):
        self.echoFactory = echoFactory

    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        userEmail = request.args.get('userEmail')[0]
        userPassword = request.args.get('userPassword')[0]

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['email'] = userEmail
        sessionUser['password'] = userPassword

        if error.email(request, userEmail):
            return redirectTo('../login', request)

        if error.password(request, userPassword):
            return redirectTo('../login', request)

        users = db.query(User).filter(User.email == userEmail)
        user = users.filter(User.status == 'active').first()
        if not user:
            SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.EMAIL[2]})
            return redirectTo('../login', request)

        if request.args.get('button')[0] == 'Login':
            if encryptor.checkPassword(user.password, userPassword):
                userType = user.type
                isEmailVerified = user.isEmailVerified

                if isEmailVerified == 0:
                    isEmailVerified = False

                if isEmailVerified == 1:
                    isEmailVerified = True

                if userType == 1:
                    url = '../'

                if userType > 1:
                    store = db.query(StoreDirectory).filter(StoreDirectory.ownerId == user.id).first()
                    url = '../%s' % store.name

                if not isEmailVerified:
                    url = '../settings'

                if userType == 0:
                    url = '../summaryUsers'

                functions.makeLogin(request, user.id)
                SessionManager(request).setSessionResponse({'class': 2, 'form': 0, 'text': definitions.SUCCESS_LOGIN})

                email = str(user.email)

                activity.pushToSocket(self.echoFactory, '%s**** logged in' % email[0])
                activity.pushToDatabase('%s logged in' % email)

                url = str(url)
                return redirectTo(url, request)
            else:
                SessionManager(request).setSessionResponse({'class': 1, 'form': 0, 'text': definitions.PASSWORD[2]})
                return redirectTo('../login', request)


class RecoverPassword(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        sessionUser = SessionManager(request).getSessionUser()
        sessionUser['userEmail'] = request.args.get('userEmail')[0]
        #SessionManager(request).setSessionUser(sessionUser)

        userEmail = sessionUser['userEmail']
        #request.setSessionResponseCode(200)

        if not userEmail:
            return json.dumps(dict(response=0, text=definitions.EMAIL[0]))
        elif not re.match(definitions.REGEX_EMAIL, userEmail):
            return json.dumps(dict(response=0, text=definitions.EMAIL[1]))

        user = db.query(User).filter(User.email == userEmail).first()
        if not user:
            return json.dumps(dict(response=0, text=definitions.EMAIL[2]))

        password = ''.join(random.sample(string.digits, 5))
        user.password = encryptor.hashPassword(password)
        db.commit()

        plain = mailer.passwordRecoveryPlain(userEmail, password)
        html = mailer.passwordRecoveryHtml(userEmail, password)
        Email(mailer.noreply, userEmail, 'Your  password was reset!', plain, html).send()

        return json.dumps(dict(response=1, text=definitions.PASSWORD[3]))
