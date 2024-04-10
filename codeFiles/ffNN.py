'''
Feedforward neural network for optimizing 
task duration based on users history
'''

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from create_tables import *



def adjust_times(diff, time, importance):
    '''
    Uses the users completed tasks of a certain difficulty class
    to estimate how long a users new task will take.

    Parameters: diff - difficulty class.
                time - users time estimate for new task.
                importance - calculated importance for new task.

    Returns:    time - time estimate for new task based on history.
                importance - new importance value calculated based on
                             difference in user estimated time and computer
                             estimated time.
    '''

    estimated_times = []
    actual_times = []

    # Get previous time values from database
    time_tuples = get_times(diff)

    for tuple in time_tuples:
        estimated_times.append(tuple[0])
        actual_times.append(tuple[1])

    estimated_times = np.array(estimated_times)
    actual_times = np.array(actual_times)


    # Won't get a good estimate unless there are "enough" samples to train on
    if len(actual_times) <= 5:
        return time, importance

    # Define the model
    model = Sequential([
        Input(shape=(1,)),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1)
    ])

    # Create the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(estimated_times, actual_times, epochs=100, validation_split=0.2)

    # Evaluate the model
    loss = model.evaluate(estimated_times, actual_times)
    print("Mean Squared Error:", loss)

    # Use the model to predict actual times for new estimated times
    new_estimated_times = np.array([time])
    predicted_actual_times = model.predict(new_estimated_times)

    # Adjust importance based on new time
    imp = importance + (predicted_actual_times - time)*.1

    return predicted_actual_times.flatten(), imp

# t, i = adjust_times('a', 3, .65)
