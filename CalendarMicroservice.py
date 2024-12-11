import win32com.client
import zmq
import os

months = {"01":'1',
            "02":'2',
            "03":'3',
            "04":'4',
            "05":'5',
            "06":'6',
            "07":'7',
            "08":'8',
            "09":'9',
            "10":'10',
            "11":'11',
            "12":'12'}

def get_all_appts(appointments):
    appointments.IncludeRecurrences = 'True'
    events = []
    for a in appointments:
        events.append(a.Subject)
    return events

def add_calendar_event(socket, events, name, desc, day):
    global months
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    calendar = outlook.GetDefaultFolder(9)
    appointments = calendar.Items

    if name in events:
        socket.send_string('Event already exists in calendar, check the Outlook calendar associated with this device for details')
        return events
    
    else: 
        event = appointments.Add("IPM.Appointment")
        day = months[day[:2]]+day[2:]
        print(day)

        start_time = day+" 08:00"
        end_time = day+" 20:00"

        event.Subject = name
        event.Start = start_time
        event.End = end_time
        if desc != None:
            event.Body = desc

        event.Save()
        socket.send_string('Event added successfully, task now visible in the Outlook calendar associated with this device.')
        events.append(name)
        return events

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5554")

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    calendar = outlook.GetDefaultFolder(9)
    appointments = calendar.Items

    events = get_all_appts(appointments)

    while True:
        message, command = eval(socket.recv_string())

        if message == 'addEvent':
            events = add_calendar_event(socket, events, command[0], command[1], command[2])

        if message == "viewCalendar":
            os.startfile("outlook")
            socket.send_string("Opening Outlook")
            