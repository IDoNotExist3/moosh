import calendar
from datetime import datetime, date
from googleapiclient.discovery import build
from connector import EventsConnector, CalendarConnector
from urllib.error import HTTPError
import json

class MooshEvents:
    """Google Calendar Events"""
    service = None
    events = None
    def __init__(self) -> None:
        self.connector = EventsConnector()
        self.calCon = CalendarConnector()

    def add_event(self) -> None:
        serv = build("calendar", "v3", credentials=self.connector.creds)
        event = {
            'summary' : "Test Upload 2",
            'id' : "00000",
            'start' : {'date': "2025-05-14"},
            'end' : {'date': "2025-05-14"}
        }
        event2 = {
            'summary' : "Test Upload 2",
            'id' : "00001",
            'start' : {'date': "2025-05-15"},
            'end' : {'date': "2025-05-15"}
        }
        eventDict = {"00000": event, "00001" : event2}
        try:
            e = serv.events().insert(
                calendarId="ad83c44ba72d92c88afe5c33dfddf8dddb51f8fb56ab040a3f579371acc23c18@group.calendar.google.com",
                body = event2
            ).execute()
        except HTTPError:
            print("Event already exists")
        except:
            print("Unkown error in event creation")
        
        with open("data/events.json", 'w') as fp:
            json.dump(eventDict, fp)
 
    def get_upcoming_as_dict(self) -> dict:
        """Return upcoming"""
        output = {"events": []}
        self.calService = build("calendar", "v3", credentials=self.calCon.creds)
        self.service = build("calendar", "v3", credentials=self.connector.creds)
 
        # Call the Calendar API
        events_result = (
            self.service.events()
            .list(
                calendarId="ad83c44ba72d92c88afe5c33dfddf8dddb51f8fb56ab040a3f579371acc23c18@group.calendar.google.com",
                # maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        self.events = events_result.get("items", [])
        # print("\nAHHHHHH\n")
                # print(event)
        if not self.events:
            return output

        for event in self.events:
            # print("eventing")
            # # print(event)
            # print(type(event))
            # print(event.get("summary"))
            try:
                # if "description" not in event:
                #     continue
 
                # desc_lines = event["description"].split("\n")
                # if len(desc_lines) < 5:
                #     continue
                
 
                # start_list_1 = event["start"]["dateTime"].split("-")
                # start_list_2 = start_list_1[2].split("T")
                # start_list_3 = start_list_2[1].split(":")
                name = event.get("summary")
                # print("After get")
                gig = {
                    "name": f"{name}",
                }

                # gig = {
                #     "short_date": f"{calendar.month_abbr[int(start_list_1[1])]} {start_list_2[0]}",
                #     "time": f"{start_list_3[0]}:{start_list_3[1]}",
                #     "band": desc_lines[0],
                #     "venue": desc_lines[1],
                #     "genre": desc_lines[2],
                #     "ticket_emoji": desc_lines[3],
                #     "ticket_link": desc_lines[4],
                # }
                # print("End of try")
 
            except Exception:
                continue
 
            output["events"].append(gig)
 
        return output