import sqlite3

connection = sqlite3.connect('probot.db')

cursor = connection.cursor()

# cursor.execute(
# """
# DROP TABLE finished_tasks
# """    
# )

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    name VARCHAR(255) NOT NULL,
    est_duration INT NOT NULL,
    actual_completion_time INT,
    diff_class VARCHAR(255),
    complete BIT
)               
""")

def add_task(name, est_time, diff):
    """
    Add new tasks to table
    """
    cursor.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?)", (name, est_time, None, diff, 0))

def finish_task(name, acc_time):
    """
    Checks to see if task has been completed,
    if not, set to complete bit to 1 and set actual time of completion.
    """
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

def get_times(diff):
    """
    Retrieves times from all completed tasks of a certain difficulty class

    Returns list of tuples of the times (est, actual) 
    """
    sql = "SELECT est_duration, actual_completion_time FROM tasks WHERE (diff_class = ? AND complete = 1)"
    cursor.execute(sql, (diff,))

    # Returns list of tuples: [(estimated_time, actual_time),(et, at), ...]
    return cursor.fetchall()


# add_task('task1', 3, 'a')
# add_task('task2', 2, 'b')
# add_task('task3', 4, 'a')

# finish_task('task1', 5)
# finish_task('task3', 3)

# print(get_times('a'))



cursor.execute(
"""
SELECT * FROM tasks
WHERE diff_class = 'a'
"""
)
print("TABLE TIME")
rows = cursor.fetchall()
print(rows)

connection.commit()

connection.close()