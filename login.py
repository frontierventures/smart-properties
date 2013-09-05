#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.python.filepath import FilePath
from twisted.web.template import Element, renderer, renderElement, XMLString

from data import Profile, User
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
        sessionUser['page'] = 'login'

        if sessionUser['id'] >= 1:
            return redirectTo('../', request)

        sessionResponse = SessionManager(request).getSessionResponse()
        if request.args.get('verify'):
            verify = request.args.get('verify')[0]
            if verify == 'ok':
                sessionResponse = {'class': 2, 'form': 0, 'text': definitions.VERIFY_SUCCESS}

        Page = pages.Login('Smart Property Group - Login', 'login')
        Page.sessionUser = sessionUser
        Page.sessionResponse = sessionResponse

        print "%ssessionUser: %s%s" % (config.color.YELLOW, sessionUser, config.color.ENDC)
        print "%ssessionResponse: %s%s" % (config.color.YELLOW, sessionResponse, config.color.ENDC)
        SessionManager(request).clearSessionResponse()
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


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


def makeSession(request, userId):
    SessionManager(request).add()

    user = db.query(User).filter(User.id == userId).first()
    user.loginTimestamp = config.createTimestamp()
    user.ip = request.getClientIP()
    db.commit()

    profile = db.query(Profile).filter(Profile.userId == userId).first()
    isEmailVerified = user.isEmailVerified

    if isEmailVerified == 0:
        isEmailVerified = False

    if isEmailVerified == 1:
        isEmailVerified = True

    sessionUser = SessionManager(request).getSessionUser()
    sessionUser['id'] = user.id
    sessionUser['type'] = user.type
    sessionUser['ip'] = user.ip
    sessionUser['status'] = user.status 
    sessionUser['isEmailVerified'] = isEmailVerified
    sessionUser['first'] = profile.first
    sessionUser['last'] = profile.last
    sessionUser['loginTimestamp'] = config.createTimestamp()
