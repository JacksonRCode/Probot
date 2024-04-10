import sqlite3

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS tasks (
#     name VARCHAR(255) NOT NULL,
#     est_duration INT NOT NULL,
#     actual_completion_time INT,
#     diff_class VARCHAR(255),
#     complete BIT
# )               
# """)

def add_task(name, est_time, diff):
    """
    Add new tasks to table
    """
    connection = sqlite3.connect('probot.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?)", (name, est_time, None, diff, 0))

    connection.commit()
    connection.close()

def finish_task(name, acc_time):
    """
    Checks to see if task has been completed,
    if not, set to complete bit to 1 and set actual time of completion.
    """
    connection = sqlite3.connect('probot.db')
    cursor = connection.cursor()

    cursor.execute("SELECT complete FROM tasks WHERE name=?", (name,))
    status = cursor.fetchone()

    if status[0]==0:
        sql = ''' UPDATE tasks
                  SET actual_completion_time = ?,
                      complete = ?
                  WHERE name = ?
              '''
        vals = (acc_time, 1, name)
        cursor.execute(sql, vals) 

    connection.commit()
    connection.close()

def get_times(diff):
    """
    Retrieves times from all completed tasks of a certain difficulty class

    Returns list of tuples of the times (est, actual) 
    """
    connection = sqlite3.connect('probot.db')
    cursor = connection.cursor()

    sql = "SELECT est_duration, actual_completion_time FROM tasks WHERE (diff_class = ? AND complete = 1)"
    cursor.execute(sql, (diff,))

    ret = cursor.fetchall()

    connection.commit()
    connection.close()  
    
    # Returns list of tuples: [(estimated_time, actual_time),(et, at), ...]
    return ret

def get_current_task_names():
    '''
    Returns the names of all currently active tasks
    '''
    connection = sqlite3.connect('probot.db')
    cursor = connection.cursor()

    sql = "SELECT name FROM tasks WHERE complete = 0"
    cursor.execute(sql)

    ret = cursor.fetchall()

    connection.close()

    return ret

def look_at_table():
    '''
    Check table contents for programmer use
    '''
    connection = sqlite3.connect('probot.db')
    cursor = connection.cursor()

    sql = "SELECT * FROM tasks"
    cursor.execute(sql)

    ret = cursor.fetchall()

    connection.close()

    return ret
