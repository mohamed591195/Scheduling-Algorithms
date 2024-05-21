import tkinter as tk
from tkinter import ttk
from algorithms import *
from mlf import MLF
from round_robin import RR
from drawing import draw_tasks

class TaskSchedulerGUI:
    def __init__(self, master):
        self.master = master
        
        self.algorithms = ["FIFO", "RR", "EDF", "MLF", "RMA", "DMA"]
        self.task_frames = []
        self.font = ("Iceberg Regular", 20 * -1)

        self.entry_style = {
            'bd': 1,  # Border width
            'bg': "#FFFFFF",  # Background color
            'fg': "#000716", # Foreground color
            'highlightthickness': 1, # Highlight thickness
            'width': 5, # Width of the entry widget
            'font': self.font
        }

        self.master.title("Task Scheduler")
        self.master.geometry("1100x600")
        self.master.resizable(True, True)
        self.master.configure(background="#C4E4F2")
        
        # Create labels and dropdown for number of tasks and scheduling policy
        self.task_label = ttk.Label(master, text="Enter number of tasks:", font=self.font)
        self.task_entry = tk.Entry(master, **self.entry_style)
        self.task_entry.insert(0, "3")  # Initialize with 3 tasks
        self.generate_task_fields()

        self.policy_label = tk.Label(master, text="Scheduling Policy:", font=self.font)
        
        self.policy_var = tk.StringVar()
        self.policy_dropdown = ttk.Combobox(master, textvariable=self.policy_var, values=self.algorithms, font=self.font)
        self.policy_dropdown.current(0)
        #set plicy_dropdown read only
        self.policy_dropdown.config(state="readonly")

         # Create labels for maximum time and quantum_time
        self.max_time_label = tk.Label(master, text="Maximum Time:", font=self.font)
        self.max_time_entry = tk.Entry(master, **self.entry_style)
        self.max_time_entry.insert(0, "30")

        self.quantum_time_label = tk.Label(master, text="Quantum Time:", font=self.font)
        self.quantum_time_entry = tk.Entry(master, **self.entry_style)
        self.quantum_time_entry.insert(0, "1")

        self.notice_label = tk.Label(master, text="Note: priority fields are only for (preemptive and non-preemptive)", font=self.font, bg="#FFFB92")
        
        # Create a button to generate task input fields
        self.generate_button = tk.Button(master, text="Generate Tasks Fields", command=self.generate_task_fields)
        self.caclulate_button = tk.Button(master, text="Draw Graph", command=self.draw_graph)
        self.task_label.place(x=270, y=30)
        self.task_entry.place(x=500, y=30)
        
        self.policy_label.place(x=270, y=65)
        self.policy_dropdown.place(x=500, y=65)
        
        self.max_time_label.place(x=270, y=100)
        self.max_time_entry.place(x=500, y=100)
        
        self.quantum_time_label.place(x=620, y=100)
        self.quantum_time_entry.place(x=760, y=100)
        
        # self.notice_label.place(x=270, y=135)
        self.generate_button.place(x=470, y=170)
        self.caclulate_button.place(x=600, y=170)

    def generate_task_fields(self):
        num_tasks = int(self.task_entry.get())

        # Clear existing task frames
        for frame in self.task_frames:
            frame.destroy()
        self.task_frames = []

        # Create input fields for each task
        for i in range(num_tasks):
            y = (i*100)+ 200
            task_frame = tk.Frame(self.master, bd=2, relief=tk.SUNKEN, padx=10, pady=10, bg="#EF6363", )
            task_frame.place(x=20, y=y)

            task_label = tk.Label(task_frame, text=f"Task No.{i+1}")
            task_label.pack(side=tk.TOP, pady=10)

            release_time_label = tk.Label(task_frame, text="Release time:")
            release_time_label.pack(side=tk.LEFT)
            task_frame.release_time_entry = tk.Entry(task_frame)
            task_frame.release_time_entry.pack(side=tk.LEFT, padx=10)

            period_label = tk.Label(task_frame, text="Period:")
            period_label.pack(side=tk.LEFT)
            task_frame.period_entry = tk.Entry(task_frame)
            task_frame.period_entry.pack(side=tk.LEFT, padx=10)

            priority_label = tk.Label(task_frame, text="Priority:")
            priority_label.pack(side=tk.LEFT)
            task_frame.priority_entry = tk.Entry(task_frame)
            task_frame.priority_entry.insert(0, "0")  # Initialize with 0 priority
            task_frame.priority_entry.pack(side=tk.LEFT, padx=10)

            execution_time_label = tk.Label(task_frame, text="Execution time:")
            execution_time_label.pack(side=tk.LEFT)
            task_frame.execution_time_entry = tk.Entry(task_frame)
            task_frame.execution_time_entry.pack(side=tk.LEFT, padx=10)

            deadline_label = tk.Label(task_frame, text="Deadline:")
            deadline_label.pack(side=tk.LEFT)
            task_frame.deadline_entry = tk.Entry(task_frame)
            task_frame.deadline_entry.pack(side=tk.LEFT, padx=10)

            # Create an empty label at the bottom of the frame

            self.task_frames.append(task_frame)

    def draw_graph(self):
        # Initialize an empty list to store the task values
        tasks = {}
        tasksRR = {}
    
        # Loop through each task frame
        for idx, task_frame in enumerate(self.task_frames):
            # Get the values from the entry widgets
            release_time = int(task_frame.release_time_entry.get())
            period = int(task_frame.period_entry.get())
            priority = int(task_frame.priority_entry.get())
            execution_time = task_frame.execution_time_entry.get()
            deadline = int(task_frame.deadline_entry.get())
      
    
            # Store the values in a dictionary and add it to the list
            tasks[f'Task {idx}'] = {
                'release_time': release_time,
                'period': period,
                'priority': priority,
                'execution_time': float(execution_time),
                'deadline': deadline
            }
            tasksRR[f'Task {idx}'] = {
                'release_time': task_frame.release_time_entry.get(),
                'period': task_frame.period_entry.get(),
                'priority': task_frame.priority_entry.get(),
                'execution_time': task_frame.execution_time_entry.get(),
                'deadline': task_frame.deadline_entry.get()
            }

        # Get the scheduling policy value
        policy = self.policy_var.get()
        # Get the maximum time and quantum_time values
        max_time = int(self.max_time_entry.get())
        quantum_time = self.quantum_time_entry.get()
        print("quantum_time", quantum_time)
        print("execution_time", execution_time)

        # Print the values for testing
        print(tasks)
        if policy == "FIFO":
            print(tasks, max_time)
            draw_tasks(*FIFO(tasks, max_time))
        elif policy == "RR":
            draw_tasks(*RR(tasksRR, max_time, quantum_time))
        elif policy == "EDF":
            draw_tasks(*EDF(tasks, max_time))
        elif policy == "MLF":
            draw_tasks(*MLF(tasks, max_time))
        elif policy == "RMA":
            draw_tasks(*RMA(tasks, max_time))
        elif policy == "DMA":
            draw_tasks(*DMA(tasks, max_time))

root_window = tk.Tk()
TaskSchedulerGUI(root_window)
root_window.mainloop()