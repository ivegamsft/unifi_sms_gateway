import paramiko
import os
from models import SMSLog, db
from datetime import datetime

class UniFiSMSService:
    def __init__(self):
        self.ip = os.getenv("UNIFI_HOST")
        self.username = os.getenv("UNIFI_USERNAME")
        self.password = os.getenv("UNIFI_PASSWORD")
    
    def build_client(self):
        """Build SSH client connection to UniFi device (from original sms.py)"""
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ip, username=self.username, password=self.password)
        client.exec_command("ifconfig usb0 up")
        return client
    
    def run_command(self, client, command):
        """Run command on UniFi device (from original sms.py)"""
        _stdin, _stdout, _stderr = client.exec_command(f"ssh -y root@$(cat /var/run/topipv6) '/legato/systems/current/bin/cm {command}'")
        return _stdout.read().decode(), _stderr.read().decode()
    
    def get_device_status(self):
        """Get device status (from original sms.py)"""
        client = self.build_client()
        
        out_info, err_info = self.run_command(client, "info all")
        out_sim, err_sim = self.run_command(client, "sim info")
        out_temp, err_temp = self.run_command(client, "temp all")
        
        client.close()
        
        # Return structured data for API
        return {
            'device_info': out_info.strip(),
            'sim_info': out_sim.strip(),
            'temperature_info': out_temp.strip(),
            'status': 'online'
        }

    def get_received_messages(self):
        """Get received SMS messages (from original sms.py)"""
        client = self.build_client()
        
        out_count, err_count = self.run_command(client, "sms count")
        
        count = out_count.replace("\n", "")
        if count == "0":
            result = "NO STORED MESSAGES"
        else:
            out_list, err_list = self.run_command(client, "sms list")
            result = f"{count} STORED MESSAGES:\n{out_list}"
        
        client.close()
        return result
    
    def clear_messages(self):
        """Clear all stored messages (from original sms.py)"""
        client = self.build_client()
        self.run_command(client, "sms clear")
        client.close()
        return "ALL STORED MESSAGES CLEARED"
    
    def send_sms(self, number, message, user_id=None):
        """Send SMS message (from original sms.py with optional logging)"""
        client = self.build_client()
        
        self.run_command(client, f"sms send {number} \"{message}\"")
        
        client.close()
        
        # Log the SMS if user_id is provided (for 3-tier architecture)
        if user_id:
            try:
                sms_log = SMSLog(
                    user_id=user_id,
                    to_number=number,
                    message=message,
                    direction='sent',
                    status='sent'
                )
                db.session.add(sms_log)
                db.session.commit()
                
                return {'success': True, 'message': 'MESSAGE SENT', 'log_id': sms_log.id}
            except Exception as e:
                return {'success': False, 'error': f'Message sent but logging failed: {str(e)}'}
        
        return {'success': True, 'message': 'MESSAGE SENT'}
    
    # Additional methods for the 3-tier architecture compatibility
    def get_received_sms(self):
        """Get received SMS for JSON API response"""
        messages = self.get_received_messages()
        return {'messages': messages}
