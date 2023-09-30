
# -------------------
#   TASK BUTTON 
#--------------------

#orange,pink, cyan,green
BUTTON_COLOR_LIST = ["#FFBA55", "#FF6E40", "#0099CC"]

def get_button_style(color):
        return (f"""
             QPushButton {{
                background-color: {color};
                border: 6px solid white;
                color: black;
                padding: 10px 40px;
                font-family: "Roboto", sans-serif;
                font-size: 16px;
                font-weight: bold;
                border-radius: 20px;
            }}
            QPushButton:hover {{
                background-color: rgba(240, 240, 240, 0.9);
            }}
            QPushButton:checked {{
                background-color: rgba(224, 224, 224, 0.2);
                text-decoration: line-through;
            }}
        """)