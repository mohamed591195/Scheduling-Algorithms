

# EDF Scheduler
def EDF(tasks, max_time):
    task_values = []
    for key, value in tasks.items():
        value["executed"] = 0
        # value["instance_number"] = 1
        value["task_id"] = key
        task_values.append(value)
        # sort the tasks based on their deadlines
    # sort the tasks based on their deadlines
    output = []
    deadline_missed = 0

    for time in range(0, max_time):
        # find the tasks that are ready to be executed
        ready_task = {"period": 0, "deadline": max_time}

        for task in task_values:
            if task["executed"] == task["execution_time"]:
                task["executed"] = 0
                task["release_time"] += task["period"]
                task["deadline"] += task["period"]
            if time - task["release_time"] == task["period"]:
                new_task = task.copy()
                new_task["release_time"] = time
                new_task["deadline"] = task["deadline"] + task["period"]
                task_values.append(new_task)
            # if task["deadline"] < time:
            #     deadline_missed = task["deadline"]
                # task_values.remove(task)

            if time >= task["release_time"]:
                if task["deadline"] < ready_task["deadline"]:
                    ready_task = task

        if ready_task["period"] == 0:
            continue
        output.append(
            [
                ready_task["task_id"],
                time,
                time + 1,
            ]
        )
        ready_task["executed"] += 1
        result = {}
        for ts in task_values:
            task_priods = []
            for task in output:
                if task[0] == ts["task_id"]:
                    task_priods.append([task[1], task[2]])
            result[ts["task_id"]] = task_priods
        if time > ready_task["deadline"]:
            deadline_missed = ready_task["deadline"]
            break

    return result, deadline_missed


# DMA Scheduler
def DMA(tasks, max_time):
    task_values = []
    for key, value in tasks.items():
        value["executed"] = 0
        value["task_id"] = key
        task_values.append(value)

        # sort the tasks based on their deadlines
    output = []
    deadline_broken = False
    # sort the tasks based on their deadlines
    task_values.sort(key=lambda x: x["deadline"])
    # assign priorities to the tasks based on their deadlines
    for i, task in enumerate(task_values):
        task["priority"] = i
    # loop through each time step
    for time in range(0, max_time):
        ready_task = {"priority": max_time, "deadline": max_time}

        # check if the task is fully executed
        for task in task_values:
            if task["executed"] == task["execution_time"]:
                task["executed"] = 0
                task["release_time"] += task["period"]
                task["deadline"] += task["period"]
            # if the period of the task is equal to the time step, create a new task
            if time - task["release_time"] == task["period"]:
                new_task = task.copy()
                new_task["release_time"] = time
                new_task["deadline"] = task["deadline"] + task["period"]
                task_values.append(new_task)
            # if the deadline broken
            if task["deadline"] < time:
                deadline_broken = True
                # task_values.remove(task)

            # get the task with the highest priority that is ready to be executed
            if time >= task["release_time"]:
                if task["priority"] < ready_task["priority"]:
                    ready_task = task

        # if no task is ready to be executed, skip to the next time step
        if ready_task["priority"] == max_time:
            continue

        output.append(
            [
                ready_task["task_id"],
                time,
                time + 1,
            ]
        )
        # execute i second of the task
        ready_task["executed"] += 1

        result = {}
        for ts in task_values:
            task_priods = []
            for task in output:
                if task[0] == ts["task_id"]:
                    task_priods.append([task[1], task[2]])
            result[ts["task_id"]] = task_priods

    return result, deadline_broken


# RMA Scheduler


def RMA(tasks, max_time):
    task_values = []
    for key, value in tasks.items():
        value["executed"] = 0
        value["task_id"] = key
        task_values.append(value)

        # sort the tasks based on their deadlines
    output = []
    deadline_broken = False
    time = 0
    task_values.sort(key=lambda x: x["period"])
    for i, task in enumerate(task_values):
        task["priority"] = i
    for time in range(0, max_time):
        time1 = time
        ready_task = {"priority": max_time, "deadline": max_time}

        for task in task_values:
            if task["executed"] == task["execution_time"]:
                task["executed"] = 0
                task["release_time"] += task["period"]
                task["deadline"] += task["period"]
            if time - task["release_time"] == task["period"]:
                new_task = task.copy()
                new_task["release_time"] = time
                new_task["deadline"] = task["deadline"] + task["period"]

                task_values.append(new_task)
            if task["deadline"] < time:
                deadline_broken = True
                # task_values.remove(task)

            if time >= task["release_time"]:
                if task["priority"] < ready_task["priority"]:
                    ready_task = task

        if ready_task["priority"] == max_time:
            continue

        output.append(
            [
                ready_task["task_id"],
                time,
                time + 1,
            ]
        )
        ready_task["executed"] += 1

        result = {}
        for ts in task_values:
            task_priods = []
            for task in output:
                if task[0] == ts["task_id"]:
                    task_priods.append([task[1], task[2]])
            result[ts["task_id"]] = task_priods

    return result, deadline_broken


def FIFO(tasks, max_time):

    scheduled_tasks = {}
    timeline_sections = {}
    deadline_missed = 0

    # we sort tasks according to first release time before starting, 
    # so later when two jobs of different tasks are released at the same time,
    # we can schedule them in the order they are released with
    sorted_tasks = dict(sorted(tasks.items(), key=lambda x: x[1]['release_time']))
    
    for task_name, task in sorted_tasks.items():
        release_time = task['release_time']
        deadline = task['deadline']
        period = task['period']
        tasks[task_name]['release_times'] = list(range(release_time, max_time*2, period))
        tasks[task_name]['deadlines'] = list(range(deadline, max_time*2, period))
        timeline_sections[task_name] = []

    timer = 0
    while timer <= max_time: 
        for task_name, task in sorted_tasks.items():    # maybe two jobs of different tasks are released at the same time
                                                        # for that we sorted tasks earlier by release time, so that the job of the task
                                                        # released first will be scheduled first
            if task['release_times'][0] <= timer:
                scheduled_tasks[task_name] = task['release_times'].pop(0)

        if scheduled_tasks:
            # problem here is that when two jobs are released at the same time,
            # we can't sort them by their respective first release time priority
            # therefore we sorted them earlier as sorted_tasks
            # then different jobs in their current release time are sorted according to it
            sorted_scheduled_tasks = dict(sorted(scheduled_tasks.items(), key=lambda x: x[1]))
            
            for item in sorted_scheduled_tasks.items(): # item = ('Task 1', 0)
                start = timer
                timer += sorted_tasks[item[0]]['execution_time']

                # detection of deadline miss
                deadline = tasks[item[0]]['deadlines'].pop(0)
                if timer > deadline:
                    
                    timeline_sections[item[0]].append([start, deadline])
                    deadline_missed = deadline
                    # to exit outer while loop
                    timer = max_time + 1
                    # then exit inner for loop
                    break

                timeline_sections[item[0]].append([start, timer])
                
            scheduled_tasks = {}
            continue
        timer += 1
    return timeline_sections, deadline_missed


