import sqlite3
import random

connection = sqlite3.connect('probot.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    name VARCHAR(255) NOT NULL,
    est_duration INT NOT NULL,
    actual_completion_time INT,
    diff_class VARCHAR(255),
    complete BIT
)               
""")

connection.commit()
connection.close()

def add_task(name, est_time, diff):
    """
    Add new tasks to table

    Parameters: - name is the tasks name
                - est_time is the users estimated time to complete task
                - diff is the tasks difficulty class

    Returns: none
    """
    connection = sqlite3.connect('probot.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?)", (name, est_time, None, diff, 0))

    connection.commit()
    connection.close()

def finish_task(name, acc_time):
    """
    Checks to see if task has been completed,
    if not, set the complete bit to 1 and set actual time of completion.

    Parameters: - name of task that has been completed
                - acc_time is the actual time it took to complete the task
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
        vals = (int(acc_time+0.5), 1, name)
        cursor.execute(sql, vals) 

    connection.commit()
    connection.close()

def get_times(diff):
    """
    Retrieves times from all completed tasks of a certain difficulty class

    Parameters: - diff is the difficulty class of the task that is being scheduled.
                  it is passed in to see how the user performed on tasks of the same
                  difficulty class in the past, so that ffNN.py can accurately adjust 
                  the duration and importance of the task.
                  
    Return:     - ret is a list of tuples of the times (est, actual) 
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
    Get names of all currently active tasks

    Parameters: none

    Return:     - ret contains the names of all currently active tasks
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
    Programmer testing utility
    '''
    connection = sqlite3.connect('probot.db')
    cursor = connection.cursor()

    sql = "SELECT * FROM tasks"
    cursor.execute(sql)

    ret = cursor.fetchall()

    connection.close()

    return ret

def ran():
    '''
    Programmer testing utility
    '''
    return random.randint(1, 5)

def remove_unfinished():
    '''
    Programmer testing utility
    '''
    connection = sqlite3.connect('probot.db')
    cursor = connection.cursor()

    sql = "DELETE FROM tasks WHERE complete=0"
    cursor.execute(sql)

    connection.commit()
    connection.close()

def clear_table():
    '''
    Programmer utility
    '''
    connection = sqlite3.connect('probot.db')
    cursor = connection.cursor()

    sql = "DELETE FROM tasks"
    cursor.execute(sql)

    connection.commit()
    connection.close()
