from twisted.application.service import Application
from twisted.internet import protocol
from twisted.application import internet
from txws import WebSocketFactory
from twisted.web.server import Request, Site, Session
from twisted.web.static import File
from twisted.python import log

import account
import actions
import contract
import config
import exchange
import faq
import history
import home
import legal
import lend
import login
import logout
import assets
import orders
import profile
import receipt
import register
import settings
import signature
import summaryOrders
import summaryProperties
import summaryUsers
import summaryTransactions
import userToken


class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        #log.msg("Got %r" % (data,))
        #self.transport.write(data.upper())
        self.transport.write(data)


class EchoFactory(protocol.Factory):
    protocol = EchoProtocol
    connectedProtocols = []

    def buildProtocol(self, address):
        connectedProtocol = protocol.Factory.buildProtocol(self, address)
        self.connectedProtocols.append(connectedProtocol)
        return connectedProtocol


class XForwardedForRequest(Request):
    def getClientIP(self):
        "If there's an X-Forwarded-For, treat that as the client IP."
        forwarded_for = self.getHeader('X-Real-IP')
        if forwarded_for is not None:
            return forwarded_for
        else:
            return Request.getClientIP(self)


class XForwardedForSite(Site):
    requestFactory = XForwardedForRequest


class ShortSession(Session):
    sessionTimeout = 600

application = Application("")
echoFactory = EchoFactory()
factory = WebSocketFactory(echoFactory)

wsService = internet.TCPServer(8090, factory)
wsService.setServiceParent(application)

root = home.Main(echoFactory)
root.putChild('', root)

def assemble(root):
    #PAGES
    root.putChild('account', account.Main())
    root.putChild('contract', contract.Main())
    root.putChild('history', history.Main())
    root.putChild('login', login.Main())
    root.putChild('signature', signature.Main())

    #POST ACTIONS
    root.putChild('contractAction', actions.Finalize())
    root.putChild('loginAction', actions.Login(echoFactory))
    root.putChild('registerAction', actions.Register(echoFactory))
    root.putChild('validateBitcoinAddress', actions.ValidateBitcoinAddress(echoFactory))
    root.putChild('lendAction', actions.Lend())

    #GET ACTIONS
    root.putChild('sendToken', userToken.Send())
    root.putChild('updateTransaction', actions.UpdateTransaction())
    root.putChild('verifyEmail', userToken.Verify())

    root.putChild('legal', legal.Main())
    root.putChild('faq', faq.Main())
    root.putChild('lend', lend.Main())
    root.putChild('logout', logout.Main())
    root.putChild('register', register.Main())
    root.putChild('settings', settings.Main())
    root.putChild('orders', orders.Main())
    root.putChild('profile', profile.Main())
    root.putChild('receipt', receipt.Main())
    root.putChild('summaryProperties', summaryProperties.Main())
    root.putChild('summaryOrders', summaryOrders.Main())
    root.putChild('summaryUsers', summaryUsers.Main())
    root.putChild('summaryTransactions', summaryTransactions.Main())
    root.putChild('verifyMessage', settings.Action(echoFactory))
    root.putChild('addProperty', actions.AddProperty())
    root.putChild('buyProperty', actions.BuyProperty())
    root.putChild('exchange', exchange.Main())
    root.putChild('assets', assets.Main())

    root.putChild('resources', File("./resources"))
    root.putChild('images', File("./images"))
    root.putChild('files', File("./files"))
    return root

root = assemble(root)

site = XForwardedForSite(root)
site.sessionFactory = ShortSession
httpService = internet.TCPServer(8080, site)
httpService.setServiceParent(application)
