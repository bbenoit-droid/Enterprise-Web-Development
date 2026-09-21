import time
import numpy as np
import matplotlib
matplotlib.use('TkAgg') #interactive backend
import matplotlib.pyplot as plt

def time_complexity_visualizer(algorithm, n_min, n_max, n_step):
    times = []
    input_sizes = list(range(n_min, n_max + 1, n_step))

    plt.ion()  # Enable on interactive mode
    fig, ax = plt.subplots()
    ax.set_xlabel('Input size')
    ax.set_ylabel('Running time (seconds)')
    ax.set_title('Algorithm time complexity visualization (Live)')
    line, = ax.plot([], [], 'o-')

    for i, n in enumerate(input_sizes):
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)

        # Update the plot with new data point
        line.set_data(input_sizes[:i + 1], times)
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)  # Small pause to allow the plot to refresh

        plt.ioff()  # Disable interactive mode
        plt.show() # Keep plot open

        def linear_search(n):
            for i in range(n): 
                pass

        time_complexity_visualizer(linear_search, 1000, 100, 1000)