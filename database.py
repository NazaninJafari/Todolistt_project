import sqlite3

con = sqlite3.connect("Todolist.db")
my_cursor = con.cursor()

def getAll():
    my_cursor.execute("SELECT * FROM tasks")
    result = my_cursor.fetchall()
    return result

def add(id ,title , desc, done, time, date, priority):
    my_cursor.execute(f'INSERT INTO tasks(id, title, description, done, time, date, priority) VALUES({id}, "{title}", "{desc}",{done}, "{time}", "{date}", {priority})')
    con.commit()    


def done_update(id, x):
    my_cursor.execute(f'UPDATE tasks SET done= {x} WHERE id= {id}')
    con.commit()

def delet_fromdatabase(id):
    my_cursor.execute(f'DELETE FROM tasks WHERE id= {id}')
    con.commit()