""" GDrive connector module """
from os import path
from oauth2client.service_account import ServiceAccountCredentials
 
 
class EventsConnector:
    """GDrive connector class"""
 
    _SCOPE = [
        "https://www.googleapis.com/auth/calendar.events"
    ]
 
    def __init__(self) -> None:
        cred_path = path.join("gdrive", "gdrive.json")
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            cred_path, EventsConnector._SCOPE
        )
        print(cred_path)

class CalendarConnector:
    """GDrive connector class"""
 
    _SCOPE = [
        "https://www.googleapis.com/auth/calendar.calendar"
    ]
 
    def __init__(self) -> None:
        cred_path = path.join("gdrive", "gdrive.json")
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            cred_path, EventsConnector._SCOPE
        )
        print(cred_path)