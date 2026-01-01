import json
from datetime import datetime
import uuid
import os

# GLOBAL DICTIONARIES 
All_task = {}
Incom_task = {}
Comp_task = {}

file="tasks.json"

#TASK CLASS
class Task:
    def __init__(self, task, tags=None, due_date="NA"):
        self.task = task
        self.id = str(uuid.uuid1())
        self.created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_time = "NA"
        self.completed = False
        self.completed_time = "NA"
        self.tags = tags if tags else []
        self.due_date = due_date

    def update_task(self, new_task, new_tags, new_due_date):
        All_task[new_task] = All_task.pop(self.task)
        Incom_task[new_task] = Incom_task.pop(self.task)

        self.task = new_task
        self.tags = new_tags
        self.due_date = new_due_date
        self.updated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def complete_task(self):
        self.completed = True
        self.completed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Comp_task[self.task] = self
        Incom_task.pop(self.task)

    def to_dict(self):
        return {
            "task": self.task,
            "id": self.id,
            "created_time": self.created_time,
            "updated_time": self.updated_time,
            "completed": self.completed,
            "completed_time": self.completed_time,
            "tags": self.tags,
            "due_date": self.due_date
        }

    @classmethod
    def from_dict(cls, data):
        t = cls(
            data["task"],
            data.get("tags", []),
            data.get("due_date", "NA")
        )
        t.id = data["id"]
        t.created_time = data["created_time"]
        t.updated_time = data["updated_time"]
        t.completed = data["completed"]
        t.completed_time = data["completed_time"]
        return t

    def __repr__(self):
        return (
            f"ID - {self.id}\n"
            f"Task - {self.task}\n"
            f"Tags - {', '.join(self.tags) if self.tags else 'NA'}\n"
            f"Due Date - {self.due_date}\n"
            f"Created Time - {self.created_time}\n"
            f"Updated Time - {self.updated_time}\n"
            f"Completed - {self.completed}\n"
            f"Completed Time - {self.completed_time}\n"
        )

#  FILE FUNCTIONS 
def save_tasks():
    data = {
        "All_task": {k: v.to_dict() for k, v in All_task.items()},
        "Incom_task": {k: v.to_dict() for k, v in Incom_task.items()},
        "Comp_task": {k: v.to_dict() for k, v in Comp_task.items()}
    }
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def load_tasks():
    global All_task, Incom_task, Comp_task

    if not os.path.exists(file):
        return

    try:
        with open(file, "r") as f:
            content = f.read().strip()
            if not content:
                return
            data = json.loads(content)

        All_task = {k: Task.from_dict(v) for k, v in data.get("All_task", {}).items()}
        Incom_task = {k: Task.from_dict(v) for k, v in data.get("Incom_task", {}).items()}
        Comp_task = {k: Task.from_dict(v) for k, v in data.get("Comp_task", {}).items()}

    except json.JSONDecodeError:
        print("Corrupted file detected. Resetting tasks.")
        save_tasks()

# LOAD DATA
load_tasks()

# MAIN LOOP


while True:
    print("\n1. Add a new task")
    print("2. Show all tasks")
    print("3. Show incomplete tasks")
    print("4. Show completed tasks")
    print("5. Update task")
    print("6. Mark task completed")
    print("7. Exit")

    try:
        op = int(input("Enter option: "))
    except ValueError:
        print("Invalid input!")
        continue

    if op == 1:
        name = input("Enter task name: ")
        tags = input("Enter tags (comma separated): ").split(",")
        tags = [t.strip() for t in tags if t.strip()]
        due = input("Enter due date (YYYY-MM-DD or NA): ")

        task = Task(name, tags, due)
        All_task[name] = task
        Incom_task[name] = task
        save_tasks()
        print("Task added successfully!")

    elif op == 2:
        if not All_task:
            print("No tasks found.")
        for v in All_task.values():
            print(v)

    elif op == 3:
        if not Incom_task:
            print("No incomplete tasks.")
        for v in Incom_task.values():
            print(v)

    elif op == 4:
        if not Comp_task:
            print("No completed tasks.")
        for v in Comp_task.values():
            print(v)

    elif op == 5:
        if not Incom_task:
            print("No tasks to update.")
            continue

        for i, v in enumerate(Incom_task.values(), 1):
            print(f"Task no - {i}")
            print(v)

        n = int(input("Enter task number: "))
        key = list(Incom_task.keys())[n - 1]

        new_name = input("Enter new task name: ")
        new_tags = input("Enter new tags (comma separated): ").split(",")
        new_tags = [t.strip() for t in new_tags if t.strip()]
        new_due = input("Enter new due date (YYYY-MM-DD or NA): ")

        Incom_task[key].update_task(new_name, new_tags, new_due)
        save_tasks()
        print("Task updated successfully!")

    elif op == 6:
        if not Incom_task:
            print("No tasks to complete.")
            continue

        for i, v in enumerate(Incom_task.values(), 1):
            print(f"Task no - {i}")
            print(v)

        n = int(input("Enter task number: "))
        key = list(Incom_task.keys())[n - 1]
        Incom_task[key].complete_task()
        save_tasks()
        print("Task completed successfully!")

    elif op == 7:
        save_tasks()
        print("Exiting... Data saved.")
        break

    else:
        print("Invalid option!")
