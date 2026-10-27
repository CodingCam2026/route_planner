from datetime import datetime, time, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from datetime import datetime, time
from zoneinfo import ZoneInfo

class GoogleCalendarReader:
    """Class for managing the google calendar such as getting and writing events"""
    def __init__(self):
        self.SCOPES = [
            "https://www.googleapis.com/auth/calendar.events",
            "https://www.googleapis.com/auth/calendar.calendarlist.readonly"
        ]
        self.service = self.authenticate()


    def authenticate(self):
        """Method for authenitcating the google calendar api"""
        creds = None

        if os.path.exists("json/token.json"):
            creds = Credentials.from_authorized_user_file(
                "json/token.json", self.SCOPES
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "json/credentials.json", self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            with open("json/token.json", "w") as file:
                file.write(creds.to_json())

        return build("calendar", "v3", credentials=creds)


    def get_events(self, date, calendar_id):
        timezone = ZoneInfo("Europe/London")

        time_min = datetime.combine(
            date,
            time.min,
            tzinfo=timezone
        ).isoformat()

        time_max = datetime.combine(
            date + timedelta(days=1),
            time.min,
            tzinfo=timezone
        ).isoformat()

        result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=2500,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        return result.get("items", [])

    def get_calendars(self):
        result = self.service.calendarList().list().execute()

        calendars = []
        for calendar in result.get("items", []):
            
            dic = {"calendar_name":calendar["summary"],"calendar_id":calendar["id"],"bg_colour":calendar.get("backgroundColor")}
            calendars.append(dic)
        
       # print(calendars)
        return calendars

    def copy_event(self,event,target_calendar_id):
        """Copies the event into the given calendar id"""
        # Insert into the destination calendar
        copied_event = self.service.events().insert(
            calendarId=target_calendar_id,
            body=event
        ).execute()

