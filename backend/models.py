from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    shared_key_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __init__(self, email, phone_number, shared_key):
        self.email = email
        self.phone_number = phone_number
        self.shared_key = shared_key
    
    @property
    def shared_key(self):
        raise AttributeError('Shared key is not readable')
    
    @shared_key.setter
    def shared_key(self, shared_key):
        self.shared_key_hash = hashlib.sha256(shared_key.encode('utf-8')).hexdigest()
    
    def check_shared_key(self, shared_key):
        return self.shared_key_hash == hashlib.sha256(shared_key.encode('utf-8')).hexdigest()
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone_number': self.phone_number,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class SMSMessage(db.Model):
    __tablename__ = 'sms_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    direction = db.Column(db.String(10), nullable=False)  # 'sent' or 'received'
    phone_number = db.Column(db.String(20), nullable=False)
    message_content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'sent', 'delivered', 'failed'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    gateway_response = db.Column(db.Text)  # Store gateway response for debugging
    
    user = db.relationship('User', backref=db.backref('sms_messages', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'direction': self.direction,
            'phone_number': self.phone_number,
            'message_content': self.message_content,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'gateway_response': self.gateway_response
        }

class APILog(db.Model):
    __tablename__ = 'api_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    endpoint = db.Column(db.String(200), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.String(500))
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)  # in milliseconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('api_logs', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'endpoint': self.endpoint,
            'method': self.method,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'status_code': self.status_code,
            'response_time': self.response_time,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
