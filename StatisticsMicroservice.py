import zmq
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.figsize'] = (20, 10)

def construct_graph(data):
    x = []
    y1 = []
    y2 = []

    for i in data:
        x.append(i[0])

        if i[3]-i[2] > 0:
            y1.append(round(i[1]/(i[3]-i[2]), 2))
        else:
            y1.append(0)
        if i[2] > 0:
            y2.append(round(i[1]/i[2], 2))
        else:
            y2.append(0)

    plt.bar(x, y1, color='r')
    plt.bar(x, y2, bottom=y1, color='b')

    plt.xlabel('Month')
    plt.ylabel('Average Time spent on Tasks (seconds)')
    plt.title('Monthly Averages of Time spent Working on Tasks')
    plt.legend(["On Time", "Overdue"], loc="upper right")

    plt.show()

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5552')

    while True:
        message, command = eval(socket.recv_string())

        if message == 'getStats':
            socket.send_string('Showing stats')
            construct_graph(command)