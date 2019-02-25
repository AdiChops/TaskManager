class Task:
    def __init__(self, desc):
        self.desc = desc
        self.completed = False
        self.priority = None
        self.project = None


class TaskNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidCommandError(Exception):
    def __init__(self, message):
        self.message = message


while True:
    command = input('''
Hello. Please enter a command. These are the commands you can write:
    add: to add a task
    upd x: to update task number x
    rem x: to remove task number x
    done x: to mark task number x as completed
    list all: to list all tasks
    list todo: to list all tasks that are not completed
    purge: to remove all completed tasks
Enter q to quit.
''')
    task_dict = {}
    try:
        if command == 'q':
            print('Thank you for using the task service')
            quit()
        with open("tasks.txt", "a+t") as file:
            file.seek(0)
            tasks = file.readlines()
            for line in tasks:
                task = line.split('~')
                single_task = Task(task[1])
                single_task.completed = task[2] == 'True'
                priority = task[3]
                if priority == 'None':
                    single_task.priority = None
                else:
                    single_task.priority = priority
                project = task[4].strip()
                if project == 'None':
                    single_task.project = None
                else:
                    single_task.project = project
                task_dict[int(task[0])] = single_task
            if command[:4] == 'add ' or command == 'add':
                if len(task_dict) > 0:
                    new_id = int(sorted(task_dict.keys())[-1]) + 1
                else:
                    new_id = 1
                project = None
                priority = None
                if len(command) == 4 or len(command) == 3:
                    description = input('Please enter a description for the new task to add > ')
                elif " !" in command:
                    index_of_priority = command.index(" !") + 2
                    description = command[4:index_of_priority-2]
                    while len(description) == 0:
                        description = input('Please enter a description for the new task to add > ')
                    priority = command[index_of_priority]
                    if " #" in command:
                        index_of_project = command.index(" #") + 2
                        project = command[index_of_project:]
                elif " #" in command:
                    index_of_project = command.index(" #") + 2
                    project = command[index_of_project:]
                    description = command[4:index_of_project - 2]
                    while len(description) == 0:
                        description = input('Please enter a description for the new task to add > ')
                task = Task(description)
                task.priority = priority
                task.project = project
                task_dict[new_id] = task
            elif command[:4] == 'upd ':
                project = None
                priority = None
                index_of_task = command.index(" ") + 1
                end_index = command.find(" ", index_of_task)
                task_num = int(command[index_of_task:end_index])
                if end_index == -1 or end_index + 1 == len(command):
                    task_num = int(command[index_of_task:].strip())
                    description = input(f'Enter the updated description for task # {task_num} > ')
                elif " !" in command:
                    index_of_priority = command.index(" !") + 2
                    description = command[end_index:index_of_priority-2]
                    priority = command[index_of_priority]
                    if " #" in command:
                        index_of_project = command.index(" #") + 2
                        project = command[index_of_project:]
                elif " #" in command:
                    index_of_project = command.index(" #") + 2
                    project = command[index_of_project:]
                    description = command[end_index+2:index_of_project - 2]
                task = task_dict[task_num]
                if len(description) > 0:
                    task.desc = description
            elif command[:4] == 'rem ':
                index_of_task = command.find(" ") + 1
                task_num = int(command[index_of_task:])
                if task_num not in task_dict:
                    raise TaskNotFoundError(f"Task number {task_num} does not exist.")
                confirm = input(f'Are you sure you would like to delete task # {task_num} (y/n)? ')
                if confirm == 'y':
                    del task_dict[task_num]
                    print(f'Task # {task_num} deleted')
            elif command == 'list all':
                for key in sorted(task_dict):
                    task = task_dict[key]
                    print(f'''
Task # {key}
-----------
Description: {task.desc}
Completed: {task.completed}''')
                    if task.priority is not None:
                        print(f'Priority: {task.priority}')
                    if task.project is not None:
                        print(f'Project: {task.project}')

            elif command == 'list todo':
                task_dict = sorted(task_dict.values(), key=lambda t: (t.priority, t))
            elif command == 'purge':
                to_del = [k for k in task_dict if task_dict[k].completed]
                for i in to_del:
                    del task_dict[i]
                if len(to_del) == 1:
                    print(f'{len(to_del)} task deleted.')
                else:
                    print(f'{len(to_del)} tasks deleted')
            elif command[:5] == 'done ':
                index_of_task = command.index(" ") + 1
                task_num = int(command[index_of_task:])
                if task_num not in task_dict:
                    raise TaskNotFoundError(f"Task number {task_num} does not exist.")
                task = task_dict[task_num]
                task['completed'] = True
                task_dict[task_num] = task
            else:
                raise InvalidCommandError(f'{command} is not a valid command. Make sure required components are present.')
            file.truncate(0)
            for i in task_dict:
                task = task_dict[i]
                file.write(f'{i}~{task.desc}~{task.completed}~{task.priority}~{task.project}\n')
            file.close()

    except TaskNotFoundError as e:
        print(e.message)
    except InvalidCommandError as e:
        print(e.message)
    except ValueError as e:
        print('''An unexpected value was encountered.
Make sure that the required components of the command are present and in valid format.''')
