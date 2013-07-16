#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET

from data import Price
from data import db
from sessions import SessionManager
import config
import definitions


class Main(Resource):
    def render(self, request):
        request.write("<!DOCTYPE html>\n")
        request.write("<html>\n")
        request.write("<head>\n")
        request.write("</head>\n")
        request.write("<body>\n")
        timestamp = config.createTimestamp()
        prices = db.query(Price).order_by(Price.timestamp.desc())
        request.write("<table style=\"width: 100%\">\n")
        request.write("<tr>\n")
        request.write("<td><b>Timestamp</b></td>\n")
        request.write("<td><b>Currency</b></td>\n")
        request.write("<td><b>Last</b></td>\n")
        request.write("<td><b>Delay</b></td>\n")
        request.write("<td><b>Status</b></td>\n")
        request.write("</tr>\n")

        for price in prices:
            request.write("<tr>\n")
            request.write("<td>%s</td>\n" % str(config.convertTimestamp(float(price.timestamp))))
            request.write("<td>%s</td>\n" % str(price.currencyId))
            request.write("<td>%s</td>\n" % str(price.last))
            delta = timestamp - float(price.timestamp)
            request.write("<td>%s</td>\n" % str(delta))
            if delta > 30:
                request.write("<td bgcolor='red'>Delayed</td>\n")
            else:
                request.write("<td bgcolor='green'>Current</td>\n")

            #request.write("<td>%s</td>\n" % str(config.convertTimestamp(float(delta))))
            request.write("</tr>\n")
        request.write("</table>\n")
        request.write("</body>\n")
        request.write("</html>\n")
        request.finish()
        return NOT_DONE_YET
