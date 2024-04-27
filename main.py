import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-do List Application")
        self.root.geometry("550x550")

        self.tasks = []
        self.finished_tasks = []

        self.task_label = tk.Label(self.root, text="Task:", font=('Times New Roman', 15, 'bold'))
        self.task_label.pack()
        self.task_entry = tk.Entry(self.root, font=("Times New Roman",12),justify="center", width=40)
        self.task_entry.pack()

        self.task_list_frame = tk.Frame(self.root)
        self.task_list_frame.pack()
        self.task_list = tk.Listbox(self.task_list_frame, width=60, height=20)
        self.task_list.pack(side=tk.LEFT)
        self.scrollbar = tk.Scrollbar(self.task_list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_list.yview)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_button.pack()
        self.view_button = tk.Button(self.root, text="View Tasks", command=self.view_tasks)
        self.view_button.pack()
        self.finish_button = tk.Button(self.root, text="Finish Task", command=self.finish_task)
        self.finish_button.pack()
        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()
        self.view_finished_button = tk.Button(self.root, text="View Finished Tasks", command=self.view_finished_tasks)
        self.view_finished_button.pack()
        self.edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        self.edit_button.pack()

        self.load_tasks()
        

    def load_tasks(self):
        self.tasks = self.read_from_file("todo.txt")
        self.finished_tasks = self.read_from_file("finished.txt")
        self.view_tasks()

    def write_to_file(self, tasks, file_name):
        with open(file_name, 'w') as f:
            for task in tasks:
                f.write(task+'\n')

    def read_from_file(self, file_name):
        tasks = []
        with open(file_name, 'r') as f:
            for line in f:
                tasks.append(line.strip())
        return tasks

    def add_task(self):
        task = self.task_entry.get()
        self.tasks.append(task)
        self.write_to_file(self.tasks, "todo.txt")
        self.task_entry.delete(0, tk.END)
        self.view_tasks()        


    def view_tasks(self):
        self.task_list.delete(0, tk.END)
        for x, task in enumerate(self.tasks, 1):
            self.task_list.insert(tk.END, str(x) + ") " + task)

        self.view_button.config(state='normal')
        self.view_finished_button.config(state='normal')
        self.add_button.config(state='normal')
        self.finish_button.config(state='normal')
        self.delete_button.config(state='normal')
        self.edit_button.config(state='normal')

    def finish_task(self):
        finished = self.task_list.curselection()
        if finished:
            finished = finished[0]
            if finished > len(self.tasks):
                messagebox.showerror("Error", "Invalid index! There are not that many tasks!")
                return
            self.finished_tasks.append(self.tasks[finished])
            self.tasks.pop(finished)
            self.write_to_file(self.tasks, "todo.txt")
            self.write_to_file(self.finished_tasks, "finished.txt")
            self.view_tasks()
        else:
            messagebox.showerror("Error", "No task selected!")

    def delete_task(self):
        deleted = self.task_list.curselection()
        if deleted:
            deleted = deleted[0]
            if deleted > len(self.tasks):
                messagebox.showerror("Error", "Invalid index! There are not that many tasks!")
                return
            self.tasks.pop(deleted)
            self.write_to_file(self.tasks, "todo.txt")
            self.view_tasks()
        else:
            messagebox.showerror("Error", "No task selected!")

    def edit_task(self):
        selected = self.task_list.curselection()
        if selected:
            selected = selected[0]
            if selected > len(self.tasks):
                messagebox.showerror("Error", "Invalid index! There are not that many tasks!")
                return
            task_to_edit = self.tasks[selected]
            new_task = simpledialog.askstring("Edit Task", "Enter the new task:", initialvalue=task_to_edit)
            if new_task:
                self.tasks[selected] = new_task
                self.write_to_file(self.tasks, "todo.txt")
                self.view_tasks()
        else:
            messagebox.showerror("Error", "No task selected!")

    def view_finished_tasks(self):
        self.task_list.delete(0, tk.END)
        for task in self.finished_tasks:
            self.task_list.insert(tk.END, task)
        self.view_button.config(state='normal')
        self.view_finished_button.config(state='disabled')
        self.add_button.config(state='disabled')
        self.finish_button.config(state='disabled')
        self.delete_button.config(state='disabled')

root = tk.Tk()
app = ToDoApp(root)
root.mainloop()

# https://www.youtube.com/watch?v=Miydkti_QVE&ab_channel=TurbineThree

