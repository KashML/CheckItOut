from main.Widgets.task_button import TaskbuttonWidget
from main.model.data_types import TaskData, Era

class AppModel:
    
    def __init__(self):
        self._task_dict: dict[int, TaskData] = {}
        self._task_dict_current: dict[int, TaskData] = {}
        print("Initialized Model")
    
    def add_task(self, task: TaskData) -> None:
        """Add the taskbuttons to a dict"""
        self._task_dict[task.id] = task
    
    def add_clicked(self, id: int, checked: bool) -> None:
        """Updates the status of the task"""
        if self._task_dict.get(id) is not None:
            self._task_dict[id].complete = checked

    
    def get_num_tasks(self) -> int:
        """Get total number of task in the current dict"""
        return len(self._task_dict_current.keys())

    def get_num_completed_tasks(self) -> int:
        """Get number of tasks which are checked in the current dict"""
        count = 0 
        for task in self._task_dict_current.values():
            if task.complete is True:
                count = count + 1
        return count
    
    def get_num_idle_tasks(self) -> int:
        """Get number of idle tasks in the current dict"""
        return self.get_num_tasks - self.get_num_completed_tasks()
                
    def remove_task(self, id: int) -> None:
        """Removes task from dict"""
        self._task_dict.pop(id)

    def get_completion_rate(self) -> float:
        """ Get percentage of completion"""
        if self.get_num_tasks() == 0:
            return 0.0
        
        rate = self.get_num_completed_tasks()/self.get_num_tasks()
        return rate*100

    def get_task_list(self) -> list:
        return self._task_dict.values()

    def get_task_id_by_filter(self, filter: Era) -> list:

        id_list = []
        for task in self._task_dict.values():
            if task.era == filter:
                id_list.append(task.id)
        return id_list

    def set_working_task_list(self, filter: Era) -> list:

        id_list = self.get_task_id_by_filter(filter=filter)
        # Empty the current directory and fill it again.
        self._task_dict_current = {}
        for id in id_list:
            self._task_dict_current[id] = self._task_dict[id]

    def set_current_dir_to_full_dir(self):
        self._task_dict_current = self._task_dict.copy()


    
