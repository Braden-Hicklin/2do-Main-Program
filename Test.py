from DB import *

pw = 'cs361_Fall2024'
connection = create_server_connection("localhost", "root", pw)

create_database_test = "CREATE DATABASE test2"
create_database(connection, create_database_test)

connection = create_db_connection("localhost", "root", pw, "test2")

execute_query(connection, create_task_table)
execute_query(connection, create_todo_table)

id1 = insert_task(connection, name="Mow Lawn", priority="Low")
id2 = insert_task(connection, "Mow Lawn", None, None, "Low")
print(insert_todo(connection, "Trim Edges", id2))
print(insert_todo(connection, "Trim hedges", id2))

print(get_task(connection, id1))
print(get_todo(connection, id1))
print(get_all_tasks(connection))

delete_task(connection, id1)

print(get_task(connection, id2))
print(get_all_tasks(connection))
print(get_todo(connection, id2))

delete_task(connection, id2)