from ortools.sat.python import cp_model
import pandas as pd

def schedule_day(start_time, end_time, tasks_planned, tasks_to_schedule):
    # Sort tasks and round time to whole number
    sorted_tasks = sorted(tasks_to_schedule, key=lambda x: x[1], reverse=True)
    tasks_to_schedule = [(name, importance, int(duration + 0.5)) for name, importance, duration in sorted_tasks]

    # Create a new CP-SAT model
    model = cp_model.CpModel()

    # Define variable list
    task_vars = []

    # Initialize the start time for scheduling
    current_time = start_time

    # Add new tasks to the model
    for task in tasks_to_schedule:
        task_name, _, task_duration = task
        task_start = model.NewIntVar(start_time, end_time, task_name + "_start")
        task_end = model.NewIntVar(start_time, end_time, task_name + "_end")
        task_vars.append((task_name, task_start, task_end))

        # Constraint: Task duration
        model.Add(task_end == task_start + task_duration)

        # Constraint: Tasks should be scheduled sequentially without overlap
        model.Add(task_start >= current_time)
        current_time = task_end

    # Create solver and solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Print the schedule
    schedule = []
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for task_name, task_start, task_end in task_vars:
            schedule.append([task_name, solver.Value(task_start), solver.Value(task_end)])
    else:
        print("No feasible solution found.")

    '''
    Sorry I know this is disgusting
    '''
    # s keeps track of the starting point for the next insertion
    s = 0
    for pTask in tasks_planned:
        # Start and finish are the time values for previously planned task
        start = pTask[1]
        fin = pTask[2]
        # Add on is the value you need to add to subsequent tasks in order for the times to add up
        add_on = 0
        # i_add is the index value you have to add to i in order to index the proper task
        i_add = 0
        for i in range(s, len(schedule)):
            i += i_add
            # o_bool represents whether there is overlap or not
            o_bool = 0
            start2 = schedule[i][1]
            fin2 = schedule[i][2]
            if add_on == 0:
                o_bool, diff = overlap(start, fin, start2, fin2)

            if o_bool:
                add_on += diff
                schedule[i][1] += add_on
                schedule[i][2] += add_on
                schedule.insert(i, pTask)
                # Increment starting position s as well as i_add so you start at and index the correct task
                s = i+1
                i_add += 1
            else:   
                schedule[i][1] += add_on
                schedule[i][2] += add_on

    return schedule

def overlap(startA, endA, startB, endB):
    '''
    Calculate overlaps of task times
    '''
    interval1 = pd.Interval(startA,endA,closed='neither')
    interval2 = pd.Interval(startB,endB,closed='neither')

    return interval1.overlaps(interval2), endA-startB

# Example usage
# start_time = 9  # Assuming day starts at 9 AM
# end_time = 18  # Assuming work ends at 6 PM
# tasks_planned = [["Beer with friend", 9, 10], ["Coffee with friend", 11, 13]]  # Existing tasks
# tasks_to_schedule = [("Work on project", 0.7, 2), ("Exercise", 0.8, 1), ("Read book", 0.6, 1.5)]  # Tasks to schedule


# schedule = schedule_day(start_time, end_time, tasks_planned, tasks_to_schedule)
# print(schedule)
    
