from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    shared_key = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship to SMS logs
    sms_logs = db.relationship('SMSLog', backref='user', lazy=True)
    
    def __init__(self, email, phone_number, shared_key):
        self.email = email
        self.phone_number = phone_number
        self.shared_key = bcrypt.hashpw(shared_key.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_shared_key(self, shared_key):
        return bcrypt.checkpw(shared_key.encode('utf-8'), self.shared_key.encode('utf-8'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

class SMSLog(db.Model):
    __tablename__ = 'sms_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    to_number = db.Column(db.String(20), nullable=False)
    from_number = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=False)
    direction = db.Column(db.String(10), nullable=False)  # 'sent' or 'received'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'sent', 'failed', 'delivered'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    device_response = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'to_number': self.to_number,
            'from_number': self.from_number,
            'message': self.message,
            'direction': self.direction,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'device_response': self.device_response
        }
