# Aliyun-SMS-Integration

A Flask web application that integrates with the Aliyun SMS Service, allowing you to send SMS messages through a user-friendly web interface or a REST API.

## Features

- Web UI for sending SMS messages
- REST API for programmatic access
- Support for multiple phone numbers
- Template parameter customization
- Error handling and validation

## Prerequisites

- Python 3.7 or higher
- Aliyun account with SMS service enabled
- Aliyun AccessKey ID and AccessKey Secret
- Valid SMS signature and template approved by Aliyun

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/tjcchen/Aliyun-SMS-Integration.git
cd Aliyun-SMS-Integration
```

### 2. Python environment setup

```bash
# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt
```

### 3. Configure environment variables

Copy the example environment file and update with your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file with your Aliyun credentials:

```
# Aliyun SMS API Credentials
ALIBABA_CLOUD_ACCESS_KEY_ID=your_access_key_id
ALIBABA_CLOUD_ACCESS_KEY_SECRET=your_access_key_secret
```

## Running the Application

```bash
python3 app.py

# or

python3 test_sms.py --phone "13800138000" --sign "YourCompany" --template "SMS_123456789" --params '{"code":"123456"}'
```

The application will be available at http://localhost:5000

## How to Use

### Web Interface

1. Open your browser and navigate to http://localhost:5000
2. Fill in the form with:
   - Phone number(s) - separate multiple numbers with commas
   - Sign name - your Aliyun registered SMS signature
   - Template code - your Aliyun SMS template code
   - Template parameters - JSON format of parameters for your template
3. Click "Send SMS" to send the message

### REST API

You can also send SMS messages programmatically using the API endpoint:

```
POST /api/send-sms
Content-Type: application/json

{
  "phone_numbers": "13800138000",
  "sign_name": "YourSignName",
  "template_code": "SMS_123456789",
  "template_param": {
    "code": "123456"
  }
}
```

Response:

```json
{
  "success": true,
  "message": "SMS sent successfully",
  "request_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
  "code": "OK",
  "biz_id": "XXXXXXXXXXXXXXXX"
}
```

## Aliyun SMS Configuration

To use this application, you need to:

1. Create an Aliyun account and enable the SMS service
2. Create an AccessKey ID and Secret from the Aliyun console
3. Register an SMS signature through the Aliyun SMS console
4. Create an SMS template through the Aliyun SMS console

For more information, refer to the [Aliyun SMS documentation](https://www.alibabacloud.com/help/product/44282.htm).

## Error Handling

The application includes error handling for common issues:

- Missing required parameters
- Invalid template parameter format
- Aliyun API errors

Check the web interface for error messages or the API response for error details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

