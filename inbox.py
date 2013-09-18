#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo
from twisted.web.template import Element, renderer, renderElement, XMLString
from twisted.python.filepath import FilePath

from data import Message, Profile, User
from data import db
from sqlalchemy.sql import and_
from sessions import SessionManager

import elements
import config
import definitions
import json
import mailer
import pages
import re

Email = mailer.Email


class Main(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).getSessionUser()
        session_user['page'] = 'settings'
        userId = session_user['id']
        if userId == 0:
            return redirectTo('../', request)

        session_user = SessionManager(request).getSessionUser()
        session_user['page'] = 'inbox'

        sessionSearch = SessionManager(request).getSessionSearch()
        sessionSearch['isTabOpen'] = False
        sessionProduct = SessionManager(request).getSessionProduct()
        sessionOrder = SessionManager(request).getSessionOrder()

        sessionResponse = SessionManager(request).getSessionResponse()

        Page = pages.Inbox('Coingig.com - Inbox', 'inbox')
        Page.session_user = session_user

        print "%ssession_user: %s%s" % (config.color.BLUE, session_user, config.color.ENDC)
        print "sessionProduct: %s" % sessionProduct
        print "sessionOrder: %s" % sessionOrder
        print "sessionResponse: %s" % sessionResponse
        SessionManager(request).clearSessionResponse()
        SessionManager(request).clearSessionProduct()
        request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page)


class Form(Element):
    def __init__(self, session_user):
        self.session_user = session_user
        self.userId = session_user['id']

        messages = db.query(Message).filter(and_(
            Message.receiverId == self.userId,
            Message.status != 'deleted')).order_by(Message.timestamp.desc())

        if messages.count() == 0:
            template = 'templates/messages0.xml'
        else:
            template = 'templates/messages1.xml'

        self.loader = XMLString(FilePath(template).getContent())
        self.messages = messages

    @renderer
    def menu(self, request, tag):
        return elements.TabCell(self.session_user, 3)

    @renderer
    def row(self, request, tag):
        for message in self.messages:
            self.messageId = str(message.id)
            self.senderId = str(message.senderId)

            slots = {}
            slots['htmlId'] = str(message.id)
            slots['htmlTimestamp'] = config.convertTimestamp(float(message.timestamp))
            slots['htmlSender'] = str(message.senderId)

            style = ''
            if message.status == 'unread':
                style = 'font-weight: bold;'

            slots['htmlStyle'] = style
            slots['htmlSubject'] = '%s' % str(message.subject)
            slots['htmlName'] = str(message.name)
            yield tag.clone().fillSlots(**slots)

    @renderer
    def action(self, request, tag):
        messageId = self.messageId
        actions = {}
        actions[config.createTimestamp()] = ['Reply', 'ticon edit hint hint--top hint--rounded', '../sendMessage']
        actions[config.createTimestamp()] = ['Delete Message', 'ticon remove hint hint--top hint--rounded', '../deleteMessage?id=%s' % messageId]

        for key in sorted(actions.keys()):
            slots = {}
            slots['htmlId'] = str(messageId)
            slots['htmlHint'] = actions[key][0]
            slots['htmlClass'] = actions[key][1]
            slots['htmlUrl'] = actions[key][2]
            newTag = tag.clone().fillSlots(**slots)
            yield newTag


class Send(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        #sessionReview = SessionManager(request).getSessionReview()
        #sessionReview['id'] = int(request.args.get('reviewId')[0])

        receiverId = request.args.get('messageReceiverId')[0]
        senderId = request.args.get('messageSenderId')[0]
        name = request.args.get('messageName')[0]
        subject = request.args.get('messageSubject')[0]
        #sessionReview['headline'] = reviewHeadline

        body = request.args.get('messageBody')[0]
        #sessionReview['body'] = reviewBody
        #SessionManager(request).setSessionReview(sessionReview)

        if not subject:
            return json.dumps(dict(response=0, text=definitions.MESSAGE_SUBJECT[0]))
        elif not re.match(definitions.REGEX_MESSAGE_SUBJECT, subject):
            return json.dumps(dict(response=0, text=definitions.MESSAGE_SUBJECT[1]))

        if not body:
            return json.dumps(dict(response=0, text=definitions.MESSAGE_BODY[0]))

        timestamp = config.createTimestamp()
        parentId = 0
        newMessage = Message(parentId, 'unread', timestamp, receiverId, senderId, name, subject, body)
        #def __init__(self, parentId, status, timestamp, receiverId, senderId, subject, body):
        db.add(newMessage)
        db.commit()

        return json.dumps(dict(response=1, text=definitions.UPDATE_SUCCESS))


class SendMessage(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        if not request.args:
            return redirectTo('../', request)

        #session_user = SessionManager(request).getSessionUser()
        receiverId = request.args.get('messageReceiverId')[0]
        senderId = request.args.get('messageSenderId')[0]
        subject = request.args.get('messageSubject')[0]
        body = request.args.get('messageBody')[0]

        if not subject:
            return json.dumps(dict(response=0, text=definitions.SUBJECT[0]))
        elif not re.match(definitions.REGEX_SUBJECT, subject):
            return json.dumps(dict(response=0, text=definitions.SUBJECT[1]))

        if not body:
            return json.dumps(dict(response=0, text=definitions.BODY[0]))
        elif not re.match(definitions.REGEX_BODY, body):
            return json.dumps(dict(response=0, text=definitions.BODY[1]))

        sender = db.query(Profile).filter(Profile.userId == senderId).first()

        timestamp = config.createTimestamp()
        parentId = 0
        newMessage = Message(parentId, 'unread', timestamp, receiverId, senderId, sender.first, subject, body)
        db.add(newMessage)
        profile = db.query(Profile).filter(Profile.userId == receiverId).first()
        profile.unreadCount += 1
        db.commit()
        user = db.query(User).filter(User.id == receiverId).first()

        plain = mailer.messageMemoPlain(profile)
        html = mailer.messageMemoHtml(profile)
        Email(mailer.noreply, user.email, 'You have a new message at Coingig.com!', plain, html).send()

        return json.dumps(dict(response=1, text=definitions.MESSAGE_SUCCESS))


class DeleteOne(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)

        session_user = SessionManager(request).getSessionUser()
        userId = session_user['id']
        if userId == 0:
            return redirectTo('../', request)

        messageId = ''
        try:
            messageId = int(request.args.get('id')[0])
        except:
            return redirectTo('../', request)

        message = db.query(Message).filter(Message.id == messageId).first()
        profile = db.query(Profile).filter(Profile.id == userId).first()

        if message.status == 'unread':
            profile.unreadCount -= 1

        message.status = "deleted"
        db.commit()
        return redirectTo('../inbox', request)


class DeleteMany(Resource):
    def render(self, request):
        print '%srequest.args: %s%s' % (config.color.RED, request.args, config.color.ENDC)
        if not request.args:
            return redirectTo('../inbox', request)

        session_user = SessionManager(request).getSessionUser()
        userId = session_user['id']
        if userId == 0:
            return redirectTo('../', request)

        profile = db.query(Profile).filter(Profile.id == userId).first()
        messageIds = request.args.get('messageIds')

        for messageId in messageIds:
            print messageId
            message = db.query(Message).filter(Message.id == messageId).first()
            if message.status == 'unread':
                profile.unreadCount -= 1
            message.status = "deleted"
        db.commit()
        return redirectTo('../inbox', request)
