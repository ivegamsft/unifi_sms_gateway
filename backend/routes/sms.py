from flask import Blueprint, request, jsonify
from models import SMSLog, db
from services.unifi_service import UniFiSMSService
import jwt
import os
import logging
import jsonpath_ng.ext as jp
from functools import wraps

sms_bp = Blueprint('sms', __name__)
unifi_service = UniFiSMSService()
logger = logging.getLogger(__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logger.debug(f"Token validation for endpoint: {request.endpoint}")
        token = request.headers.get('Authorization')
        
        if not token:
            logger.warning("No token provided in Authorization header")
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
                logger.debug("Extracted Bearer token")
            
            logger.debug("Attempting to decode JWT token")
            data = jwt.decode(token, os.getenv('SMS_API_KEY'), algorithms=['HS256'])
            current_user_id = data['user_id']
            logger.info(f"Token validated successfully for user ID: {current_user_id}")
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return jsonify({'error': 'Token is invalid'}), 401
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            return jsonify({'error': 'Token validation failed'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('auth')
        
        if not auth or auth != os.getenv('SMS_API_KEY'):
            return "INVALID AUTH", 403
        
        return f(*args, **kwargs)
    
    return decorated

# Frontend endpoints - all use JWT authentication
@sms_bp.route('/status', methods=['GET'])
@token_required
def sms_status(current_user_id):
    logger.info(f"Device status requested by user ID: {current_user_id}")
    try:
        status_data = unifi_service.get_device_status()
        logger.debug(f"Device status retrieved: {status_data}")
        return jsonify(status_data), 200
    except Exception as e:
        logger.error(f"Failed to get device status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@sms_bp.route('/retrieve', methods=['GET'])
@token_required
def sms_retrieve(current_user_id):
    try:
        messages = unifi_service.get_received_messages()
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sms_bp.route('/clear', methods=['DELETE'])
@token_required
def sms_clear(current_user_id):
    try:
        result = unifi_service.clear_messages()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sms_bp.route('/send/<number>', methods=['POST'])
@token_required
def sms_send(current_user_id, number):
    try:
        # Handle JSON path extraction (from your original)
        content_path = request.args.get('path')
        if content_path:
            json_data = request.get_json(force=True)
            query = jp.parse(content_path)
            body = query.find(json_data)[0].value
        else:
            body = request.data.decode('UTF-8')
        
        result = unifi_service.send_sms(number, body)
        return {"message": "MESSAGE SENT", "result": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500

# Additional endpoints for 3-tier architecture (with JWT authentication)
@sms_bp.route('/send', methods=['POST'])
@token_required
def send_sms(current_user_id):
    data = request.get_json()
    
    if not data or not data.get('to_number') or not data.get('message'):
        return jsonify({'error': 'To number and message are required'}), 400
    
    try:
        result = unifi_service.send_sms(
            number=data['to_number'],
            message=data['message'],
            user_id=current_user_id
        )
        
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sms_bp.route('/history', methods=['GET'])
@token_required
def get_sms_history(current_user_id):
    try:
        # Get user's SMS history
        sms_logs = SMSLog.query.filter_by(user_id=current_user_id).order_by(SMSLog.timestamp.desc()).all()
        
        return jsonify([log.to_dict() for log in sms_logs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sms_bp.route('/received', methods=['GET'])
@api_key_required
def get_received_sms():
    try:
        result = unifi_service.get_received_sms()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sms_bp.route('/logs', methods=['GET'])
@api_key_required
def get_all_sms_logs():
    try:
        # Get all SMS logs (admin function)
        sms_logs = SMSLog.query.order_by(SMSLog.timestamp.desc()).all()
        
        return jsonify([log.to_dict() for log in sms_logs]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
