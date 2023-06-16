from pprint import pprint
from Google import create_service


CLIENT = "client_secret_754421839897-mm7ictagubbvt5uengtjfqsm12b6dim8.apps.googleusercontent.com.json"
API = "calendar"
API_V = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


service = create_service(CLIENT, API, API_V, SCOPES)

event = {
    'summary': 'Python API test',
    'location': 'bla',
    'description': '',
    'start': {
    'dateTime': '2023-06-22T9:20:00',
    'timeZone': 'Europe/Prague',
    },
    'end': {
    'dateTime': '2023-06-22T10:00:00',
    'timeZone': 'Europe/Prague',
    },
    'recurrence': [
    ],
    'attendees': [
    ],
    'reminders': {
    'useDefault': True,
    'overrides': [
    ],
    },
}

event = service.events().insert(calendarId='primary', body=event).execute()
print ('Event created: %s' % (event.get('htmlLink')))