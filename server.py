from twisted.application.service import Application
from twisted.internet import protocol
from twisted.application import internet
from txws import WebSocketFactory
from twisted.web.server import Request, Site, Session
from twisted.web.static import File
from twisted.python import log


import market
import config
import login
import logout
import register
import summaryUsers


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

root = market.Main(echoFactory)
root.putChild('', root)

def assemble(root):
    root.putChild('login', login.Main())
    root.putChild('loginAction', login.Action(echoFactory))
    root.putChild('logout', logout.Main())
    root.putChild('register', register.Main())
    root.putChild('summaryUsers', summaryUsers.Main())
    return root

root = assemble(root)

site = XForwardedForSite(root)
site.sessionFactory = ShortSession
httpService = internet.TCPServer(8080, site)
httpService.setServiceParent(application)
