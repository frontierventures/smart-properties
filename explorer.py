import StringIO
import json
import pycurl
import urllib

c = pycurl.Curl()
c.setopt(c.USERPWD, 'bitcoinrpc:hCbOA193pH')
c.setopt(c.URL, 'http://127.0.0.1:8332/')
c.setopt(c.HTTPHEADER, ['content-type: text/plain'])


def summary():
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }'
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)

    try:
        c.perform()
        output = b.getvalue()
        output = json.loads(output)
    except Exception as e:
        print e
        output = ''
    print output
    return output


def getNewAddress(account):
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "getnewaddress", "params": ["%s"] }' % account
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)

    try:
        c.perform()
        output = b.getvalue()
        output = json.loads(output)
    except Exception as e:
        print e
        output = ''

    print output
    return output


def verifyMessage(bitcoinAddress, signature, message):
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "verifymessage", "params": ["%s", "%s", "%s"] }' % (bitcoinAddress, signature, message)
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)

    try:
        c.perform()
        output = b.getvalue()
        output = json.loads(output)
    except Exception as e:
        print e
        output = ''

    print output
    return output


address = '17EoJsYcb5nPMLkjv92W85n2nr2pBzUrjE'
message = '''This is a message'''
message = ''
signature = 'IGgHKI8dvS5T1ubYWW/zLRq0Pa63y1/7xy9rMn6z8q8+cRuri5nsidw6YEEXgdDwDlWD0fY49pw0/6+WWj1lyNM='

signature = 'IiGgHKI8dvS5T1ubYWW/zLRq0Pa63y1/7xy9rMn6z8q8+cRuri5nsidw6YEEXgdDwDlWD0fY49pw0/6+WWj1lyNM='

verifyMessage(address, signature, message)
#{u'id': u'curltest', u'result': None, u'error': {u'message': u'Invalid address', u'code': -3}}
#verifymessage <bitcoinaddress> <signature> <message>
