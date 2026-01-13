import requests

EMAIL_SERVICE_URL = "http://localhost:3000/dev/send-email"

def send_email_notification(email_type, to_email, username):
    payload = {
        "type": email_type,
        "to_email": to_email,
        "username": username
    }
    requests.post(EMAIL_SERVICE_URL, json=payload)
