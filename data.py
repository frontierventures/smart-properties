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

    def __init__(self, timestamp, entry):
        self.timestamp = timestamp
        self.entry = entry


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

    def __init__(self, parentId, status, timestamp, receiverId, senderId, name, subject, body):
        self.parentId = parentId
        self.status = status
        self.timestamp = timestamp
        self.receiverId = receiverId
        self.senderId = senderId
        self.name = name
        self.subject = subject
        self.body = body


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
    investorId = Column(Integer)
    total = Column(String)
    paymentAddress = Column(String)

    def __init__(self, status, createTimestamp, updateTimestamp, propertyId, propertyTitle, units, pricePerUnit, investorId, total, paymentAddress):
        self.status = status
        self.createTimestamp = createTimestamp
        self.updateTimestamp = updateTimestamp
        self.propertyId = propertyId
        self.propertyTitle = propertyTitle
        self.units = units
        self.pricePerUnit = pricePerUnit
        self.investorId = investorId
        self.total = total
        self.paymentAddress = paymentAddress


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    currencyId = Column(Integer)
    last = Column(String)

    def __init__(self, timestamp, currencyId, last):
        self.timestamp = timestamp
        self.currencyId = currencyId
        self.last = last


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

    def __init__(self, createTimestamp, updateTimestamp, first, last, token, bitcoinAddress, seed, balance, unreadMessages):
        self.createTimestamp = createTimestamp
        self.updateTimestamp = updateTimestamp
        self.first = first
        self.last = last
        self.token = token
        self.bitcoinAddress = bitcoinAddress
        self.seed = seed
        self.balance = balance
        self.unreadMessages = unreadMessages


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

    def __init__(self, status, createTimestamp, updateTimestamp, title, description, address, mls, siteSize, totalUnits, askingPrice, imageHash, imageCount):
        self.status = status
        self.createTimestamp = createTimestamp
        self.updateTimestamp = updateTimestamp
        self.title = title 
        self.description = description 
        self.address = address 
        self.mls = mls 
        self.siteSize = siteSize 
        self.totalUnits = totalUnits 
        self.askingPrice = askingPrice 
        self.imageCount = imageCount 
        self.imageHash = imageHash 


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    status = Column(String)
    createTimestamp = Column(String)
    updateTimestamp = Column(String)
    userId = Column(Integer)
    amount = Column(String)
    bitcoinAddress = Column(String)

    def __init__(self, status, createTimestamp, updateTimestamp, userId, amount, bitcoinAddress):
        self.status = status
        self.createTimestamp = createTimestamp
        self.updateTimestamp = updateTimestamp
        self.userId = userId
        self.amount = amount
        self.bitcoinAddress = bitcoinAddress


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

    def __init__(self, status, type, loginTimestamp, email, password, isEmailVerified, ip):
        self.status = status
        self.type = type
        self.loginTimestamp = loginTimestamp
        self.email = email
        self.password = password
        self.isEmailVerified = isEmailVerified
        self.ip = ip


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
        admin = User("active", 0, timestamp, "0@0.0", password, 1, '')
        newProfile = Profile(timestamp, timestamp, 'admin', 'admin', '', '', '', 1000, 0)
        admin.profiles = [newProfile]
        db.add(admin)

    db.commit()

reset()
