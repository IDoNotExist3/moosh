import calendar
from datetime import datetime
from googleapiclient.discovery import build
from connector import Connector

class MooshEvents:
    """Google Calendar Events"""
    def __init__(self) -> None:
        self.connector = Connector()
 
    def get_upcoming_as_dict(self) -> dict:
        """Return upcoming"""
        output = {"gigs": []}
 
        service = build("calendar", "v3", credentials=self.connector.creds)
 
        # Call the Calendar API
        events_result = (
            service.events()
            .list(
                calendarId="ad83c44ba72d92c88afe5c33dfddf8dddb51f8fb56ab040a3f579371acc23c18@group.calendar.google.com",
                # maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        # print("\nAHHHHHH\n")
                # print(event)
        if not events:
            return output

        for event in events:
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
 
            output["gigs"].append(gig)
 
        return output