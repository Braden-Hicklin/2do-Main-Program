import zmq
import time
import datetime

# set up context for ZMQ pipeline
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

stopwatch_time = 0
timer_running = False

def getDate():
    now = datetime.date.today()
    sent_message = now.strftime("%d-%m-%Y")
    socket.send_string(sent_message)
    print("Date sent!")

def getStopwatchTime():
    global stopwatch_time
    current_time = time.time() - stopwatch_time
    socket.send_string(str(current_time))
    print("Time retrieved!")

def stopTimer():
    global timer_running, stopwatch_time
    elapsed_time = time.time() - stopwatch_time
    timer_running = False
    socket.send_string(str(elapsed_time))
    print("Timer stopped!")

# loop to run, consistently communicating
while True:
    try:
        message = socket.recv()
        message = message.decode()
    except:
        print("message not sent yet")

    if (message == "getDate"):
        getDate()
    elif (message == "getStopwatchTime"):
        if timer_running != True:
            stopwatch_time = time.time()
            timer_running = True
        getStopwatchTime()
    elif (message == "stopTimer"):
        stopwatch_time = 0
        stopTimer()
    else:
        print("No command received, or unknown command received")