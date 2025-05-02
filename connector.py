""" GDrive connector module """
from os import path
from oauth2client.service_account import ServiceAccountCredentials
 
 
class Connector:
    """GDrive connector class"""
 
    _SCOPE = [
        "https://www.googleapis.com/auth/calendar.events"
    ]
 
    def __init__(self) -> None:
        cred_path = path.join("gdrive", "gdrive.json")
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            cred_path, Connector._SCOPE
        )
        print(cred_path)