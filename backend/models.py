from flask import current_app
from backend import db
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import MetaData, func, create_engine
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI')) # connect to server
engine.execute(f"CREATE SCHEMA IF NOT EXISTS {current_app.config.get('POSTGRES_SCHEMA')};") #create db

class UserAccount(UserMixin, db.Model):
    """User Account table """
    __bind_key__ = 'postgresql'
    __tablename__ = 'user_account'
    __table_args__ = {"schema": current_app.config['POSTGRES_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(512), unique=True, index=True)
    first_name = db.Column(db.String(512))
    last_name = db.Column(db.String(512))
    last_active = db.Column(db.DateTime)
    password_changes = db.relationship('PasswordChange', backref='user', lazy='dynamic')
    authentications = db.relationship('AccountAuthentication', backref='user', lazy='dynamic')
    social_profile = db.relationship('SocialProfile', backref='user', uselist=False)

    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User: {self.first_name} {self.last_name} ({self.id})>"

    def update_last_active(self):
        """Updates a user's last_login field on every login"""
        self.last_active = datetime.utcnow()
        db.session.commit()

    def set_password(self, password):
        """Generates password hash from provided string and sets as user's password"""
        # TODO -- fix ip and session_id
        PasswordChange.create(self.id, password, 'ip', 'session_id')

    @property
    def password_hash(self):
        return PasswordChange.get_password(self.id).new_password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SocialProfile(db.Model):
    """Social Profile table """
    __bind_key__ = 'postgresql'
    __tablename__ = 'social_profile'
    __table_args__ = {"schema": current_app.config['POSTGRES_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{current_app.config["POSTGRES_SCHEMA"]}.user_account.id'))
    email = db.Column(db.String(512), unique=True, index=True)
    phone = db.Column(db.String(512), unique=True, index=True)
    snap = db.Column(db.String(512), unique=True, index=True)
    insta = db.Column(db.String(512), unique=True, index=True)
    spotify = db.Column(db.String(512), unique=True, index=True)
    linkedin = db.Column(db.String(512), unique=True, index=True)
    facebook = db.Column(db.String(512), unique=True, index=True)

    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AccountAuthentication(db.Model):
    """Account Authentications table """
    __bind_key__ = 'postgresql'
    __tablename__ = 'account_authentication'
    __table_args__ = {"schema": current_app.config['POSTGRES_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(512))
    password_hash = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey(f'{current_app.config["POSTGRES_SCHEMA"]}.user_account.id'))
    ip_address = db.Column(db.String(512))
    session_id = db.Column(db.String(512))

    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PasswordChange(db.Model):
    """Password Change table """
    __bind_key__ = 'postgresql'
    __tablename__ = 'password_change'
    __table_args__ = {"schema": current_app.config['POSTGRES_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{current_app.config["POSTGRES_SCHEMA"]}.user_account.id'))
    old_password_hash = db.Column(db.String(512))
    new_password_hash = db.Column(db.String(512))
    ip_address = db.Column(db.String(512))
    session_id = db.Column(db.String(512))

    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, new, ip, session_id):
        old_hash = cls.get_password(user_id)
        new_password_change = cls(user_id=user_id,
                                  old_password_hash=old_hash.old_password_hash if old_hash is not None else None,
                                  new_password_hash=generate_password_hash(new),
                                  ip_address=ip,
                                  session_id=session_id)
        db.session.add(new_password_change)
        db.session.commit()

    @classmethod
    def get_password(cls, user_id):
        return db.session.query(cls).filter_by(user_id=user_id).order_by(cls.created_at.desc()).first()
