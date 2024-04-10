# from getCpds import *
from getInput import *
from templan import *
from create_tables import *
from bNet import *
from ffNN import *

inference = getInference()

cont = True

task_list = []
# [[task, task_name, task_duration, task_difficulty_class], ...1]

print("Hello!")
print()

while cont:
    print("What would you like to do?")
    print("__________________________")
    print("1. Create Task")
    print("2. Finish Task")
    print("3. Generate Schedule")
    print("4. Exit")
    print("5. Check table")
    print("__________________________")
    print("__________________________")
    print()
    choice = int(input("Please enter 1-4: "))

    # Create task
    if choice==1:
        name = str(input("What is the name of this task: "))
        # Get task values [Name, evidence, duration]
        task, difficultyClass = getAllInput(name)

        # Calculate importance value
        posterior = inference.query(variables=['I'], evidence=task[1])
        
        # Set value to proper spot in task
        imp = posterior.values[1]

        # Update est duration and importance with FFNN
        # Task[2] is user estimated duration
        dur, new_imp = adjust_values(difficultyClass, task[2], imp)

        # Fill task with proper values
        task[2] = dur
        task[1] = new_imp
        
        # task = ['Name', 'Importance value', 'Duration']

        # Add task to list of tasks
        task_list.append([task, name, dur, difficultyClass])
        # print(task_list)
        print()
        input("Enter to continue")

    # Complete task
    elif choice == 2:
        print("Current tasks: ")
        print("-----------------------------")
        task_names = get_current_task_names()
        for t_name in task_names:
            print(t_name[0])
        print("-----------------------------")
        t_name = str(input("Which task did you complete: "))
        ac_time = int(input("How long did it take you to finish it (hours): "))
        finish_task(t_name, ac_time)
        print()
        input("Enter to continue")

    # Generate schedule
    elif choice == 3:

        arg_task_list = []
        for t in task_list:
            arg_task_list.append(t[0])

        tasks_planned = [["Beer with friend", 9, 10], ["Coffee with friend", 11, 13]]
        schedule = schedule_day(9, 17, tasks_planned, arg_task_list)

        print(schedule)
        input("Enter to continue")
        print()

        # Add tasks to DB
        for t in task_list:
            add_task(t[1], t[2], t[3])

    elif choice == 4:
        cont = False
        print()
        print("Have a good day!")

    elif choice == 5:
        table = look_at_table()
        for row in table:
            print(row)
        print()
        input("Enter to continue")
    

    else:
        print("********************************")
        print("That input is invalid, try again")
        print("********************************")
        print()

