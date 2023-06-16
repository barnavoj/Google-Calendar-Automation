"""
Automatic Creation of google calendar events using Google API and PDF reader
"""


from datetime import datetime, timedelta
import PyPDF2

from Google import create_service


def read_pdf(src_path, start_keyword, stop_keyword):
    """
    Reads pdf file with readable text. Returns a list of rows of interest.

    Args:
        src_path (str): Source path of PDF file.
        start_keyword (str): A keyword from which to begin making rows
        stop_keyword (str): A keyword at which to end making rows

    Returns:
        list of str: Extracted rows of text.
    """
    reader = PyPDF2.PdfReader(src_path)
    string = reader.pages[0].extract_text()
    string = string.split(start_keyword)[1].split(stop_keyword)[0]
    rows_list = string.split("\n")
    return rows_list


def main():

    # Connecting to Google API
    CLIENT = "client_secret_754421839897-mm7ictagubbvt5uengtjfqsm12b6dim8.apps.googleusercontent.com.json"
    API = "calendar"
    API_V = "v3"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]

    service = create_service(CLIENT, API, API_V, SCOPES)

    # Geting strings to write to events
    rows_list = read_pdf('Barnat Vojtěch rozpis.pdf', "*Vyšetření", "Důležité")
    rows_list = rows_list[1:-1]

    # For each second row create event
    for i, s in enumerate(rows_list):
        s = s.replace(" (Čt)" ," (Út)").split(" (Út)")

        if i%2 == 0:
            date = s[0]

        if i%2 == 1:
            time = s[0]
            event = s[1]


            date_time = datetime.strptime(date + " " + time, '%d.%m.%Y %H:%M')
            end_time = date_time + timedelta(minutes=40)
            
            event = {
                'summary': 'Rehabilitace',
                'location': 'Rehabilitační Nemocnice Beroun',
                'description': event,
                'start': {
                'dateTime': date_time.strftime('%Y-%m-%dT%H:%M') + ":00",
                'timeZone': 'Europe/Prague',
                },
                'end': {
                'dateTime': end_time.strftime('%Y-%m-%dT%H:%M') + ":00",
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
            

if __name__ == "__main__":
    main()