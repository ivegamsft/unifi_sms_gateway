from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from models import db
from routes.auth import auth_bp
from routes.sms import sms_bp
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('backend.log')  # File output
    ]
)

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///unifi_sms.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('SMS_API_KEY', 'dev-jwt-secret-key-change-in-production')

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(sms_bp, url_prefix='/api/sms')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'service': 'UniFi SMS Gateway API'}, 200

@app.route('/', methods=['GET'])
def root():
    return {
        'service': 'UniFi SMS Gateway API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'auth': '/api/auth',
            'sms': '/api/sms'
        }
    }, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=8585, debug=True)
