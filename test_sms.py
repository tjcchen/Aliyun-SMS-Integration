#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for Aliyun SMS integration.
This script allows you to send an SMS message directly from the command line
without using the web interface.
"""

import argparse
import json
import os
from dotenv import load_dotenv

# Import AliyunSMS class from app.py
from app import AliyunSMS

def main():
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Send SMS using Aliyun SMS service')
    parser.add_argument('--phone', '-p', required=True, help='Phone number(s) to send SMS to (comma separated for multiple)')
    parser.add_argument('--sign', '-s', required=True, help='SMS signature name registered with Aliyun')
    parser.add_argument('--template', '-t', required=True, help='SMS template code registered with Aliyun')
    parser.add_argument('--params', '-m', default='{}', help='Template parameters as JSON string, e.g. \'{"code":"123456"}\'')
    
    args = parser.parse_args()
    
    try:
        # Parse template parameters
        template_param = json.loads(args.params)
        
        print(f"Sending SMS to: {args.phone}")
        print(f"Using sign name: {args.sign}")
        print(f"Using template code: {args.template}")
        print(f"With parameters: {template_param}")
        
        # Send SMS
        response = AliyunSMS.send_sms(
            phone_numbers=args.phone,
            sign_name=args.sign,
            template_code=args.template,
            template_param=template_param
        )
        
        # Print response
        print("\nResponse:")
        for key, value in response.items():
            print(f"{key}: {value}")
            
        if response.get('success'):
            print("\nSMS sent successfully!")
        else:
            print("\nFailed to send SMS.")
            
    except json.JSONDecodeError:
        print("Error: Invalid JSON format for template parameters")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
