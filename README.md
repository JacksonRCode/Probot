# Probot - A Productivity Robot

This application schedules a users day. Initially this is done based upon
a users previously scheduled tasks in the day, along with new tasks the user wants to incorporate into their schedule. With these new tasks, the user is prompted for metrics that contribute to the tasks difficulty and importance. With these metrics, an importance score is calculated. With this importance score and the user's estimation on how long a task will take to complete, the task is scheduled.

Once the user has completed enough tasks and has given feedback on how long the tasks actually took to complete, the algorithm takes this task completion data (users estimate on time to complete vs actual time to complete) and alters the users estimates based on his or her history.

In the future, I hope to implement a dependency queue that will stop a task from being scheduled if it relies on another task being completed beforehand.

To run the project, simply run the main file and then follow along with the prompts.