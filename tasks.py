class Task:
    def __init__(self, desc, num):
        self.num = num
        self.desc = desc
        self.completed = False
        self.priority = None
        self.project = None

    def __str__(self):
        string = f'''
Task # {self.num}
-----------
Description: {self.desc}
Completed: {self.completed}'''

        if self.priority is not None:
            string += f'\nPriority: {self.priority}'
        if self.project is not None:
            string += f'\nProject: {self.project}'
        return string

    def __repr__(self):
        dict_repr = {'desc': self.desc, 'completed': self.completed, 'priority': self.priority, 'project': self.project}
        return str(dict_repr)

    def __lt__(self, other):
        if self.priority is None and other.priority is not None:
            return False
        elif self.priority is not None and other.priority is None:
            return True
        elif self.priority == other.priority:
            return self.num < other.num
        else:
            return self.priority < other.priority


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
                single_task = Task(task[1], int(task[0]))
                single_task.completed = task[2] == 'True'
                priority = task[3]
                if priority == 'None':
                    single_task.priority = None
                else:
                    single_task.priority = int(priority)
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
                    priority = int(command[index_of_priority])
                    if priority < 1 or priority > 4:
                        raise InvalidCommandError("Priority must be number from 1 to 4")
                    while len(description) == 0:
                        description = input('Please enter a description for the new task to add > ')
                    if " #" in command:
                        index_of_project = command.index(" #") + 2
                        project = command[index_of_project:]
                elif " #" in command:
                    index_of_project = command.index(" #") + 2
                    project = command[index_of_project:]
                    description = command[4:index_of_project - 2]
                    while len(description) == 0:
                        description = input('Please enter a description for the new task to add > ')
                task = Task(description, new_id)
                task.priority = priority
                task.project = project
                task_dict[new_id] = task
                print(f'New task added with task # {new_id}')
            elif command[:4] == 'upd ':
                project = None
                priority = None
                index_of_task = command.index(" ") + 1
                end_index = command.find(" ", index_of_task)
                task_num = command[index_of_task:end_index]
                if end_index == -1 or end_index + 1 == len(command):
                    task_num = int(command[index_of_task:].strip())
                    if task_num in task_dict:
                        description = input(f'Enter the updated description for task # {task_num} > ')
                elif " !" in command:
                    index_of_priority = command.index(" !") + 2
                    description = command[end_index+1:index_of_priority-2]
                    priority = int(command[index_of_priority])
                    if priority < 1 or priority > 4:
                        raise InvalidCommandError("Priority must be number from 1 to 4")
                    if " #" in command:
                        index_of_project = command.index(" #") + 2
                        project = command[index_of_project:]
                elif " #" in command:
                    index_of_project = command.index(" #") + 2
                    project = command[index_of_project:]
                    description = command[end_index+1:index_of_project - 2]
                task_num = int(task_num)
                if task_num not in task_dict:
                    raise TaskNotFoundError(f'Task # {task_num} does not exist')
                if len(description) > 0:
                    task_dict[task_num].desc = description
                if project is not None:
                    task_dict[task_num].project = project
                if priority is not None:
                    task_dict[task_num].priority = priority
                print(f'Updated task # {task_num}')
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
                    print(task_dict[key])
                if len(task_dict) == 0:
                    print('Nothing to show here!')

            elif command == 'list todo':
                values = False
                for val in sorted(task_dict.values()):
                    if not val.completed:
                        print(val)
                        values = True
                if not values:
                    print('Nothing to show here!')
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
                task_dict[task_num].completed = True
                print(f'Task # {task_num} marked as complete.')
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
Make sure that the required components of the command are present and in valid format.
Also ensure that no manual changes are made to the file.''')
