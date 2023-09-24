
# -------------------
#   TASK BUTTON 
#--------------------

BTN_ORIG = """
        QPushButton {
            background-color: white; 
            border: 6px solid pink; 
            color: black; 
            padding: 10px 40px; 
            font-size: 16px; 
            font-weight: bold;
            border-radius: 20px; 
        }

        QPushButton:hover {
                background-color: #f0f0f0;
        }
        """

BTN_PRESSED = """
        QPushButton {
            background-color: white; 
            border: 6px solid pink; 
            color: black; 
            padding: 10px 40px; 
            font-size: 16px; 
            font-weight: bold;
            text-decoration: line-through;
            border-radius: 20px; 
        }

        QPushButton:hover {
                background-color: #f0f0f0;
        }
        """