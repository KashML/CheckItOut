from main.Widgets.task_button import TaskbuttonWidget
from main.model.data_types import TaskData

class AppModel:
    
    def __init__(self):
        self._task_list: dict[int, TaskData] = {}
        print("Initialized Model")
    
    def add_task(self, task: TaskData) -> None:
        """Add the taskbuttons to a dict"""
        self._task_list[task.id] = task
    
    def add_clicked(self, id: int, checked: bool) -> None:
        """Updates the status of the task"""
        self._task_list[id].complete = checked

    
    def get_num_tasks(self) -> int:
        """Get total number of task in the dict"""
        return len(self._task_list.keys())

    def get_num_completed_tasks(self) -> int:
        """Get number oftasks which are checked"""
        count = 0 
        for task in self._task_list.values():
            if task.complete is True:
                count = count + 1
        return count
    
    def get_num_idle_tasks(self) -> int:
        """Get number of idle tasks"""
        return self.get_num_tasks - self.get_num_completed_tasks()
                
    def remove_task(self, id: int) -> None:
        """Removes task from dict"""
        self._task_list.pop(id)

    def get_completion_rate(self) -> float:
        """ Get percentage of completion"""
        if self.get_num_tasks() == 0:
            return 0.0
        
        rate = self.get_num_completed_tasks()/self.get_num_tasks()
        return rate*100

    def get_task_list(self) -> list:
        return self._task_list.values()


    
