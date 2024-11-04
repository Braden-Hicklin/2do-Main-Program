from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
import DB
from PIL import ImageTk, Image

class App ():
    def __init__(self):
        # Keys for MySQL server connection
        self.db = None
        self.pw = None
        self.connection = None
        self.create_database_test = None

        # Initialize the root window
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.geometry('1471x800')
        
        # Modify Background
        self.bg = ImageTk.PhotoImage(Image.open("bg_main.png"))
        self.bg_label = Label(self.root, image=self.bg)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Modify global font
        self.default_font = tkFont.nametofont("TkDefaultFont")
        self.default_font.configure(family="Courier")
        self.default_font.configure(size=12)
        self.root.option_add("*Font", self.default_font)

        # Initialize Notebook and taskPage tab
        self.nb = ttk.Notebook(self.root)
        self.tree_bg = ImageTk.PhotoImage(Image.open("default_task_page.png"))
        self.taskPage = ttk.Frame(self.nb)
        self.nb.pack(pady=100)

        # Initialize basics for task list page
        self.nb.add(self.taskPage, text="Task Page")
        self.title = Label(self.taskPage, text='Task List')
        self.scrollbar = Scrollbar(self.taskPage)
        self.tasksTree = ttk.Treeview(self.taskPage, 
                                      columns=("description", "priority"), 
                                      height=20,
                                      yscrollcommand=self.scrollbar.set)
        
        self.addTaskButton = Button(self.taskPage, 
                                    text='Add Task', 
                                    width=25, 
                                    command=lambda: self.init_task())

        self.tasksTree.heading('#0', text='Task Name')
        self.tasksTree.column("#0", minwidth=0, width=300)
        self.tasksTree.heading('description', text='Description')
        self.tasksTree.column("description", minwidth=0, width=300)
        self.tasksTree.heading('priority', text='Priority Level')
        self.tasksTree.column("priority", minwidth=0, width=300)

        self.title.grid(row=1, column=0, pady=2, sticky= NSEW)
        self.tasksTree.grid(row=2, column=0, sticky= NSEW)
        self.addTaskButton.grid(row=3, column=0, pady=2, sticky=W)

        # Initialize common variables
        self.tl = None
        self.curItem = None
        self.canvas = None

    # Initialize a connection with the database
    def establish_connection(self):
        self.connection = DB.create_server_connection("localhost", "root", self.pw)
        self.create_database_test = f"CREATE DATABASE {self.db}"
        DB.create_database(self.connection, self.create_database_test)
        self.connection = DB.create_db_connection("localhost", "root", self.pw, self.db)
        DB.execute_query(self.connection, DB.create_task_table)
        DB.execute_query(self.connection, DB.create_todo_table)

    # Create popups
    def open_popup(self, size):
        self.tl = Toplevel()
        self.tl.geometry(size)
        self.tl.focus_force()
        self.tl.grab_set_global()

    # Close popups created by open_popup
    def close_popup(self):
        self.tl.destroy()
        self.tl = None
    
    # Initialize the Help Page
    def help_page(self):
        self.tl = Toplevel()
        self.tl.geometry('1420x480')
        self.tl.focus_force()
        self.tl.grab_set_global()
        Label(self.tl, text="Help Page").grid(column=0, row=0, columnspan=2, sticky=N)
        Label(self.tl, text="- The task list allows you to create a new task by pressing the add task button in the bottom left corner.").grid(column=0, row=1, sticky=W)
        Label(self.tl, text="- You can create a To-Do by selecting a Task in the Task List and clicking the add To-Do button that appears in the list to the right.").grid(column=0, row=2, sticky=W)
        Label(self.tl, text="- While optional, To-Do's can be added to any Task, these can help organize a Task further by subdividing it into smaller parts.").grid(column=0, row=3, sticky=W)
        Label(self.tl, text="- Tasks and To-Do's can be deleted by selecting the delete button in the inspection window to the right of the task list.").grid(column=0, row=4, sticky=W)
        Label(self.tl, text="- Tasks can be edited by selecting the edit button in the inspection window to the right of the task list.").grid(column=0, row=5, sticky=W)
        Label(self.tl, text="- Tasks and To-Do's are saved between sessions, so don't worry about closing the program if need be.").grid(column=0, row=6, sticky=W)
        Label(self.tl, text="- Within the Add Task Page, the description and priority fields are both optional, only the Task Name is required to create a Task.").grid(column=0, row=7, sticky=W)
        Label(self.tl, text="- A To-Do name is required to create a To-Do.").grid(column=0, row=8, sticky=W)
        Label(self.tl, text="- To-Do's cannot be editted after creation, but they can be deleted.").grid(column=0, row=9, sticky=W)

        Button(self.tl, text="Back", command=lambda: self.close_popup()).grid(column=0, row=10, columnspan=2)
        
    # Used to dynamically layout certain objects
    def layout_grid(self, columnStart, rowStart, elemperCol, labels, components, pady=None, padx=None):
        if len(components) != len(labels):
            print("Error initializing components, label component mismatch.")
        i = 0
        colMod = 0
        rowMod = 0

        while i < len(components):
            if i % elemperCol == 0:
                rowMod = rowStart
                colMod += 2
            labels[i].grid(column=columnStart+colMod, row=rowStart+rowMod, sticky=E, pady=pady)
            components[i].grid(column=columnStart+1+colMod, row=rowStart+rowMod, sticky=W, pady=pady, padx=padx)
            rowMod += 1
            i += 1

    # Confirmation popup box
    def confirm_popup(self, funct, text, size, confirmtxt='Yes', denytxt='No'):
        if self.tl is None:
            self.open_popup(size)
            text = Label(self.tl, text=text)
            confirm = Button(self.tl, text=confirmtxt, command=funct)
            deny = Button(self.tl, text=denytxt, command=lambda: self.close_popup())
            text.grid(column=0,row=0, columnspan=2)
            confirm.grid(column=0,row=1)
            deny.grid(column=1,row=1)

    # Navigate to the tasks list page
    def task_page(self):
        self.nb.select(tab_id=self.taskPage)
        Button(self.taskPage, text="Help", command=lambda: self.help_page()).grid(column=1, columnspan=10, row=0, sticky=NW)
        if len(self.tasksTree.get_children()) <= 0:
            self.tasksTree.insert('', iid='bg', index=END, image=self.tree_bg)
        else:
            try:
                self.tasksTree.delete('bg')
            except:
                pass

    # Populate the tasksTree widget upon entry
    def populate_on_entry(self):
        li = DB.get_all_tasks(self.connection)
        for task in li:
            self.tasksTree.insert('', index=END, iid=task[0], text=task[1], values=task[2:])
            for todo in DB.get_todo(self.connection, task[0]):
                self.tasksTree.insert(str(task[0]), index=END, text=todo[0], values=[todo[1]])
    
    # Ensure the name field is filled before adding a task
    def validate_add_task(self, name, description, priority, addpage):
        confunct = lambda: self.add_tasks(name, description, priority, addpage)
        if name.get() == '':
            self.open_popup('700x200')
            text = Label(self.tl, text=f"ERROR: Task Name is required to create a task\nplease enter a task name in the Task Name entry field")
            back = Button(self.tl, text="Back", command=lambda: self.close_popup())

            text.grid(column=0,row=0, columnspan=2)
            back.grid(column=1,row=1)
        else:
            self.confirm_popup(confunct, 
                               f"Are you sure you want to add {name.get()} to the task list?\n*You can edit and delete tasks from within the task list page*",
                               '700x200')

    # Initialize a task, confirmation still required
    def init_task(self):
        addPage = ttk.Frame(self.nb)

        Button(addPage, text="Help", command=lambda: self.help_page()).grid(column=6, columnspan=10, row=0, sticky=NE)
        self.nb.hide(self.taskPage)
        self.nb.add(addPage, text="Add Task")
        self.nb.select(tab_id=addPage)
        n = StringVar()

        title = Label(addPage, text="Create Task")
        nameLabel = Label(addPage, text="*Task Name: ")
        descLabel = Label(addPage, text="Description: ")
        prioLabel = Label(addPage, text="Priority Level: ")
        reqLabel = Label(addPage, text="* Required Fields")
        
        
        name = Entry(addPage, width=50)
        description = Text(addPage, height=10, width=50)
        priority = ttk.Combobox(addPage, textvariable=n, values=['Low', 'Medium', 'High'])
        
        labList = [nameLabel, descLabel, prioLabel]
        compList = [name, description, priority]

        cancelfunct = lambda: self.exit_task_page(addPage)

        save = Button(
            addPage, text='Save', 
            width=25, 
            command=lambda: self.validate_add_task(name, description, priority, addPage))
        cancel = Button(addPage, text="Cancel",
                        width=25,
                        command=lambda: self.confirm_popup(cancelfunct, 
                                                           "Are you sure you want to cancel task creation?\ncanceling will clear all fields", 
                                                           '700x200'))
        
        self.layout_grid(0,1,2,labList,compList, pady=20, padx=20)
        title.grid(column=0, row=0, columnspan=4)
        reqLabel.grid(column=5, row=3, sticky=S)
        save.grid(column=0, columnspan=4, row=5)
        cancel.grid(column=5, columnspan=4, row=5)
        
    # Finalize the addition of a task to the task list
    def add_tasks(self, name, desc, priority, frame):
        task = name.get()
        description = '' if desc.get("1.0", "end-1c") == '' else desc.get("1.0", "end-1c")
        priority = '' if priority.get() == '' else priority.get()
        id = DB.insert_task(self.connection, task, description, priority)
        self.tasksTree.insert('', index=END, iid=id, text = task, values=[description, priority])
        self.nb.forget(frame)
        self.close_popup()
        self.task_page()

    # Leave the task page and remove it from the notebooks ledger
    def exit_task_page(self, frame):
        self.nb.forget(frame)
        self.close_popup()
        self.task_page()

    # Ensure that the name field is filled in when updating a task
    def validate_update_task(self, name, description, priority, popup):
        if name.get() == '':
            self.open_popup('700x200')
            text = Label(self.tl, text=f"ERROR: Task Name is required to create a task\nplease enter a task name in the Task Name entry field")
            back = Button(self.tl, text="Back", command=lambda: self.close_popup())

            text.grid(column=0,row=0, columnspan=2)
            back.grid(column=1,row=1)
        else:
            confunct = lambda: self.update_task(name, description, priority, popup)
            self.confirm_popup(confunct, 
                           f"Are you sure you want to update {name.get()}?",
                           '700x200')

    # Finalize updating a task
    def update_task(self, name, description, priority, frame):
        task = name.get()
        description = description.get("1.0", "end-1c")
        priority = priority.get()
        self.tasksTree.item(self.curItem, 
                            text=task, 
                            values=[description, priority])
        DB.update_task(self.connection, self.curItem,task, description, priority)
        
        frame.destroy()
        self.close_popup()
        self.inspect_item(event=None)

    # Show edit task popup
    def edit_task(self):
        popup = Tk()
        popup.geometry('1420x580')
        popup.option_add("*Font", self.default_font)
        popup.resizable(False, False)

        n = StringVar()
        items = self.tasksTree.item(self.curItem)

        Label(popup, text=f"Edit {items['text']}").grid(column=0, row=0, columnspan=10)

        nameLabel = Label(popup, text="Task Name: ")
        descLabel = Label(popup, text="Description: ")
        prioLabel = Label(popup, text="Priority Level: ")

        nameLabel.grid(column=0, row=1, sticky=E)
        descLabel.grid(column=0, row=2, sticky=NE, pady=20)
        prioLabel.grid(column=2, row=2, sticky=NE, pady=20)

        # Initialize entry boxes and fill them with existing content
        name = Entry(popup, width=50)
        name.insert(index=END, string=str(items['text']))
        name.grid(column=1,row=1)

        description = Text(popup, height=10, width=50)
        description.insert(END, chars=items['values'][0])
        description.grid(column=1, row=2, sticky=W, ipady=100, pady=20)

        priority = ttk.Combobox(popup, textvariable=n, values=['Low', 'Medium', 'High'])
        priority.insert(index=END, string=str(items["values"][1]))
        priority.grid(column=3, row=2, sticky=NW, pady=20, columnspan=5)   
    
        save = Button(popup, 
                      text='Save', 
                      width=25, 
                      command=lambda: self.validate_update_task(name, description, priority, popup))
        
        cancel = Button(popup, 
                      text='cancel', 
                      width=25, 
                      command=lambda: popup.destroy())
        
        save.grid(column=0, row=5)
        cancel.grid(column=4, row=5)

    # Finalize deletion of task
    def delete_task(self):
        DB.delete_task(self.connection, self.curItem)
        self.tasksTree.delete(self.curItem)
        self.close_popup()
        self.curItem = None
        # Recheck for blank list
        self.task_page()
        
    # Finalize deletion of todo
    def delete_todo(self):
        id = self.tasksTree.item(self.curItem)['text']
        DB.delete_todo(self.connection, id)
        self.tasksTree.delete(self.curItem)
        self.close_popup()
        self.curItem = None

    # Ensure the todo has a name before it is added
    def validate_add_todo(self, name, popup):
        if name.get() == '':
            self.open_popup('700x200')
            text = Label(self.tl, text=f"ERROR: To-Do Name is required to create a To-Do\nplease enter a To-Do name in the To-Do Name entry field")
            back = Button(self.tl, text="Back", command=lambda: self.close_popup())

            text.grid(column=0,row=0, columnspan=2)
            back.grid(column=1,row=1)
        else:
            confunct = lambda: self.add_todo(name, popup)
            self.confirm_popup(confunct, 
                           f"Are you sure you want to add {name.get()} to the task?\n*Todo's can only be deleted, they cannot be edited after creation",
                           '700x200')

    # Cancel the todo creation
    def cancel_todo(self, frame):
        frame.destroy()
        self.close_popup()

    # Initialize todo, confirmation still required
    def init_todo(self):
        popup = Tk()
        popup.geometry('700x200')
        popup.option_add("*Font", self.default_font)
        Label(popup, text="Create To-Do").grid(column=0, row=0, columnspan=3)
        cancelfunct = lambda: self.cancel_todo(popup)
        name = Entry(popup, width=25)
        Label(popup, text="*To-Do Name: ").grid(column=0, row=1, sticky=E)
        name.grid(column=1, row=1)       
        save = Button(popup, 
                      text='Save', 
                      width=25, 
                      command=lambda: self.validate_add_todo(name, popup))
        
        cancel = Button(popup, 
                      text='Cancel', 
                      width=25, 
                      command=lambda: self.confirm_popup(cancelfunct, 
                           f"Are you sure you want to cancel To-Do creation?\n*All fields will be cleared if yes is selected",
                           '700x200'))
        save.grid(column=0, row=3)
        cancel.grid(column=1,row=3)
        Label(popup, text="*Required fields").grid(column=0,columnspan=3, row=2)


    # Finalize addition to todo list
    def add_todo(self, name, frame):
        todo = name.get()
        id = DB.insert_todo(self.connection, todo, self.curItem)
        self.tasksTree.insert(self.curItem, index=END, text=id, values=[todo])
        frame.destroy()
        self.close_popup()

    # Inspect current selected item in tasksTree
    def inspect_item(self, event):
        if self.canvas != None:
            self.canvas.destroy()
        self.canvas = Canvas(self.taskPage, width=200, height=70)
        
        self.canvas.grid(row=2, column=2, sticky= N)
        self.curItem = self.tasksTree.focus()
        if event and self.curItem != '':
            items = self.tasksTree.item(self.curItem)

            li = Listbox(self.canvas, width=24)
            li.insert(1, items['text'])
            for i in range(len(items['values'])):
                li.insert(2, items['values'][i])

            li.grid(row=0, column=0, columnspan=2)

            if self.tasksTree.parent(self.curItem) != '':
                confunct = lambda: self.delete_todo()
                delete = Button(self.canvas, text="Delete", width=12, command=lambda: self.confirm_popup(confunct, 
                                                                                            f"Are you sure you want to permanently remove {items['values'][0]} from this task?\n*clicking yes will permanently remove {items['values'][0]}",
                                                                                            '700x200'))
                delete.grid(row=2,column=1,sticky=W)
            else:
                confunct = lambda: self.delete_task()
                
                add_todo = Button(self.canvas, text="Add To-Do", width=24, command=lambda: self.init_todo())
                add_todo.grid(row=1,column=0, columnspan=2, sticky=W)

                edit = Button(self.canvas, text="Edit", width=12, command=lambda: self.edit_task())
                delete = Button(self.canvas, text="Delete", width=12, command=lambda: self.confirm_popup(confunct, 
                                                                                                         f"Are you sure you want to remove {items['text']} from the task list?\n*clicking yes will permanently remove {items['text']}",
                                                                                                         '700x200'))

                edit.grid(row=2,column=0, sticky=W)
                delete.grid(row=2,column=1, sticky=W)
            
        else:
            self.canvas.grid_forget()
            self.canvas.destroy()

if __name__ == "__main__":
    db = None
    pwd = None # cs361_Fall2024

    # Gets the input from the entry fields
    def get_res():
        db = databaseName.get()
        pwd = databasePass.get()
        print(db, pwd)
        temp.destroy()

        app = App()
        app.db = db
        app.pw = pwd
        app.root.bind('<<TreeviewSelect>>', app.inspect_item)
        app.establish_connection()
        app.populate_on_entry()
        app.task_page()
        app.root.mainloop()

    # Pre check for database 
    temp = Tk()
    temp.geometry('500x500')
    Label(temp, text="Please enter the name and password for the established database").pack()
    namelabel = Label(temp, text="Database Name: ")
    databaseName = Entry(temp, width=25)
    passlabel = Label(temp, text="Database Password: ")
    databasePass = Entry(temp, width=25, show="*")
    save = Button(temp, text="Confirm", command=lambda: get_res())
    namelabel.pack()
    databaseName.pack()
    passlabel.pack()
    databasePass.pack()
    save.pack()

    temp.mainloop()