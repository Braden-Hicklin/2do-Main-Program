import mysql.connector
from mysql.connector import Error 

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: {err}")
    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: {err}")
    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: {err}")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: {err}")

def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def insert_task(connection, name, description=None, priority=None):
    if name and len(name) > 64:
        print("Name exceeds character limit, reducing to 64 characters.")
        name = name[:64]
    if description and len(description) > 256:
        print("Description exceeds character limit, reducing to 256 characters.")
        description = description[:256]
    q = """
    INSERT INTO task (task_name, description, priority)
    VALUES (%s, %s, %s);
    """
    val = [(name, description, priority)]
    execute_list_query(connection, q, val)
    return get_task_id(connection)

def get_task_id(connection):
    q = """
    SELECT LAST_INSERT_ID();
    """
    id = 0
    for data in read_query(connection, q):
        id=data[0]
    return id

def insert_todo(connection, name, task_id):
    if name and len(name) > 64:
        print("Name exceeds character limit, reducing to 64 characters.")
        name = name[:64]
    q = """
    INSERT INTO todo (todo_name, task_id)
    VALUES (%s, %s);
    """
    val = [(name, task_id)]
    execute_list_query(connection, q, val)
    return get_task_id(connection)

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: {err}")

def get_db(connection, db):
    q = f"""
    SELECT *
    FROM {db};
    """
    return read_query(connection, q)

def get_all_tasks(connection):
    q = f"""
    SELECT *
    FROM task;
    """
    newli = []
    for data in read_query(connection, q):
        newli.append([data[0], data[1], data[2], data[3]])
    return newli

def get_task(connection, task_id):
    q = f"""
    SELECT task_id, task_name, description, priority
    FROM task
    WHERE task_id = {task_id};
    """
    newli = []
    for data in read_query(connection, q):
        newli.append(data[0])
        newli.append(data[1])
        newli.append(data[2])
        newli.append(data[3])
    return newli

def get_todo(connection, task_id):
    q = f"""
    SELECT todo_id, todo_name, task_id
    FROM todo
    WHERE todo.task_id = {task_id};
    """
    newli = []
    for data in read_query(connection, q):
        newli.append([data[0], data[1], data[2]])
    return newli

def update_task(connection, id, name=None, description=None, priority=None):
    currComponents = get_task(connection, id)
    name = currComponents[1] if name == None else name
    description = currComponents[2] if description == None else description
    priority = currComponents[3] if priority == None else priority
    q = """
    UPDATE task
    SET task_name = %s, description = %s, priority = %s
    WHERE task_id = %s;
    """
    val = [(name, description, priority, id)]
    execute_list_query(connection, q, val)

def update_todo(connection, id, name):
    q = """
    UPDATE todo
    SET todo_name = %s
    WHERE todo_id = %s;
    """
    val = [(name, id)]
    execute_list_query(connection, q, val)

def delete_task(connection, id):
    li = get_todo(connection, id)
    if len(li) != None:
        delete_all_todos(connection, id)
    q = f"""
    DELETE FROM task
    WHERE task_id = {id};
    """
    execute_query(connection, q)

def delete_todo(connection, id):
    q = f"""
    DELETE FROM todo
    WHERE todo_id = {id};
    """
    execute_query(connection, q)

def delete_all_todos(connection, id):
    q = f"""
    DELETE FROM todo
    WHERE task_id = {id};
    """
    execute_query(connection, q)

create_task_table = """
CREATE TABLE task (
    task_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    task_name VARCHAR(64) NOT NULL,
    description VARCHAR(256),
    priority VARCHAR(6)
    );
"""

create_todo_table = """
CREATE TABLE todo (
    todo_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    todo_name VARCHAR(64) NOT NULL,
    task_id INT,
    FOREIGN KEY (task_id) REFERENCES task(task_id)
    );
"""

alter_todo = """
ALTER TABLE todo
ADD FOREIGN KEY(task)
REFERENCES task(task_id)
ON DELETE SET NULL;
"""