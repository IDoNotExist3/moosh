import calendar
# from datetime import datetime, date
import datetime
from googleapiclient.discovery import build
from connector import EventsConnector, CalendarConnector
from urllib.error import HTTPError
import json
from googleapiclient import errors

class MooshEvents:
    """Google Calendar Events"""
    service = None
    events = None
    def __init__(self) -> None:
        self.connector = EventsConnector()
        self.calCon = CalendarConnector()
        try:
            with open('data/events.json') as jf:
                self.jsonEvents = json.load(jf)
            print(self.jsonEvents)

        except:
            print("Error opening events json file")

    def saveJsonEvents(self):
        print("Saving json")
        with open("data/events.json", 'w') as fp:
            json.dump(self.jsonEvents, fp, indent=4, sort_keys=True, default=str)

    def add_event(self, summary: str, start: datetime.date, end: datetime.date, eventID=None) -> None:
        """
        add_event adds or updates event based on eventID

        :summary: string of summary for event
        :start: date of start
        :end: date of end
        :eventID: string of 5 numbers
        """
        serv = build("calendar", "v3", credentials=self.connector.creds)
        print(f"Length of events dict: {len(self.jsonEvents)}")
        
        if eventID not in self.jsonEvents:
            #create event with incremented id from 00000->99999
            print("dating")
            print(start.strftime("%Y-%m-%d"))
            testDate = datetime.datetime.now().isoformat()
            testDate2 = datetime.datetime.now(datetime.UTC).astimezone().date()
            testActualDate = datetime.datetime.today().date()
            # event = {
            #     'summary': summary,
            #     'id' : f"{str(self.jsonEvents['nextID']+1).zfill(5)}",
            #     'start': {
            #         'datetime': "2015-05-28T09:00:00-07:00Z",
            #         'timezone': 'America/New_York'
            #     },
            #     'end': {
            #         'datetime': "2023-05-28T17:00:00-07:00Z",
            #         'timezone': 'America/New_York'
            #     },
            # }
            print(testDate)
            print(testDate2.isoformat())
            print(testActualDate.isoformat())
            # testDate2 = testDate2.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            event = {
                'summary': summary,
                # 'location': '800 Howard St., San Francisco, CA 94103',
                # 'description': 'A chance to hear more about Google\'s developer products.',
                'start': {
                    'date': start.isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                'end': {
                    'date': end.isoformat(),
                    'timeZone': 'America/Los_Angeles',
                },
                # 'recurrence': [
                #     'RRULE:FREQ=DAILY;COUNT=2'
                # ],
                # 'reminders': {
                #     'useDefault': False,
                #     'overrides': [
                #         {'method': 'email', 'minutes': 24 * 60},
                #         {'method': 'popup', 'minutes': 10},
                #     ],
                # },
            }
            
            # print(event["end"])

            try:
                ### Insert new event into google calendar
                print("Ah?")
                print(f"Inserting event {event}")
                e = serv.events().insert(
                    calendarId="ad83c44ba72d92c88afe5c33dfddf8dddb51f8fb56ab040a3f579371acc23c18@group.calendar.google.com",
                    body = event
                ).execute()
                ### Insert new event into local json file
                print("ahhhh")
                # self.jsonEvents[eventID] = event
                # ### Increment local json file nextID
                # self.jsonEvents.update({"nextID": self.jsonEvents["nextID"] + 1}) 
            except errors.HttpError as er:
                print("Error With Event Inserting\n\n")
                print(er)
                print(f"\n")
            except Exception as er:
                print(f"SaveEventError: {er}")
            
        else: ###Event exists
            
            try:
                calEvent = serv.events().get(calendarId="ad83c44ba72d92c88afe5c33dfddf8dddb51f8fb56ab040a3f579371acc23c18@group.calendar.google.com", eventId=eventID).execute()
                if summary != None:
                    calEvent['summary'] = summary
                if start != None:
                    calEvent['start'] = start.strftime('%Y-%m-%d')
                if end != None:
                    calEvent['end'] = end.strftime('%Y-%m-%d')

                e = serv.events().update(
                    calendarId="ad83c44ba72d92c88afe5c33dfddf8dddb51f8fb56ab040a3f579371acc23c18@group.calendar.google.com",
                    eventID=calEvent['id'],
                    body = calEvent
                ).execute()

                event = {
                'summary': summary,
                'id' : eventID,
                'start': start.strftime('%Y-%m-%d'),
                'end': end.strftime('%Y-%m-%d')
                }
                self.jsonEvents.update({eventID: event})
            except Exception as e:
                print(f"Error: {e}")
        
        self.saveJsonEvents()
            
            
        # event = {
        #     'summary' : "Test Upload 1",
        #     'id' : "00000",
        #     'start' : {'date': "2025-05-14"},
        #     'end' : {'date': "2025-05-14"}
        # }
        # event2 = {
        #     'summary' : "Test Upload 2",
        #     'id' : "00001",
        #     'start' : {'date': "2025-05-15"},
        #     'end' : {'date': "2025-05-15"}
        # }
        # eventDict = {"00000": event, "00001" : event2}
        # try:
        #     e = serv.events().insert(
        #         calendarId="ad83c44ba72d92c88afe5c33dfddf8dddb51f8fb56ab040a3f579371acc23c18@group.calendar.google.com",
        #         body = event2
        #     ).execute()
        # except errors.HttpError as e:
        #     print("Event Already Exists")
        # except Exception as e:
        #     print(type(e))
        #     print("An exception occurred:", e)
        #     # print(f"\n{e.args[0]}")
        
        # with open("data/events.json", 'w') as fp:
        #     json.dump(eventDict, fp)
 
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