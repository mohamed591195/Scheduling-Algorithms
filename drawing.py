import matplotlib.pyplot as plt

# tasks = {'Task 1': [[0, 2], [8, 10], [12, 14], [23, 24]], 'Task 2': [[2, 4], [10, 12], [17, 19]], 'Task 3': [[4, 8], [19, 23]]}


def draw_tasks(tasks, deadline_missed=0):
    fig, ax = plt.subplots(figsize=(10, 4))
    y = 0
    y_labels = []
    x_ticks = []
    height = 0.2
    y_scale = 0.2
    colors = ['skyblue', 'lightgreen', 'lightpink', 'lightcoral', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightsteelblue', 'lightyellow']  # Define a list of colors
    for task_name, task in tasks.items():
        y_labels.append(task_name)
        for start, end in task:
            x_ticks.extend([start, end])
            ax.barh(y*y_scale, end-start, left=start, height=height, color=colors[y % len(colors)], edgecolor='black')  # Use a different color for each task
            ax.axvline(x=end, color='b', linestyle=':', linewidth=1)
            ax.axhline(y= y * y_scale - height/2, color='b', linestyle=':', linewidth=0.5)  # Add vertical line at the end of the task
        y += 1
    if deadline_missed: # If the deadline_missed parameter is set, draw a red vertical line at the end of the last task
        ax.axvline(x=deadline_missed, color='r', linestyle='-', linewidth=1) 
        ax.text(deadline_missed, -0.1, 'Deadline Miss', color='r', ha='center', va='top')  # Add text under the x-axis
        
    ax.set_yticks([y * y_scale for y in range(len(y_labels))])
    ax.set_yticklabels(y_labels)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks)
    plt.show()

# draw_tasks(tasks, deadline_missed=24)