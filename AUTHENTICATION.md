# Authentication Configuration

## Overview
This application uses separate authentication keys for different purposes to enhance security.

## Authentication Keys

### 1. Flask Secret Key (`SECRET_KEY`)
- **Purpose**: Flask session management, CSRF protection, and general Flask security
- **Usage**: Used by Flask framework for secure session handling
- **Location**: Flask app configuration
- **Recommendation**: Use a strong, random 32+ character string

### 2. JWT Secret Key (`JWT_SECRET_KEY`)
- **Purpose**: User authentication tokens (login sessions)
- **Usage**: Signs and verifies JWT tokens for user login/logout
- **Location**: User authentication endpoints (`/api/auth/login`)
- **Recommendation**: Use a different key from SECRET_KEY, 32+ characters

### 3. SMS API Key (`SMS_API_KEY`)
- **Purpose**: API authentication for SMS device access
- **Usage**: Authenticates with UniFi devices or SMS services
- **Location**: UniFi service for device communication
- **Recommendation**: Use device-specific API key or shared secret

## Configuration Example

```properties
# Flask Configuration
SECRET_KEY=flask-app-secret-key-32-chars-minimum
JWT_SECRET_KEY=jwt-token-secret-key-different-from-flask
FLASK_ENV=development
FLASK_DEBUG=1

# SMS API Authentication
SMS_API_KEY=sms-device-api-authentication-key

# UniFi Controller Configuration
UNIFI_HOST=192.168.1.1
UNIFI_USERNAME=admin
UNIFI_PASSWORD=your-unifi-password
UNIFI_PORT=22
UNIFI_SITE=default
```

## Security Best Practices

1. **Use Different Keys**: Never use the same key for multiple purposes
2. **Key Length**: Minimum 32 characters for all keys
3. **Random Generation**: Use cryptographically secure random generators
4. **Environment Variables**: Store in .env files, never commit to git
5. **Production**: Use proper secret management systems in production

## Key Generation Commands

```bash
# Generate random keys (examples)
python -c "import secrets; print(secrets.token_urlsafe(32))"
openssl rand -base64 32
```

## Usage in Code

- **Flask Secret**: `app.config['SECRET_KEY']`
- **JWT Secret**: `app.config['JWT_SECRET_KEY']` for jwt.encode/decode
- **SMS API**: `self.sms_api_key` in UniFiSMSService for device authentication
