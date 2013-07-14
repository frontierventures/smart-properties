import StringIO
import json
import pycurl
import urllib

c = pycurl.Curl()
#rpcuser=bitcoinrpc:vhCbOA193pdH
#rpcpassword=
#rpcport=8332

#rpcuser=bitcoinrpc
#rpcpassword=hCbOA193pH
#rpcport=8332

c.setopt(c.USERPWD, 'bitcoinrpc:hCbOA193pH')
c.setopt(c.URL, 'http://127.0.0.1:8332/')
c.setopt(c.HTTPHEADER, ['content-type: text/plain'])


def summary():
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }'
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)
    c.perform()

    output = b.getvalue()
    output = json.loads(output)
    return output


def getNewAddress(account):
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "getnewaddress", "params": ["%s"] }' % account
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)
    c.perform()

    output = b.getvalue()
    output = json.loads(output)
    return output


def verifyMessage(bitcoinAddress, signature, message):
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "verifymessage", "params": ["%s", "%s", "%s"] }' % (str(bitcoinAddress), str(signature), str(message))
    print data

    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)
    c.perform()

    output = b.getvalue()
    #output = json.loads(output)
    return output
