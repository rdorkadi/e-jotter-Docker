# for storing Database models (like database schema)

from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import os
import base64
import onetimepass as otp

# class == table
# attributes == column

# For our Note Taking app
# 2 models : 1> Notes 2> Users data

# Notes model
class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())   # store current date and time, for every note creation
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))    # foreign key ; referencing to "User" table's "id" | 1 user having many notes

# User data
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)   # no 2 users should have same email ID
    firstName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    notes = db.relationship('Note')         # didnt understand
    
    totp_secret = db.Column(db.String(16))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.totp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

    def get_totp_uri(self):
        return 'otpauth://totp/fnote-mfa:{0}?secret={1}&issuer=fnote-mfa'.format(self.email, self.totp_secret)
    
    def verify_totp(self, token):
        return otp.valid_totp(token, self.totp_secret)
   