from flask import current_app
from backend import db, auth
from flask_login import UserMixin
from sqlalchemy import func, create_engine
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI')) # connect to server
engine.execute(f"CREATE SCHEMA IF NOT EXISTS {current_app.config.get('POSTGRES_SCHEMA')};") #create db


@auth.request_loader
def load_user(request):
    auth_headers = request.headers.get('Authorization', '').split()
    if len(auth_headers) != 2:
        return None
    try:
        token = auth_headers[1]
        data = jwt.decode(token, current_app.config['SECRET_KEY'])
        user = UserAccount.get(uid=data['sub'])
        if user:
            return user
    except jwt.ExpiredSignatureError:
        return None
    except (jwt.InvalidTokenError, Exception) as e:
        return None
    return None


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
    lookups = db.relationship('ProfileLookup', backref='user', lazy='dynamic')

    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User: {self.first_name} {self.last_name} ({self.id})>"

    def __init__(self, email, first, last):
        self.email = email
        self.first_name = first.lower().capitalize()
        self.last_name = last.lower().capitalize()

    @classmethod
    def get(cls, email=None, uid=None):
        if email is None and uid is None:
            return None
        else:
            if email is not None:
                return db.session.query(cls).filter_by(email=email).first()
            elif uid is not None:
                return db.session.query(cls).filter_by(id=uid).first()

    @classmethod
    def create(cls, email, first, last, password, ip, session=None):
        new_user = cls(email, first, last)
        db.session.add(new_user)
        db.session.commit()
        added_user = cls.get(email)
        added_user.set_password(password, ip, session)
        added_user.update_last_active()
        SocialProfile.create(added_user.id)
        return added_user

    def update_last_active(self):
        """Updates a user's last_login field on every login"""
        self.last_active = datetime.utcnow()
        db.session.commit()

    def set_password(self, password, ip, session):
        """Generates password hash from provided string and sets as user's password"""
        PasswordChange.create(self.id, password, ip, session)

    @property
    def password_hash(self):
        return PasswordChange.get_password(self.id).new_password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def check_email_availability(cls, email):
        return db.session.query(cls).filter_by(email=email).first() is None

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def get_lookups(self):
        # TODO -- sort, paginate, remove dublicates
        return []


class SocialProfile(db.Model):
    """Social Profile table """
    __bind_key__ = 'postgresql'
    __tablename__ = 'social_profile'
    __table_args__ = {"schema": current_app.config['POSTGRES_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{current_app.config["POSTGRES_SCHEMA"]}.user_account.id'))
    bio = db.Column(db.String(512))
    phone = db.Column(db.String(512), unique=True, index=True)
    snap = db.Column(db.String(512), unique=True, index=True)
    insta = db.Column(db.String(512), unique=True, index=True)
    spotify = db.Column(db.String(512), unique=True, index=True)
    linkedin = db.Column(db.String(512), unique=True, index=True)
    queries = db.relationship('ProfileLookup', backref='profile', lazy='dynamic')

    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Social Profile: {self.id} of {self.user.name}>"

    @classmethod
    def create(cls, u_id):
        profile = cls(user_id=u_id)
        db.session.add(profile)
        db.session.commit()
        return profile

    def update(self, data):
        self.bio = data['bio']
        self.phone = data['phone']
        self.snap = data['snap']
        self.insta = data['insta']
        self.spotify = data['spotify']
        self.linkedin = data['linkedin']
        db.session.commit()

    @classmethod
    def get(cls, p_id):
        return db.session.query(cls).filter_by(id=p_id).first()

    def jsonify(self):
        return {"name": self.user.name,
                "bio": self.bio,
                "phone": self.phone,
                "snap": self.snap,
                "insta": self.insta,
                "spotify": self.spotify,
                "linkedin": self.linkedin}

    def get_queries(self):
        # TODO -- sort, paginate, remove dublicates
        return []


class AccountAuthentication(db.Model):
    """Account Authentications table """
    __bind_key__ = 'postgresql'
    __tablename__ = 'account_authentication'
    __table_args__ = {"schema": current_app.config['POSTGRES_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(512))
    password_hash = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey(f'{current_app.config["POSTGRES_SCHEMA"]}.user_account.id'))
    ip_address = db.Column(db.String(512))
    session_id = db.Column(db.String(512))

    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Account Auth: {self.id}>"

    def __init__(self, email, password, ip, u_id):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.ip_address = ip
        self.user_id = u_id

    @classmethod
    def create(cls, email, password, ip, u_id=None):
        auth = cls(email, password, ip, u_id)
        db.session.add(auth)
        db.session.commit()
        return auth


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


class ProfileLookup(db.Model):
    """Profile Lookup table """
    __bind_key__ = 'postgresql'
    __tablename__ = 'profile_lookup'
    __table_args__ = {"schema": current_app.config['POSTGRES_SCHEMA']}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(f'{current_app.config["POSTGRES_SCHEMA"]}.user_account.id'),
                        index=True)
    social_profile_id = db.Column(db.Integer, db.ForeignKey(f'{current_app.config["POSTGRES_SCHEMA"]}.social_profile.id'),
                                  index=True)

    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.current_timestamp())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, user_id, profile_id):
        lookup = cls(user_id=user_id, social_profile_id=profile_id)
        db.session.add(lookup)
        db.session.commit()
        return lookup
