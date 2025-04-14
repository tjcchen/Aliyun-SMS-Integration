import os
import sys
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv

from typing import List, Dict, Any

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

class AliyunSMS:
    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        Initialize Aliyun SMS client with API keys
        """
        # Security Note: It's better to use environment variables for sensitive data
        # See: https://help.aliyun.com/document_detail/378659.html for more secure auth methods
        access_key_id = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID')
        access_key_secret = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
        
        if not access_key_id or not access_key_secret:
            raise ValueError('Aliyun API credentials not set in environment variables')
        
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        # Endpoint for the Aliyun SMS API
        config.endpoint = 'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def send_sms(phone_numbers: str, sign_name: str, template_code: str, template_param: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Send SMS using Aliyun SMS service
        
        Args:
            phone_numbers: Phone number(s) to send SMS to
            sign_name: SMS signature name registered with Aliyun
            template_code: SMS template code registered with Aliyun
            template_param: Template parameters as a dictionary
            
        Returns:
            Response from Aliyun SMS API
        """
        client = AliyunSMS.create_client()
        
        # Create SMS request
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone_numbers,
            sign_name=sign_name,
            template_code=template_code,
            template_param=str(template_param) if template_param else None
        )
        
        response = {}
        try:
            # Send SMS
            result = client.send_sms_with_options(send_sms_request, util_models.RuntimeOptions())
            # Convert response to dictionary
            response = {
                'success': True,
                'message': 'SMS sent successfully',
                'request_id': result.body.request_id,
                'code': result.body.code,
                'message': result.body.message,
                'biz_id': result.body.biz_id
            }
        except Exception as error:
            # Handle errors
            response = {
                'success': False,
                'message': str(error.message) if hasattr(error, 'message') else str(error),
                'recommend': error.data.get("Recommend") if hasattr(error, 'data') else None
            }
        
        return response

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/send-sms', methods=['POST'])
def send_sms():
    # Get form data
    phone_numbers = request.form.get('phone_numbers')
    sign_name = request.form.get('sign_name')
    template_code = request.form.get('template_code')
    template_param = request.form.get('template_param', '{}')
    
    # Validate form data
    if not all([phone_numbers, sign_name, template_code]):
        flash('Please fill in all required fields', 'error')
        return redirect(url_for('index'))
    
    try:
        # Parse template parameters
        import json
        template_param_dict = json.loads(template_param)
        
        # Send SMS
        response = AliyunSMS.send_sms(
            phone_numbers=phone_numbers,
            sign_name=sign_name,
            template_code=template_code,
            template_param=template_param_dict
        )
        
        if response.get('success'):
            flash('SMS sent successfully. BizId: ' + response.get('biz_id', 'N/A'), 'success')
        else:
            flash('Failed to send SMS: ' + response.get('message', 'Unknown error'), 'error')
    
    except json.JSONDecodeError:
        flash('Invalid template parameters format. Must be a valid JSON object.', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/send-sms', methods=['POST'])
def api_send_sms():
    """
    API endpoint for sending SMS programmatically
    """
    from flask import jsonify
    
    try:
        data = request.get_json()
        
        # Validate request data
        if not all([data.get('phone_numbers'), data.get('sign_name'), data.get('template_code')]):
            return jsonify({
                'success': False,
                'message': 'Missing required parameters: phone_numbers, sign_name, template_code'
            }), 400
        
        # Send SMS
        response = AliyunSMS.send_sms(
            phone_numbers=data.get('phone_numbers'),
            sign_name=data.get('sign_name'),
            template_code=data.get('template_code'),
            template_param=data.get('template_param')
        )
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)
