from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from main.model import AppModel
from main.view import AppView
from main.Widgets.task_button import TaskbuttonWidget
from main.helper import validate_text_input

class AppController:
    
    def __init__(self, model, view):
        self.model: AppModel = model
        self.view: AppView = view


        # Connect UI interactions to model manipulations
        self.view.add_task_btn.clicked.connect(self.add_task)
        print("Initialized Controller")
    
    def add_task(self) -> None:
        """Handles the action of adding a task"""

        # Handle view side
        task_name = validate_text_input(self.view.add_task_line.text())
        self.view.add_task_line.clear()
        print(f"Adding a new task : {task_name}")
        
        new_task = TaskbuttonWidget(title=task_name)
        new_task.clicked.connect(self.click_task)
        new_task.doubleClicked.connect(self.remove_task)
        self.view.task_frame_layout.addWidget(new_task)

        # Handle model side
        self.model.add_task(new_task)

    def click_task(self, checked):
        """Handles the action of a task being clicked"""

        button: TaskbuttonWidget = self.view.app.sender()
        button.toggle(checked)

        # Get rate of completion
        status = self.model.get_completion_rate()
        print(f"Completion rate : {status}%")

        self.view.progress_bar.set_value(int(status))
    
    def remove_task(self):

        button: TaskbuttonWidget = self.view.app.sender()
        
        # Delete button
        self.model.remove_task(button)
        self.view.task_frame_layout.removeWidget(button)

        # Get rate of completion
        status = self.model.get_completion_rate()
        print(f"Completion rate : {status}%")

        self.view.progress_bar.set_value(int(status))




