#!/usr/bin/env python
from twisted.web.resource import Resource
from twisted.web.util import redirectTo

from data import db

import config


class Main(Resource):
    isLeaf = True

    def __init__(self, sellerId):
        Resource.__init__(self)
        self.sellerId = sellerId

    def render(self, request):
        url = '../'
        return redirectTo(url, request)
