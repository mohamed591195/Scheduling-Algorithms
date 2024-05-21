def update_task(task, quantum_time):
    task['release_time'] += task['period']
    task['deadline'] += task['period']
    task['start_time'] = task['release_time']
    task['current_to_execute'] = min(quantum_time, task['execution_time'])
    task['remain_to_execute'] = task['execution_time'] - task['current_to_execute']


def update_tasks(tasks, current_time, quantum_time):
    test_broken = False
    for task in tasks:
        if task['start_time'] < current_time:
            task['start_time'] = current_time

        if task['start_time'] >= task['deadline'] and (task['remain_to_execute'] > 0 or task['current_to_execute'] > 0):
            test_broken = True
            update_task(task, quantum_time)

        if task['current_to_execute'] == 0:
            if task['remain_to_execute'] <= 0:
                update_task(task, quantum_time)
            else:
                task['current_to_execute'] = min(quantum_time, task['remain_to_execute'])
                task['remain_to_execute'] -= quantum_time
                task['remain_to_execute'] = max(0, task['remain_to_execute'])
    return test_broken
'''
input :
    tasks (list) : list of tasks with format 'task id'={'release_time':key, 'execution_time':key, 'period':key, 'deadline':key, 'priority':key}

output :
    list of tasks after processing with format [task_id, start_time, end_time]

'''

def calc_num_of_digit_after_period(num_as_string):
    # calculate split by . and return size of second part if no . in string return 0 otherwise return len of digits of second index 
    
    if len(num_as_string.split("."))==2:
        return len(num_as_string.split(".")[1])
    return 0

def apply_scale(num_as_string, scale):
    if len(num_as_string.split("."))==1:
        return int(num_as_string + '0' * scale)
    decimal, fractional = num_as_string.split(".")
    
    remain_scale = scale - len(fractional)
    
    return int(decimal+fractional+'0'*remain_scale)

def rescale(tasks, scale):
    tasks_after_rescaling = {}
    for task_id, durations in tasks.items():
        tasks_after_rescaling[task_id]=[]
        
        for start, end in durations:
            tasks_after_rescaling[task_id].append([start/(scale*1.0), end/(scale*1.0)])
            
    return tasks_after_rescaling

    
def RR(tasks, maximum_time, quantum_time_string):
    
    '''
    reformat input to queue of tasks with format : [
                                                    task_id,
                                                    release_time,
                                                    execution_time,
                                                    period, 
                                                    deadline,
                                                    start_time,
                                                    remain_to_execute,
                                                    current_to_execute,
                                                    priority
                                                ]
    '''
    
    if len(tasks) == 0:
        return []
    # find scaling factor by iterate over all tasks and quantum time to find maximum digit after . and multiply tasks and quantum by 10^max 
    max_digit_after_period = calc_num_of_digit_after_period(quantum_time_string)
    
    for task_id, task in tasks.items():
        max_digit_after_period = max(max_digit_after_period, calc_num_of_digit_after_period(task['release_time']))
        max_digit_after_period = max(max_digit_after_period, calc_num_of_digit_after_period(task['execution_time']))
        max_digit_after_period = max(max_digit_after_period, calc_num_of_digit_after_period(task['period']))
        max_digit_after_period = max(max_digit_after_period, calc_num_of_digit_after_period(task['deadline']))
            
    scale = 10**max_digit_after_period 
    
    quantum_time = apply_scale(quantum_time_string, max_digit_after_period)
    # print("\n================================")
    # print(scale)
    
    queue_of_tasks = []

    for task_id, task in tasks.items():
        queue_of_tasks.append({
            'task_id': task_id,
            'release_time': apply_scale(task['release_time'], max_digit_after_period),
            'execution_time': apply_scale(task['execution_time'], max_digit_after_period),
            'period': apply_scale(task['period'], max_digit_after_period),
            'deadline': apply_scale(task['deadline'], max_digit_after_period),
            'start_time': apply_scale(task['release_time'], max_digit_after_period),
            'remain_to_execute': apply_scale(task['execution_time'], max_digit_after_period)-min(quantum_time, apply_scale(task['execution_time'], max_digit_after_period)),
            'current_to_execute': min(quantum_time, apply_scale(task['execution_time'], max_digit_after_period)),
            'priority': int(task['priority'])
        })
        # print(scale)
        # print(queue_of_tasks[-1])

    current_time = 0


    # list of tasks after processing with format [task_id, start_time, end_time]
    tasks_after_processing = {}
    broken_times = [] # contain times
    time_broken = 0
    
    while current_time < maximum_time * scale:

        # pick first highest priority(low number of priority) task that start time <= current time
        index = -1
        highest_priority = 1e9

        for task in queue_of_tasks:
            if task['start_time'] <= current_time and task['priority'] < highest_priority:
                highest_priority = task['priority']
                index = queue_of_tasks.index(task)

        current_time += 1

        if index != -1:
            queue_of_tasks[index]['current_to_execute'] -= 1
            
            task_id = queue_of_tasks[index]['task_id']
            
            if tasks_after_processing.get(task_id) is None:
                tasks_after_processing[task_id] = []
                
                # access last element with key task_id
            if len(tasks_after_processing[task_id])!=0 and tasks_after_processing.get(task_id)[-1][-1] == current_time - 1:
                tasks_after_processing[task_id][-1][-1] = current_time
            else:
                tasks_after_processing[task_id].append([current_time - 1, current_time])
            
            
            if queue_of_tasks[index]['current_to_execute'] == 0:
                task = queue_of_tasks.pop(index)
                queue_of_tasks.append(task)

        if update_tasks(queue_of_tasks, current_time, quantum_time):
            broken_times.append(current_time)
            time_broken = current_time
            break

    tasks_after_rescaling = rescale(tasks_after_processing, scale)
    return tasks_after_rescaling, time_broken


tasks = {
    'Task 1': {
        'release_time': '0',
        'period': '6',
        'priority': '0',
        'execution_time': '2',
        'deadline': '6'
    },
    'Task 2': {
        'release_time': '1',
        'period': '8',
        'priority': '0',
        'execution_time': '2',
        'deadline': '8'
    },
    'Task 3': {
        'release_time': '2',
        'period': '15',
        'priority': '0',
        'execution_time': '4',
        'deadline': '15'
    }
}


## process tasks with round robin 
# from drawing import draw_tasks

# draw_tasks(*RR(tasks, 28, '0.25'))

# tasks_after_processing, broken = RR(tasks, 28, '0.25')

# print(tasks_after_processing)