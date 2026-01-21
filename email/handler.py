import json
import smtplib
from email.message import EmailMessage

def send_email(event, context):
    body = json.loads(event['body'])

    email_type = body.get('type')
    to_email = body.get('to_email')
    username = body.get('username')

    msg = EmailMessage()

    if email_type == "SIGNUP_WELCOME":
        msg['Subject'] = "Welcome to Mini HMS"
        msg.set_content(f"Hi {username},\n\nWelcome to our Hospital Management System!")

    elif email_type == "BOOKING_CONFIRMATION":
        msg['Subject'] = "Appointment Confirmed"
        msg.set_content(f"Hi {username},\n\nYour appointment has been confirmed.")

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid email type"})
        }

    msg['From'] = "sadathkhan717@gmail.com"
    msg['To'] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("sadathkhan717@gmail.com", "gbjd xcjf fiwn dvba")
        server.send_message(msg)
        server.quit()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
