-- PostgreSQL setup script for UniFi SMS Gateway

-- Create database
CREATE DATABASE unifi_sms_gateway;

-- Create user
CREATE USER unifi_user WITH PASSWORD 'unifi_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE unifi_sms_gateway TO unifi_user;

-- Connect to the database and grant schema privileges
\c unifi_sms_gateway;
GRANT ALL ON SCHEMA public TO unifi_user;
