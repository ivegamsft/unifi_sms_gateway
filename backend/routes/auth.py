from flask import Blueprint, request, jsonify
from models import User, db
import jwt
import os
import logging
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    logger.info("Login attempt started")
    
    try:
        data = request.get_json()
        logger.debug(f"Login request data: {data}")
        
        if not data or not data.get('email') or not data.get('phone_number') or not data.get('shared_key'):
            logger.warning("Missing required fields in login request")
            return jsonify({'error': 'Email, phone number, and shared key are required'}), 400
        
        # For now, validate against hardcoded shared key from environment
        expected_shared_key = os.getenv('DEFAULT_SHARED_KEY', 'your-default-shared-key-for-user-registration')
        logger.debug(f"Expected shared key: {expected_shared_key}")
        logger.debug(f"Provided shared key: {data['shared_key']}")
        
        if data['shared_key'] != expected_shared_key:
            logger.warning(f"Invalid shared key provided: {data['shared_key']}")
            return jsonify({'error': 'Invalid shared key'}), 401
        
        # Check if user exists or create new user
        logger.info(f"Looking up user: {data['email']}, {data['phone_number']}")
        user = User.query.filter_by(email=data['email'], phone_number=data['phone_number']).first()
        
        if not user:
            logger.info("User not found, creating new user")
            # Auto-register user with hardcoded shared key
            try:
                user = User(
                    email=data['email'],
                    phone_number=data['phone_number'],
                    shared_key=data['shared_key']
                )
                db.session.add(user)
                db.session.commit()
                logger.info(f"New user created with ID: {user.id}")
            except Exception as e:
                logger.error(f"Failed to create user: {str(e)}")
                db.session.rollback()
                return jsonify({'error': 'Failed to create user account'}), 500
        else:
            logger.info(f"Existing user found with ID: {user.id}")
        
        if not user.is_active:
            logger.warning(f"Account disabled for user ID: {user.id}")
            return jsonify({'error': 'Account is disabled'}), 401
        
        # Generate JWT token
        logger.info(f"Generating JWT token for user ID: {user.id}")
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'phone_number': user.phone_number,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, os.getenv('SMS_API_KEY'), algorithm='HS256')
        
        logger.info(f"Login successful for user ID: {user.id}")
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        logger.error(f"Login failed with error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('phone_number') or not data.get('shared_key'):
        return jsonify({'error': 'Email, phone number, and shared key are required'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'User with this email already exists'}), 409
    
    try:
        user = User(
            email=data['email'],
            phone_number=data['phone_number'],
            shared_key=data['shared_key']
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create user'}), 500

@auth_bp.route('/users', methods=['GET'])
def get_users():
    # This would typically require admin authentication
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200
