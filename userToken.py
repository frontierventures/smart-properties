#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo

from data import Profile, User
from data import db
from sessions import SessionManager

import config
import definitions
import mailer
import sessions

Email = mailer.Email


class Verify(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        if request.args.get('id') and request.args.get('token'):
            try:
                userId = int(request.args.get('id')[0])
            except:
                return redirectTo('../', request)

            try:
                token = request.args.get('token')[0]
            except:
                return redirectTo('../', request)

            profile = db.query(Profile).filter(Profile.userId == userId).first()
            if not profile:
                return redirectTo('../', request)

            if profile.token == token:
                user = db.query(User).filter(User.id == userId).first()
                user.isEmailVerified = 1
                user.status = 'verified'
                profile.token = ''
                db.commit()
                sessions.disconnect(request, userId)
                SessionManager(request).setSessionResponse({'class': 2, 'form': 0, 'text': definitions.VERIFY_SUCCESS})
                return redirectTo('../login?verify=ok', request)
            else:
                return redirectTo('../', request)


class Send(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).getSessionUser()
        userId = session_user['id']

        user = db.query(User).filter(User.id == userId).first()
        profile = db.query(Profile).filter(Profile.userId == userId).first()

        url = 'http://www.sptrust.co/verifyEmail?id=%s&token=%s' % (str(userId), profile.token)
        plain = mailer.verificationPlain(url)
        html = mailer.verificationHtml(url)
        Email(mailer.noreply, user.email, 'Smart Property Group - Email Verification Instructions', plain, html).send()

        SessionManager(request).setSessionResponse({'class': 2, 'form': 0, 'text': definitions.UNDEF})
        return redirectTo('../account', request)
