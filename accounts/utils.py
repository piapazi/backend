import requests
from django.conf import settings

def verify_recaptcha(token):
    """Verify reCAPTCHA v3 token with Google."""
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": settings.RECAPTCHA_PRIVATE_KEY,
        "response": token,
    }
    response = requests.post(url, data=data)
    result = response.json()
    # result['success'] should be True and score > 0.5 (adjust as needed)
    return result.get("success", False) and result.get("score", 0) > 0.5