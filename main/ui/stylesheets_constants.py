
# -------------------
#   TASK BUTTON 
#--------------------

#orange,pink, cyan,green
#BUTTON_COLOR_LIST = ["#FFBA55", "#FF6E40", "#0099CC"]

#Pinkish Green
BUTTON_COLOR_LIST = ["#FE4365","#FC9D9A","#F9CDAD","#C8C8A9","#83AF9B"]

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
                border-radius: 25px;
            }}
        """)

def get_button_style_checked(color):
        return (f"""
             QPushButton {{
                background-color: rgba(224, 224, 224, 0.2);
                border: 6px solid white;
                color: black;
                padding: 10px 40px;
                font-family: "Roboto", sans-serif;
                font-size: 16px;
                font-weight: bold;
                border-radius: 25px;
                text-decoration: line-through;
            }}
        """)