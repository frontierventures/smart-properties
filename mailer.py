#! /usr/bin/python
from smtplib import SMTP
from smtplib import SMTPException

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Utils import COMMASPACE, formatdate

from data import db

import definitions
import decimal
D = decimal.Decimal

noreply = ''
fromNoReply = ''
ordersBox = ''


class Email():
    def __init__(self, sender, receiver, subject, plain, html):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.plain = plain
        self.html = html

    def send(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = 'Smart Property Group <noreply@sptrust.co>'
        msg['To'] = self.receiver
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject

        part1 = MIMEText(self.plain, 'plain')
        part2 = MIMEText(self.html, 'html')

        msg.attach(part1)
        msg.attach(part2)

        try:
            smtp = SMTP('smtp.mailgun.org', 587)
            smtp.ehlo()
            smtp.starttls()
            #need pass
            smtp.login('noreply@sptrust.co', 'noreply123noreply')
            smtp.sendmail(self.sender, self.receiver, msg.as_string())
            smtp.quit()

            print 'Success: %s %s' % (self.sender, self.receiver)
        except SMTPException as e:
            print 'Fail: %s %s' % (self.sender, self.receiver)
            print e


def messageMemoPlain(profile):
    plain = """
    You have %s message(s).\n
    Please visit the link below to check your inbox.\n
    http://www.coingig.com/login\n
    Coingig Team
    """ % profile.unreadCount
    return plain


def messageMemoHtml(profile):
    html = """
    <html>
    <head></head>
    <body>
    <p><b>You have %s message(s).</b></p>
    <p>Please visit the link below to check your inbox.</p>
    <p><a href="http://www.coingig.com/login">Login Here</a></p>
    <p><b>Coingig Team</b></p>
    </body>
    </html>
    """ % profile.unreadCount
    return html


def verificationPlain(url):
    plain = """
    Thank you for registering!\n
    You can now take the steps to become a Smart Property Group investor!\n
    Please visit the link below to verify your email address.\n
    %s/n
    Smart Property Group 
    """ % url
    return plain


def verificationHtml(url):
    html = """
    <html>
    <p><b>Thank you for registering!</b></p>
    <p>You can now take the steps to become a Smart Property Group investor!</p>
    <p>Please visit the link below to verify your email address.</p>
    <p><a href="%s">Verify Email</a></p>
    <p><b>Smart Property Group</b></p>
    </html>
    """ % url
    return html


def passwordRecoveryPlain(email, password):
    plain = """Account Details\nEmail:  %s\nTemporary Password: %s\nCoingig Team""" % (email, password)
    return plain


def passwordRecoveryHtml(email, password):
    html = """\
    <html>
    <p><h2>Account Details</h2></p>
    <p><b>Email:</b> %s</p>
    <p><b>Temporary Password:</b> %s</p>
    <p><b>Coingig Team</b></p>
    </html>
    """ % (email, password)
    return html


def invitationPlain(email, password):
    plain = """
    Account Details\n
    Email: %s\n
    Temporary Password: %s\n
    Coingig Team
    """ % (email, password)
    return plain


def invitationHtml(email, password):
    html = """
    <html>
    <p>
    <h2>Account Details</h2>
    </p>
    <p><b>Email:</b> %s</p>
    <p><b>Temporary Password:</b> %s</p>
    <p><b>Coingig Team</b></p>
    </html>
    """ % (email, password)
    return html
