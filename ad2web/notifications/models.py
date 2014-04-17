# -*- coding: utf-8 -*-

from OpenSSL import crypto, SSL
from sqlalchemy import Column, orm
from sqlalchemy.orm.collections import attribute_mapped_collection

from ..extensions import db

class CustomNotification(db.Model):
    __tablename__ = 'custom_notifications'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    description = Column(db.String(255), nullable=False)
    type = Column(db.Integer, nullable=False)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))

    settings = db.relationship("CustomNotificationSetting", backref="CustomNotification", cascade="all, delete-orphan")

class CustomNotificationSetting(db.Model):
    __tablename__ = 'custom_notification_settings'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(db.String(32), nullable=False)
    custom_notification_id = Column(db.Integer, db.ForeignKey("custom_notifications.id"))
    message_type = Column(db.Integer, nullable=False)
    message_address_or_serial = Column(db.Integer)
    message_channel = Column(db.Integer)
    message_data = Column(db.Integer)

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    description = Column(db.String(255), nullable=False)
    type = Column(db.Integer, nullable=False)
    user_id = Column(db.Integer, db.ForeignKey('users.id'))

    settings = db.relationship("NotificationSetting", backref="notification", collection_class=attribute_mapped_collection('name'), cascade="all, delete-orphan")

class NotificationSetting(db.Model):
    __tablename__ = 'notification_settings'

    id = Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(db.String(32), nullable=False)

    notification_id = Column(db.Integer, db.ForeignKey("notifications.id"))

    int_value = Column(db.Integer)
    string_value = Column(db.String(255))

    @property
    def value(self):
        for k in ('int_value', 'string_value'):
            v = getattr(self, k)
            if v is not None:
                return v
        else:
            return None

    @value.setter
    def value(self, value):
        if isinstance(value, int):
            self.int_value = value
            self.string_value = None
        else:
            self.string_value = str(value)
            self.int_value = None
