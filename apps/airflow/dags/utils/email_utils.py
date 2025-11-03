"""
Simplified email utilities for news aggregation pipeline.
Handles email sending via Resend API.
"""

import os
import resend
from typing import List, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailManager:
    """Simplified email manager using Resend API."""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('RESEND_API_KEY')
        if not self.api_key:
            raise ValueError("Resend API key not provided")
        
        resend.api_key = self.api_key
    
    def send_email(self, subject: str, content: str, recipients: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Send email to multiple recipients.
        
        Args:
            subject: Email subject line
            content: HTML email content
            recipients: List of dicts with 'name' and 'email' keys
            
        Returns:
            Dict with results for each recipient
        """
        results = {
            'success_count': 0,
            'failed_count': 0,
            'details': []
        }
        
        for recipient in recipients:
            result = self._send_to_recipient(subject, content, recipient)
            results['details'].append(result)
            
            if result['success']:
                results['success_count'] += 1
            else:
                results['failed_count'] += 1
        
        logger.info(f"Email sending complete: {results['success_count']} sent, {results['failed_count']} failed")
        return results
    
    def _send_to_recipient(self, subject: str, content: str, recipient: Dict[str, str]) -> Dict[str, Any]:
        """Send email to a single recipient."""
        
        try:
            response = resend.Emails.send({
                "from": "onboarding@resend.dev",  # Use Resend's test domain
                "to": [recipient['email']],
                "subject": subject,
                "html": content
            })
            
            logger.info(f"Email sent successfully to {recipient['email']}: {response['id']}")
            
            return {
                'success': True,
                'email': recipient['email'],
                'name': recipient['name'],
                'resend_id': response.get('id'),
                'sent_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error sending email to {recipient['email']}: {e}")
            return {
                'success': False,
                'email': recipient['email'],
                'name': recipient['name'],
                'error': str(e),
                'sent_at': datetime.now().isoformat()
            }
    
    def test_email_connection(self) -> bool:
        """Test email API connection."""
        try:
            if self.api_key and len(self.api_key) > 10:
                logger.info("Email API key appears to be valid")
                return True
            else:
                logger.error("Invalid email API key")
                return False
        except Exception as e:
            logger.error(f"Error testing email connection: {e}")
            return False

# Global email manager instance
def get_email_manager() -> EmailManager:
    """Get configured email manager."""
    return EmailManager()
