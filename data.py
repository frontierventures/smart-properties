#! /usr/bin/python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref

import config
import encryptor
import definitions
import decimal
D = decimal.Decimal

engine = create_engine('sqlite:///database/spi.db', echo=False)
Session = sessionmaker(bind=engine)
db = Session()


Base = declarative_base()


class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    entry = Column(String)

    def __init__(self, data):
        self.timestamp = data['timestamp']
        self.entry = data['entry']


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    parentId = Column(Integer)
    status = Column(String)
    timestamp = Column(String)
    receiverId = Column(Integer)
    senderId = Column(Integer)
    name = Column(String)
    subject = Column(String)
    body = Column(String)

    def __init__(self, data):
        self.parentId = data['parentId']
        self.status = data['status']
        self.timestamp = data['timestamp']
        self.receiverId = data['receiverId']
        self.senderId = data['senderId']
        self.name = data['name']
        self.subject = data['subject']
        self.body = data['body']


class Newsletter(Base):
    __tablename__ = "newsletters"
    id = Column(Integer, primary_key=True)
    status = Column(String)
    timestamp = Column(String)
    authorId = Column(Integer)
    title = Column(String)
    body = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.timestamp = data['timestamp']
        self.authorId = data['authorId']
        self.title = data['title']
        self.body = data['body']


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    status = Column(String)
    createTimestamp = Column(String)
    updateTimestamp = Column(String)
    propertyId = Column(Integer)
    propertyTitle = Column(String)
    units = Column(Integer)
    pricePerUnit = Column(String)
    lenderId = Column(Integer)
    total = Column(String)
    paymentAddress = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.createTimestamp = data['createTimestamp']
        self.updateTimestamp = data['updateTimestamp']
        self.propertyId = data['propertyId']
        self.propertyTitle = data['propertyTitle']
        self.units = data['units']
        self.pricePerUnit = data['pricePerUnit']
        self.lenderId = data['lenderId']
        self.total = data['total']
        self.paymentAddress = data['paymentAddress']


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    currencyId = Column(Integer)
    last = Column(String)

    def __init__(self, data):
        self.timestamp = data['timestamp']
        self.currencyId = data['currencyId']
        self.last = data['last']


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    createTimestamp = Column(String)
    updateTimestamp = Column(String)
    first = Column(String)
    last = Column(String)
    token = Column(String)
    bitcoinAddress = Column(String)
    seed = Column(String)
    balance = Column(String)
    unreadMessages = Column(Integer)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref=backref("profiles", order_by=id))

    def __init__(self, data):
        self.createTimestamp = data['createTimestamp']
        self.updateTimestamp = data['updateTimestamp']
        self.first = data['first']
        self.last = data['last']
        self.token = data['token']
        self.bitcoinAddress = data['bitcoinAddress']
        self.seed = data['seed']
        self.balance = data['balance']
        self.unreadMessages = data['unreadMessages']


class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    status = Column(String)
    createTimestamp = Column(String)
    updateTimestamp = Column(String)
    title = Column(String(collation='NOCASE'))
    description = Column(String)
    address =  Column(String)
    mls = Column(String)
    siteSize = Column(String)
    totalUnits = Column(String)
    askingPrice = Column(String)
    imageCount = Column(Integer)
    imageHash = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.createTimestamp = data['createTimestamp']
        self.updateTimestamp = data['updateTimestamp']
        self.title = data['title']
        self.description = data['description']
        self.address = data['address']
        self.mls = data['mls']
        self.siteSize = data['siteSize']
        self.totalUnits = data['totalUnits']
        self.askingPrice = data['askingPrice']
        self.imageCount = data['imageCount']
        self.imageHash = data['imageHash']


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    status = Column(String)
    createTimestamp = Column(String)
    updateTimestamp = Column(String)
    userId = Column(Integer)
    amount = Column(String)
    bitcoinAddress = Column(String)
    statement = Column(String)
    signature = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.createTimestamp = data['createTimestamp']
        self.updateTimestamp = data['updateTimestamp']
        self.userId = data['userId']
        self.amount = data['amount']
        self.bitcoinAddress = data['bitcoinAddress']
        self.statement = data['statement']
        self.signature = data['signature']


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    status = Column(String)
    type = Column(Integer)
    loginTimestamp = Column(String)
    email = Column(String(collation="NOCASE"))
    password = Column(String)
    isEmailVerified = Column(Integer)
    ip = Column(String)

    def __init__(self, data):
        self.status = data['status']
        self.type = data['type']
        self.loginTimestamp = data['loginTimestamp']
        self.email = data['email']
        self.password = data['password']
        self.isEmailVerified = data['isEmailVerified']
        self.ip = data['ip']


def reset():
    Base.metadata.create_all(engine)

    timestamp = config.createTimestamp()

    for currency in definitions.currencies:
        price = db.query(Price).filter(Price.currencyId == currency).first()
        if not price:
            newPrice = Price(timestamp, currency, 1)
            db.add(newPrice)

    user = db.query(User).filter(User.email == '0@0.0').first()
    if not user:
        password = encryptor.hashPassword("0")
        admin = User('verified', 0, timestamp, '0@0.0', password, 1, '')
        newProfile = Profile(timestamp, timestamp, 'admin', 'admin', '', '', '', 135000, 0)
        admin.profiles = [newProfile]
        db.add(admin)

    db.commit()

reset()
