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

def RR(tasks, maximum_time, quantum_time):
    
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

    queue_of_tasks = []

    for task_id, task in tasks.items():
        queue_of_tasks.append({
            'task_id': task_id,
            'release_time': task['release_time'],
            'execution_time': task['execution_time'],
            'period': task['period'],
            'deadline': task['deadline'],
            'start_time': task['release_time'],
            'remain_to_execute': task['execution_time']-min(quantum_time, task['execution_time']),
            'current_to_execute': min(quantum_time, task['execution_time']),
            'priority': task['priority']
        })

    current_time = 0


    # list of tasks after processing with format [task_id, start_time, end_time]
    tasks_after_processing = {}
    broken_times = [] # contain times
    time_broken = 0
    
    while current_time < maximum_time:

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
            # if len(tasks_after_processing[task_id])!=0 and tasks_after_processing.get(task_id)[-1][-1] == current_time - 1:
            #     tasks_after_processing[task_id][-1][-1] = current_time
            # else:
            tasks_after_processing[task_id].append([current_time - 1, current_time])
            
            
            if queue_of_tasks[index]['current_to_execute'] == 0:
                task = queue_of_tasks.pop(index)
                queue_of_tasks.append(task)

        if update_tasks(queue_of_tasks, current_time, quantum_time):
            broken_times.append(current_time)
            time_broken = current_time
            break

    return tasks_after_processing, time_broken


# tasks = {
#     'Task 1': {
#         'release_time': 0,
#         'period': 6,
#         'priority': 1,
#         'execution_time': 2,
#         'deadline': 6
#     },
#     'Task 2': {
#         'release_time': 1,
#         'period': 8,
#         'priority': 0,
#         'execution_time': 2,
#         'deadline': 8
#     },
#     'Task 3': {
#         'release_time': 2,
#         'period': 15,
#         'priority': 2,
#         'execution_time': 4,
#         'deadline': 15
#     }
# }


## process tasks with round robin 
# from drawing import draw_tasks

# draw_tasks(*RR(tasks, 20, 2))
