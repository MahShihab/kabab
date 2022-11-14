from tokenize import Special
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func 




class OrderLine(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    Order_id = db.Column(db.Integer , db.ForeignKey('order.id'))
    Item_id = db.Column(db.Integer , db.ForeignKey('item.id'))
    ItemNum = db.Column(db.String(150))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone = True) , default = func.now())
    OrderPrice = db.Column(db.Integer)
    # Lines = db.relationship('OrderLine')



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ItemName = db.Column(db.String(150))
    ItemPrice = db.Column(db.Float)
    ItemType = db.Column(db.String(150))
    ItemDescription = db.Column(db.String(1000))
    Special = db.Column(db.String(150))
    pic = db.Column(db.String(50))
    rival = db.Column(db.Integer)
    # Lines = db.relationship('OrderLine')


class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    Password = db.Column(db.String(150))
    # Lines = db.relationship('OrderLine')


class Rating(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    rate = db.Column(db.Integer)    




