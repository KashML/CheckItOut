
from typing import Dict

from main.model.model import AppModel
from main.view import AppView
from main.Widgets.task_button import TaskbuttonWidget
from main.controller.helper import validate_text_input
from main.controller.file_manager import FileManager
from main.controller.splunk_logger import SplunkLogger
from main.model.data_types import TaskData, Era
from main.controller.server_worker import ServerWorker
from main.controller.sound_controller import SoundController

class AppController:
    
    def __init__(self, model, view):
        
        self.model: AppModel = model
        self.view: AppView = view
        self.file_manager = FileManager()

        #Initalize the sound controller
        self.sound_ctrl = SoundController()

        #Initialize the logger
        splunk_log = SplunkLogger(status_bar_view=self.view)
        self.log = splunk_log.log


        # Counter for the TaskWidgets
        self.task_num = 0
        self.task_button_dict: Dict[int:TaskbuttonWidget] = {}

        # Set Mode
        self.mode: Era = Era.ALL

        # Connect UI interactions to model manipulations
        #TODO - Feature The add button only adds tasks as daily.
        self.view.add_task_btn.clicked.connect(self.add_task)

        self.cloud_worker = None
        self.cloud_worker_create() 
        self.view.cloud_update.clicked.connect(self.cloud_worker_start)

        self.view.window.closeEvent = self.clean_up
        self.view.clear_all_action.triggered.connect(self.clear_all_action)
        self.view.save_action.triggered.connect(self.save_action)
        self.view.load_last_action.triggered.connect(self.load_last_save)

        self.view.filter_all_action.triggered.connect(self.display_all)
        self.view.filter_daily_action.triggered.connect(lambda: self.display_by_filter(Era.DAILY))
        self.view.filter_monthly_action.triggered.connect(lambda: self.display_by_filter(Era.MONTHLY))
        self.view.filter_workout_week_action.triggered.connect(lambda: self.display_by_filter(Era.WORKOUT_WEEKLY))

        # Load previous data
        self.load_data()
        self.model.set_current_dir_to_full_dir()
        self.update_progress_bar()
        
        # Switching on the sounds only after initialization
        self.sound_ctrl.set_sound_on()
        self.log("Initialized Controller")

    # --------------
    # Core Functions
    # --------------

    def add_task(self) -> None:
        """Handles the action of adding a task by the user
        """
        self.sound_ctrl.click_sound()

        #Update View side
        task_name = validate_text_input(self.view.add_task_line.text())
        self.view.add_task_line.clear()
        self.log(f"Adding a new task : {task_name}")

        era = Era.DAILY if self.mode == Era.ALL else self.mode
        self.create_task(task_name=task_name,era=era)


    def click_task(self, checked):
        """Handles the action of a task being clicked"""
        self.sound_ctrl.task_toggle_sound()

        # Handle view side
        button: TaskbuttonWidget = self.view.app.sender()
        button.toggle(checked)

        # Handle model side
        self.model.add_clicked(id=button.id, checked=checked)

        self.update_progress_bar()
    
    def remove_task(self):
        """Handles the action of deleting a task by double clicking on it"""
        self.sound_ctrl.task_delete_sound()

        button: TaskbuttonWidget = self.view.app.sender()
        self.delete_task(id=button.id)
        
    
    def clean_up(self, event)-> None:
        """Cleaning up tasks"""

        self.log("Saving current tasks.....")
        self.file_manager.write_to_csv(self.model.get_task_list())

        self.log("Exiting App")
        event.accept()

    def create_task(self, task_name: str, complete: bool = False, era: Era = Era.DAILY) -> None:
        """Creates a new task"""

        # Handle view
        new_task = TaskbuttonWidget(task_name=str(task_name), id=self.task_num)
        new_task.clicked.connect(self.click_task)
        new_task.doubleClicked.connect(self.remove_task)
        new_task.setChecked(complete)
        new_task.toggle(complete)
        self.view.task_frame_layout.addWidget(new_task)

        # Handle model side
        task_data = TaskData(task_name=str(task_name), id=self.task_num, complete=complete, era=era)
        self.model.add_task(task_data)
        
        # Update the controller
        self.task_button_dict[self.task_num] = new_task
        self.task_num = self.task_num + 1
        self.update_progress_bar()

    def delete_task(self, id: int) -> None:
        """Deletes a task"""
        
        # Handle Model Side
        self.model.remove_task(id)

        # Handle View side
        button = self.task_button_dict.get(id)
        self.view.task_frame_layout.removeWidget(button)
        button.hide()
        button.deleteLater()
        self.update_progress_bar()

        # Update Controller
        self.task_button_dict.pop(id)
    
    def hide_task(self, id:int) -> None:
        """Hides a task only from View"""

        button: TaskbuttonWidget = self.task_button_dict.get(id)
        button.hide()
        self.view.task_frame_layout.update()

    def hide_all_tasks(self) -> None:
        """Hides all the tasks only from View"""

        for id in self.task_button_dict.keys():
            self.hide_task(id)

    def show_task(self, id:int) -> None:
        """Shows a task on the view"""

        button: TaskbuttonWidget = self.task_button_dict.get(id)
        button.show()
        self.view.task_frame_layout.update()

    def load_data(self) -> None:
        """Load previous tasks from memory"""
        
        data_list: list[TaskData] = self.file_manager.load_as_list()
        for task in data_list:
            # Handle view side
            self.create_task(task_name=task.task_name, complete=task.complete, era=task.era)

        self.log(f"{len(data_list)} tasks loaded")
    
    def update_progress_bar(self) -> None:
        """Updates progress by querying the model"""
        
        # Get rate of completion
        status = self.model.get_completion_rate()

        if int(status) == 100:
            self.sound_ctrl.complete_celebrate()

        self.view.progress_bar.set_value(int(status))


    def log(self, message: str) -> None:
        """Function to display message on the status bar"""
        self.view.status_bar.showMessage(message)

    # --------------
    # Server Functions
    # --------------

    def cloud_worker_create(self) -> None:
        """Creates a cloud worker thread"""
        self.server_worker: ServerWorker = ServerWorker()
        self.server_worker.startSignal.connect(self.cloud_worker_start_gui_update)
        self.server_worker.finishedSignal.connect(self.cloud_worker_end)

    def cloud_worker_start(self) -> None:
        """Starts the cloud worker thread"""
        self.sound_ctrl.click_sound()
        
        # If thread is running, terminate it 
        if self.server_worker.isRunning():
            print("OH NO : Thread was running")  
            self.server_worker.terminate()
            self.server_worker.wait() 

        self.cloud_worker_create()
        self.server_worker.start()    

    def cloud_worker_start_gui_update(self) -> None:
        """Update the GUI with a message"""
        self.log("Fetching data from server. Please wait .....")
        self.view.cloud_update.setEnabled(False)
    
    def cloud_worker_end(self, status, clear, task_list) -> None:
        """Handles the task when the cloud upload worker is done"""
        self.sound_ctrl.get_email_sound()

        if clear is True:
            self.clear_all_action()

        if status is False:
            self.log("Cloud Update failed")
            self.view.cloud_update.setEnabled(True)
            return

        for task in task_list:
            self.create_task(task_name=task.task_name, complete=task.complete, era=task.era)

        self.log(f"Complete. Number of tasks fetched : {len(task_list)}")
        self.view.cloud_update.setEnabled(True)

    # ----------------
    # Menu Functions
    # ----------------

    def clear_all_action(self) -> None:
        """Clears all existing tasks on the App"""
        self.sound_ctrl.menu_click_sound()

        key_list = list(self.task_button_dict.keys())

        for key in key_list:
            self.delete_task(key)

    def save_action(self) -> None:
        """Saves curent task to file when user clicks save"""
        self.sound_ctrl.save_sound()

        self.log("Saving current tasks.....")
        self.file_manager.write_to_csv(self.model.get_task_list())

    def load_last_save(self) -> None:
        """Loads last save when user clicks save"""
        self.sound_ctrl.menu_click_sound()
        self.load_data()

    def display_all(self) -> None:
        """Displays all tasks irrespective to their era"""
        self.sound_ctrl.menu_click_sound()

        self.model.set_current_dir_to_full_dir()
        for task_id in self.task_button_dict.keys():
            self.show_task(task_id)

        self.update_progress_bar()
        self.mode = Era.ALL
        self.view.mode_text.setText("Mode: ALL")
        self.log("Currently displaying all tasks")

    def display_by_filter(self, filter: Era) -> None:
        """Displays tasks only tagged as daily"""
        self.sound_ctrl.menu_click_sound()

        # Update View
        self.hide_all_tasks()
        id_list = self.model.get_task_id_by_filter(filter=filter)
        for id in id_list:
            self.show_task(id)

        #Update Model
        self.model.set_working_task_list(filter=filter)

        self.update_progress_bar()
        self.mode = filter
        self.view.mode_text.setText(f"Mode: {filter.value}")
        self.log(f"Currently displaying only {filter.value} goals")

