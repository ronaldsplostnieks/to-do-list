import tkinter as tk
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
import os

class ToDoApp:
    list_menu = None

    def __init__(self, root):
        self.root = root
        self.root.title("To-do List Application")
        self.root.geometry("550x650")

        self.tasks = []
        self.finished_tasks = []
        self.current_list = "Default"

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
        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()
        self.finish_button = tk.Button(self.root, text="Finish Task", command=self.finish_task)
        self.finish_button.pack()
        self.edit_button = tk.Button(self.root, text="Edit Task", command=self.edit_task)
        self.edit_button.pack()
        self.view_button = tk.Button(self.root, text="View Tasks", command=self.view_tasks)
        self.view_button.pack()
        self.view_finished_button = tk.Button(self.root, text="View Finished Tasks", command=self.view_finished_tasks)
        self.view_finished_button.pack()
        
        self.new_list_button = tk.Button(self.root, text="New to-do list", command=self.new_list)
        self.new_list_button.pack()
        self.delete_list_button = tk.Button(self.root, text="Delete to-do list", command=self.delete_list)
        self.delete_list_button.pack()

        self.list_menu = tk.StringVar()
        self.list_menu.set("Default")
        self.list_options = []
        self.read_lists_from_file()
        # self.list_menu_option = tk.OptionMenu(self.root, self.list_menu, *(self.list_options), command = self.change_list)
        self.list_menu_option = tk.OptionMenu(self.root, self.list_menu, "Default", *self.list_options, command=self.change_list)
        self.list_menu_option.pack()

        self.load_tasks()

        
    def load_tasks(self):
        self.task_list.delete(0, tk.END)  # Clear the ListBox
        file_name = self.current_list + ".txt"
        try:
            self.tasks = self.read_from_file(file_name)
        except FileNotFoundError:
            with open(file_name, 'w') as f:
                pass
            self.tasks = []
        self.finished_tasks = self.read_from_file(self.current_list + "_finished.txt")
        self.view_tasks()

    def write_to_file(self, tasks, file_name):
        directory = "lists"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w') as f:
            for task in tasks:
                f.write(task+'\n')

    def read_from_file(self, file_name):
        directory = "lists"
        file_path = os.path.join(directory, file_name)
        tasks = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    tasks.append(line.strip())
        except FileNotFoundError:
            pass
        return tasks

    def add_task(self):
        task = self.task_entry.get()
        self.tasks.append(task)
        self.write_to_file(self.tasks, self.current_list + ".txt")
        self.task_entry.delete(0, tk.END)
        self.view_tasks()

    def view_tasks(self):
        self.task_list.delete(0, tk.END)
        for x, task in enumerate(self.tasks, 1):
            self.task_list.insert(tk.END, str(x) + ") " + task)

    def finish_task(self):
        finished = self.task_list.curselection()
        if finished:
            finished = finished[0]
            if finished > len(self.tasks):
                messagebox.showerror("Error", "Invalid index! There are not that many tasks!")
                return
            self.finished_tasks.append(self.tasks[finished])
            self.tasks.pop(finished)
            self.write_to_file(self.tasks, self.current_list + ".txt")
            self.write_to_file(self.finished_tasks, self.current_list + "_finished.txt")
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
            self.write_to_file(self.tasks, self.current_list + ".txt")
            self.view_tasks()
        else:
            messagebox.showerror("Error", "No task selected!")

        

    def view_finished_tasks(self):
        self.task_list.delete(0, tk.END)
        for x, task in enumerate(self.finished_tasks, 1):
            self.task_list.insert(tk.END, str(x) + ") " + task)

    def edit_task(self):
        edited = self.task_list.curselection()
        if edited:
            edited = edited[0]
            if edited > len(self.tasks):
                messagebox.showerror("Error", "Invalid index! There are not that many tasks!")
                return
            task = self.tasks[edited]
            new_task = simpledialog.askstring("Edit Task", "Enter the new task:", initialvalue=task)
            if new_task:
                self.tasks[edited] = new_task
                self.write_to_file(self.tasks, self.current_list + ".txt")
                self.view_tasks()
        else:
            messagebox.showerror("Error", "No task selected!")
            
    def new_list(self):
        new_list_name = simpledialog.askstring("New List", "Enter the name of the new list:")
        if new_list_name:
            self.list_options.append(new_list_name)
            self.list_menu.set(new_list_name)
            self.current_list = new_list_name
            self.tasks = []
            self.finished_tasks = []
            self.load_tasks()
            self.write_lists_to_file()
            self.update_list_options()

    def change_list(self, value):
        if value not in self.list_options:
            self.list_options.append(value)
        self.current_list = value
        self.tasks = self.read_from_file(self.current_list + ".txt")
        self.finished_tasks = self.read_from_file(self.current_list + "_finished.txt")
        self.view_tasks()
        self.update_list_options()
        print("Selected list:", self.current_list)

    def write_lists_to_file(self):
        directory = "lists"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, "lists.txt")
        with open(file_path, 'w') as f:
            for list_name in self.list_options:
                f.write(list_name + '\n')

    def read_lists_from_file(self):
        directory = "lists"
        file_path = os.path.join(directory, "lists.txt")
        try:
            with open(file_path, 'r') as f:
                self.list_options = [line.strip() for line in f]
        except FileNotFoundError:
            self.list_options = ["Default"]

    def update_list_options(self):
        self.list_menu_option.destroy()
        self.list_menu_option = tk.OptionMenu(self.root, self.list_menu, *(self.list_options), command=self.change_list)
        self.list_menu_option.pack()


    def delete_list(self):
        list_to_delete = self.list_menu.get()
        if list_to_delete in self.list_options:
            self.list_options.remove(list_to_delete)
            self.write_lists_to_file()
            if list_to_delete == self.current_list:
                self.current_list = "Default"
                self.tasks = []
                self.finished_tasks = []
                self.load_tasks()
            self.update_list_options()

            todo_file_path = os.path.join("lists", f"{list_to_delete}.txt")
            finished_file_path = os.path.join("lists", f"{list_to_delete}_finished.txt")
            if os.path.exists(todo_file_path):
                os.remove(todo_file_path)
            if os.path.exists(finished_file_path):
                os.remove(finished_file_path)
            self.list_menu.set("Default")


root = tk.Tk()
app = ToDoApp(root)
root.mainloop()      