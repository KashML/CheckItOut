import os
import sys
import main
import pandas as pd
from server.server import ServerController

MAIN_DIR_PATH = os.path.dirname(main.__file__)
FILENAME = "tast_list_remote.txt"
FILEPATH = os.path.join(MAIN_DIR_PATH, FILENAME)

server_cntrl: ServerController = ServerController()
status = server_cntrl.establish_connection()

if status is False:
    sys.exit(1)

email_data: list = server_cntrl.get_data(is_all=True)

for subject,body in email_data:
    
    # Ensure its a task list
    if "task" in subject.lower():

        lines = body.splitlines()
        
        # Logic to determine append or overwrite
        if "clear" in lines[0]:

            # Write a new file
            with open(FILEPATH, 'w') as file:
                for line in line[0:]:
                    file.write(line + "\n")
            
        else:
            # Append to file
            with open(FILEPATH, 'a') as file:
                for line in lines:
                    file.write(line + "\n")

