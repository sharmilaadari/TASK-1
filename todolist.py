import json
from datetime import datetime

class Task:
    def __init__(self, description, priority="low", due_date=None):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False

    def mark_as_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(data['description'], data['priority'], data['due_date'])
        task.completed = data['completed']
        return task

class ToDoList:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_task_as_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_as_completed()
            self.save_tasks()

    def list_tasks(self):
        for idx, task in enumerate(self.tasks):
            status = "Done" if task.completed else "Pending"
            due_date = task.due_date if task.due_date else "No due date"
            print(f"{idx}. {task.description} [Priority: {task.priority}, Due: {due_date}, Status: {status}]")

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            tasks_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_dict, f)

    def load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                tasks_dict = json.load(f)
                return [Task.from_dict(task) for task in tasks_dict]
        except FileNotFoundError:
            return []

def main():
    todo_list = ToDoList()

    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Mark Task as Completed")
        print("4. List Tasks")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            description = input("Task description: ")
            priority = input("Task priority (low/medium/high): ")
            due_date = input("Due date (YYYY-MM-DD) or leave blank: ")
            due_date = due_date if due_date else None
            task = Task(description, priority, due_date)
            todo_list.add_task(task)
        elif choice == '2':
            index = int(input("Task index to remove: "))
            todo_list.remove_task(index)
        elif choice == '3':
            index = int(input("Task index to mark as completed: "))
            todo_list.mark_task_as_completed(index)
        elif choice == '4':
            todo_list.list_tasks()
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
