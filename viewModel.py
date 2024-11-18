from TaskManagment_Main import *
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()

    funct_dict = {
        "saveEdit": ui.update_task,
        "saveTodo": ui.save_todo,
        "cancelEdit": ui.edit_cancel,
        "saveCreate": ui.create_task,
        "saveCancel": ui.exit_creation,
        "deleteTask": ui.delete_task,
        "beginTask": ui.to_timer,
        "exitTimer": ui.exit_timer,
    }   

    ui.taskList.selectionModel().selectionChanged.connect(
    ui.handle_clicked
    )

    ui.beginEdit.clicked.connect(lambda: ui.edit(True))

    ui.editSave.clicked.connect(lambda: ui.show_popup("Update Task?", "Are you sure you want to UPDATE this task? Doing so will change its view in the task list", funct_dict["saveEdit"]))

    ui.deleteTask.clicked.connect(lambda: ui.show_popup("Delete Task?", "Are you sure you want to DELETE this task? Doing so will permanently remove it and all related to-dos from the task list", funct_dict["deleteTask"], QMessageBox.Warning))

    ui.editCancel.clicked.connect(lambda: ui.show_popup("Cancel Edit?", "Are you sure you want to CANCEL editing this task? Doing so will reset all fields to their original values.", funct_dict["cancelEdit"], QMessageBox.Warning))

    ui.editTodoSave.clicked.connect(lambda: ui.show_popup("Add To-Do?", "Are you sure you want to ADD this To-Do to this task? Doing so will insert it into the task list, this cannot be edited after insertion", funct_dict["saveTodo"]))

    ui.addTaskButton.clicked.connect(ui.init_task)

    ui.createSave.clicked.connect(lambda: ui.show_popup("Create Task?", "Are you sure you want to CREATE this task? Doing so will add it to the task list. You can edit, delete, and begin tasks from the task list page.", funct_dict["saveCreate"]))

    ui.createCancel.clicked.connect(lambda: ui.show_popup("Cancel Creation?", "Are you sure you want to CANCEL creation of this task? Doing so will reset all entries and return you to the task list page.", funct_dict["saveCancel"], QMessageBox.Warning))

    ui.createTodo.clicked.connect(lambda: ui.view_create_todo(True))

    ui.todoSave.clicked.connect(lambda: ui.add_to_list())

    ui.todoCancel.clicked.connect(lambda: ui.view_create_todo(False))

    ui.beginTask.clicked.connect(lambda: ui.show_popup("Begin Task?", "Are you sure you want to BEGIN working on this task? Doing so will redirect you to the timer page where you can keep track of how long you've spent working.", funct_dict["beginTask"]))

    ui.timerReset.clicked.connect(lambda: ui.show_popup("Return to Task List?", "Are you sure you want to RETURN to the task list? Doing so will clear the stopwatch and redirect you back to the task list page.", funct_dict["exitTimer"], QMessageBox.Warning))

    ui.addTodo.clicked.connect(lambda: ui.edit_add_todo(True))

    ui.editTodoCancel.clicked.connect(lambda: ui.edit_add_todo(False))

    ui.helpButton.clicked.connect(lambda: ui.to_help(ui.stackedWidget.currentIndex()))

    ui.timerStart.clicked.connect(lambda: ui.begin_timer(True))

    ui.timerStop.clicked.connect(lambda: ui.begin_timer(False))

    sys.exit(app.exec_())