from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

def create_calendar_event(user, title, start, end):
    # 🔒 SAFETY CHECK
    if not user.google_token:
        #User has not connected Google Calendar
       return
        
    creds = Credentials(**user.google_token)
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': title,
        'start': {'dateTime': start, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end, 'timeZone': 'Asia/Kolkata'},
    }

    service.events().insert(calendarId='primary', body=event).execute()
