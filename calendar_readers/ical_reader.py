import requests
from icalendar import Calendar
from datetime import date, datetime
from dotenv import load_dotenv
import os

class IcalReader:
    """Read events from a Google Calendar iCal feed."""
           
    def load_ical_secret(self):
        """Loads the ical_secret from the .env file and returns it"""
        load_dotenv()
        ICAL_SECRET = os.getenv("ICAL_SECRET")
        if not ICAL_SECRET:
            raise ValueError("Set ICAL_SECRET in your .env file")
        return ICAL_SECRET
    

    def get_events(self, selected_date):
        response = requests.get(
            self.load_ical_secret(),
            timeout=20
        )
        response.raise_for_status()

        calendar = Calendar.from_ical(response.content)
        events = []

        for event in calendar.walk("VEVENT"):
            start = event.decoded("DTSTART")

            event_date = (
                start.date()
                if isinstance(start, datetime)
                else start
            )

            if event_date != selected_date:
                continue

            events.append({
                "title": str(event.get("SUMMARY", "")),
                "location": str(event.get("LOCATION", "")),
                "description": str(
                    event.get("DESCRIPTION", "")
                ),
                "start": start
            })

        return events
