# utils.py

import hmac
import hashlib
import base64
from django.conf import settings

def verify_signature(data):
    # Extract relevant data from the request
    signature = data.get('razorpay_signature', '')
    order_id = data.get('razorpay_order_id', '')
  
    # Construct the payload to be signed
    payload = order_id.encode()

    # Generate the expected signature using your Razorpay key secret
    expected_signature = hmac.new(
        settings.RAZOR_KEY_SECRET.encode(),
        payload,
        hashlib.sha256
    ).digest()

    # Encode the expected signature in base64
    expected_signature = base64.b64encode(expected_signature).decode()

    # Compare the expected signature with the received signature
    return signature == expected_signature
