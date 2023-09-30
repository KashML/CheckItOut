from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from typing import Dict

from main.model.model import AppModel
from main.view import AppView
from main.Widgets.task_button import TaskbuttonWidget
from main.controller.helper import validate_text_input
from main.controller.file_manager import FileManager
from main.model.data_types import TaskData


class AppController:
    
    def __init__(self, model, view):
        
        self.model: AppModel = model
        self.view: AppView = view
        self.file_manager = FileManager()


        # Counter for the TaskWidgets
        self.task_num = 0
        self.task_button_dict: Dict[int:TaskbuttonWidget] = {}


        # Connect UI interactions to model manipulations
        self.view.add_task_btn.clicked.connect(self.add_task)
        self.view.window.closeEvent = self.clean_up

        # Load previous data
        self.load_data()
        self.update_progress_bar()
        
    
        print("Initialized Controller")
    
    def add_task(self) -> None:
        """Handles the action of adding a task. Task can be
        added through the gui or loaded from memory
        """

        #Update View side
        task_name = validate_text_input(self.view.add_task_line.text())
        self.view.add_task_line.clear()
        print(f"Adding a new task : {task_name}")
        
        
        new_task = TaskbuttonWidget(task_name=task_name, id=self.task_num)
        new_task.clicked.connect(self.click_task)
        new_task.doubleClicked.connect(self.remove_task)
        self.view.task_frame_layout.addWidget(new_task)

        # Handle model side
        task_data = TaskData(task_name=task_name, id=self.task_num)
        self.model.add_task(task_data)
        
        # Update the controller
        self.task_button_dict[self.task_num] = new_task
        self.task_num = self.task_num + 1


    def click_task(self, checked):
        """Handles the action of a task being clicked"""

        # Handle view side
        button: TaskbuttonWidget = self.view.app.sender()

        # Handle model side
        self.model.add_clicked(id=button.id, checked=checked)

        self.update_progress_bar()
    
    def remove_task(self):
        """Handles the action of deleting a task"""

        button: TaskbuttonWidget = self.view.app.sender()
        
        # Delete button
        self.view.task_frame_layout.removeWidget(button)

        # Delete data
        self.model.remove_task(button.id)

        # Get rate of completion
        status = self.model.get_completion_rate()
        print(f"Completion rate : {status}%")

        self.view.progress_bar.set_value(int(status))

    
    def clean_up(self, event)-> None:
        """Cleaning up tasks"""

        print("Saving current tasks.....")
        self.file_manager.write_to_csv(self.model.get_task_list())

        print("Exiting App")
        event.accept()

    def load_data(self) -> None:
        """Load previous tasks from memory"""
        
        data_list = self.file_manager.load_as_list()
        for task in data_list:
            
            # Handle view side
            task_name = task.task_name
            new_task = TaskbuttonWidget(task_name=task_name, id=self.task_num)
            new_task.clicked.connect(self.click_task)
            new_task.doubleClicked.connect(self.remove_task)
            new_task.setChecked(task.complete)
            self.view.task_frame_layout.addWidget(new_task)

            # Handle model side
            task_data = TaskData(task_name=task_name, id=self.task_num, complete=task.complete)
            self.model.add_task(task_data)
            
            # Update Controller
            self.task_button_dict[self.task_num] = new_task
            self.task_num = self.task_num + 1


        print(f"{len(data_list)} tasks loaded")
    
    def update_progress_bar(self) -> None:
        """Updates progress by quering the model"""
        
        # Get rate of completion
        status = self.model.get_completion_rate()
        print(f"Completion rate : {status}%")

        self.view.progress_bar.set_value(int(status))

    

    



