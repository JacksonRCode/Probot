from getCpds import *
from getInput import *
from templan import *
from create_tables import *
from bNet import *

print("Hello!")
print()

cont = True

task_list = []

while cont:
    print("What would you like to do?")
    print("__________________________")
    print("1. Create Task")
    print("2. Finish Task")
    print("3. Generate Schedule")
    print("__________________________")
    print("__________________________")
    print()
    choice = int(input("Please enter 1, 2 or 3: "))

    # Create task
    if choice==1:
        name = str(input("What is the name of this task: "))
        # Get task values [Name, evidence, duration]
        task, difficultyClass = getAllInput(name)

        # Calculate importance value
        posterior = inference.query(variables=['I'], evidence=task[1])
        
        # Set value to proper spot in task
        task[1] = posterior.values[1]

        # Add task to DB
        add_task(name, task[2], difficultyClass)
        
        # Add task to list of tasks
        task_list.append(task)
        print(task_list)

    # Complete task
    elif choice == 2:
        pass

    # Generate schedule
    elif choice == 3:
        cont = False
        tasks_planned = [["Beer with friend", 9, 10], ["Coffee with friend", 11, 13]]
        schedule = schedule_day(9, 17, tasks_planned, task_list)

        print(schedule)
        pass

    else:
        print("********************************")
        print("That input is invalid, try again")
        print("********************************")
        print()

