import sqlite3
import zmq
import datetime

def open_db(dbName):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()

    return (conn, cursor)

def close_db(conn):
    conn.close()

def create_tasks_table(conn, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            desc TEXT,
            ddate TEXT NOT NULL,
            priority TEXT,
            time REAL NOT NULL
        )
    ''')

    conn.commit()

def create_todos_table(conn, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            taskId INTEGER NOT NULL,
            FOREIGN KEY(taskId) REFERENCES tasks(id)
        )
    ''')

    conn.commit()

def create_stats_table(conn, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS months (
            id TEXT PRIMARY KEY,
            time REAL,
            overdue INTEGER,
            count INTEGER
        )
    ''')

    conn.commit()
    create_months(conn, cursor)

def create_months(conn, cursor):
    months = [
        ("01", 0, 0, 0),
        ("02", 0, 0, 0), 
        ("03", 0, 0, 0), 
        ("04", 0, 0, 0), 
        ("05", 0, 0, 0), 
        ("06", 0, 0, 0), 
        ("07", 0, 0, 0), 
        ("08", 0, 0, 0), 
        ("09", 0, 0, 0), 
        ("10", 0, 0, 0), 
        ("11", 0, 0, 0), 
        ("12", 0, 0, 0)]
    cursor.executemany("INSERT OR IGNORE INTO months (id, time, overdue, count) VALUES (?, ?, ?, ?)", months)

    conn.commit()

def create_task(conn, cursor, name, ddate, desc=None, priority=None):
    cursor.execute("INSERT INTO tasks (name, desc, ddate, priority, time) VALUES (?, ?, ?, ?, ?)", 
                   (name, desc, ddate, priority, 0))
    conn.commit()
    return get_last_id(cursor, "tasks")
    

def get_last_id(cursor, tableName):
    cursor.execute("select seq from sqlite_sequence where name=?", (tableName,))
    id = cursor.fetchone()

    return id[0]

def create_todo(conn, cursor, name, taskId):
    cursor.execute("INSERT INTO todos (name, taskId) VALUES (?, ?)", 
                   (name, taskId))

    conn.commit()

def read_tasks(cursor):
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    return tasks

def read_todos(cursor, taskId):
    cursor.execute("SELECT * FROM todos WHERE taskId=?", (taskId,))
    todos = cursor.fetchall()

    return todos

def read_task(cursor, taskId):
    cursor.execute("SELECT * FROM tasks WHERE id=?", (taskId,))
    task = cursor.fetchall()

    return task

def read_todo(cursor, todoId):
    cursor.execute("SELECT * FROM todos WHERE id=?", (todoId,))
    todo = cursor.fetchall()

    return todo

def update_task(conn, cursor, taskId, name, ddate, desc=None, priority=None, time='0'):
    currentTime = get_time(cursor, taskId)
    newTime = eval(time) + currentTime
    cursor.execute("UPDATE tasks SET name=?, desc=?, ddate=?, priority=?, time=? WHERE id=?", (name, desc, ddate, priority, newTime, taskId))

    conn.commit()

def update_todo(conn, cursor, todoId, name, taskId):
    cursor.execute("UPDATE todos SET name=?, taskId=? WHERE id=?", 
                   (name, taskId, todoId))
    
    conn.commit()

def delete_task(conn, cursor, taskId):
    delete_todos(conn, cursor, taskId)
    cursor.execute("DELETE FROM tasks WHERE id=?", (taskId,))

    conn.commit()

def delete_todo(conn, cursor, todoId):
    cursor.execute("DELETE FROM todos WHERE id=?", (todoId,))

    conn.commit()

def delete_todos(conn, cursor, taskId):
    cursor.execute("DELETE FROM todos WHERE taskId=?", (taskId,))

    conn.commit()

def get_time(cursor, taskId):
    cursor.execute("SELECT * FROM tasks WHERE id=?", (taskId,))
    time = cursor.fetchone()
    if time != None:
        return time[5]

def get_month(cursor, month):
    cursor.execute("SELECT * FROM months WHERE id=?", (month,))
    count = cursor.fetchone()
    return (count[1], count[2], count[3])

def update_month(conn, cursor, month, time, overdueCheck):
    currTime, overdue, count = get_month(cursor, month)
    count += 1
    overdue += overdueCheck
    if time != None:
        currTime += time
    cursor.execute("UPDATE months SET time=?, overdue=?, count=? WHERE id=?", (currTime, overdue, count, month))

    conn.commit()

def get_months(cursor):
    cursor.execute("SELECT * FROM months")
    months = cursor.fetchall()
    return months

if __name__ == '__main__':
    conn, cursor = open_db('Tasks.db')
    today = datetime.date.today()

    create_tasks_table(conn, cursor)
    create_todos_table(conn, cursor)
    create_stats_table(conn, cursor)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5553')

    while True:
        message, command = eval(socket.recv_string())
        
        if message == "getTasks":
            socket.send_string(str(read_tasks(cursor)))
        
        elif message == "getTodos":
            socket.send_string(str(read_todos(cursor, command)))

        elif message == "createTask":
            socket.send_string(str(create_task(conn, cursor, command[0], command[2], command[1], command[3])))

        elif message == "createTodo":
            socket.send_string(str(create_todo(conn, cursor, command[0], command[1])))

        elif message == "updateTask":
            update_task(conn, cursor, command[4], command[0], command[2], command[1], command[3], command[5])
            socket.send_string("Task successfully updated.")

        elif message == "updateTodo":
            update_todo(conn, cursor, command[0], command[1], command[2])
            socket.send_string("todo updated")

        elif message == "deleteTask":
            delete_task(conn, cursor, command[0])
            socket.send_string("Task successfully deleted.")
        
        elif message == "deleteTodo":
            delete_todo(conn, cursor, command[0])
            socket.send_string("todo deleted")

        elif message == "getTime":
            time = get_time(cursor, command[0])
            socket.send_string(str(time))

        elif message == "updateMonth":
            update_month(conn, cursor, command[0], command[1], command[2])
            socket.send_string("Month updated")
        
        elif message == "getMonths":
            socket.send_string(str(get_months(cursor)))