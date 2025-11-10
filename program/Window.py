# import requests as rq
# # from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, 
# #                              QVBoxLayout, QLabel, QPushButton, QHBoxLayout, 
# #                              QSizePolicy, QTabWidget, QLineEdit)
# # from PyQt6.QtCore import QTimer, Qt
# # from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QKeyEvent
# from AccessAPI import *
# from GlobalVariableAccess import *
# from LoginWindow import *
# from Canvas import *
# import sys

# def create_player(textBox):
#     print(textBox.text())
#     textBox.clear()

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         # All input boxes go here
#         # Standard set up is {"name": {"label": QLabel, "input": QLineEdit}}
#         # However, there can be more keys to each name if it has specific attributes
#         self.INPUTS = {
#             "login": {
#                 "label": QLabel("Enter UID: "),
#                 "input": QLineEdit(),
#                 },
#             "player_creation": {
#                 "label": QLabel("Create player: "),
#                 "input": QLineEdit(),
#                 },
#         }

#         # creating set ups through tabs
#         self.player_tab_setup = {
#             "player_data": [{
#                 "agent_name": QLabel("Agent name: "),
#                 "credits": QLabel("credits: "),
#                 "starting_faction": QLabel("starting faction: "),
#                 "ship_count": QLabel("ships: ")
#             }, QVBoxLayout()]
#         }

#         # Setting window properties
#         self.setWindowTitle("SpaceTrader API GUI")
#         self.resize(400, 300)

#         # Initalizing main window children
#         self.window = QWidget()

#         # Initalizing tabs
#         self.tabs = QTabWidget()
#         self.tab_names = {
#             "player": {
#                 "layout": QVBoxLayout(),
#                 "tab": QWidget()
#                 }, 
#             "info": {
#                 "layout": QVBoxLayout(),
#                 "tab": QWidget()
#                 }, 
#             "map": {
#                 "layout": QVBoxLayout(),
#                 "tab": QWidget()
#                 },
#             "prompt": {
#                 "layout": QVBoxLayout(),
#                 "tab": QWidget()
#                 },
#         }
#         self.tab_names["prompt"]["tab"].setStyleSheet("background-color: black")

#         # assign special attributes to certain layouts in player tab
#         self.player_tab_setup["player_data"][1].setSpacing(0)

#         # toss all widgets and layout into the window
#         for layout in self.player_tab_setup:
#             for widget in self.player_tab_setup[layout][0]:
#                 self.player_tab_setup[layout][1].addWidget(self.player_tab_setup[layout][0][widget])
#                 self.player_tab_setup[layout][0][widget].setAlignment(Qt.AlignmentFlag.AlignTop)
#                 self.player_tab_setup[layout][0][widget].setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
#             self.tab_names["player"]["layout"].addLayout(self.player_tab_setup[layout][1])
        


#         # creating the player creation input, change to be optimized later 
#         self.player_creation_container = QHBoxLayout()
#         self.player_creation_container.addWidget(self.INPUTS["player_creation"]["label"], alignment=Qt.AlignmentFlag.AlignLeft)
#         self.player_creation_container.addWidget(self.INPUTS["player_creation"]["input"], alignment=Qt.AlignmentFlag.AlignLeft)
#         self.tab_names["player"]["layout"].addLayout(self.player_creation_container)
#         self.INPUTS["player_creation"]["input"].returnPressed.connect(lambda: create_player(self.INPUTS["player_creation"]["input"]))

#         # Creating tabs
#         for tab in self.tab_names:
#             self.tab_names[tab]["tab"].setLayout(self.tab_names[tab]["layout"])
#             self.tabs.addTab(self.tab_names[tab]["tab"], tab.capitalize())

#         # map canvas
#         self.canvas = Canvas()
#         self.tab_names["map"]["layout"].addWidget(self.canvas)

#         self.input = PromptLineEdit()
#         self.tab_names["prompt"]["layout"].addWidget(self.input)

#         # placing widgets into proper places
#         temp_c = []

#         # toss main stuff into the window
#         temp_layout = QVBoxLayout()
#         temp_layout.addWidget(self.tabs)
#         self.window.setLayout(temp_layout)
#         self.setCentralWidget(self.window)
    
#     # The update that updates quickly. Used for data that changes often such as location of ships
#     def update_data_constant(self):
#         pass

#     # Update that updates slowly. Used for data that doesn't change often such as agent name and account details
#     def update_data_rare(self):
#         global data

#         # checks API
#         data = accessAgent(ID)

#         # updates texts
#         CHILDREN["agentName"].setText("Agent: " + data["data"]["symbol"])
#         CHILDREN["credits"].setText("Credits: " + str(data["data"]["credits"]))

# class PromptLineEdit(QLineEdit):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.prompt = "> "
#         self.setText(self.prompt)
#         self.cursorPositionChanged.connect(self.keep_prompt)
#         self.textChanged.connect(self.prevent_prompt_delete)
#         self.returnPressed.connect(self.on_enter)
#         self.setStyleSheet("""
#             QLineEdit {
#                 background: transparent;
#                 color: lime;
#                 border: none;
#                 font-family: Consolas;
#                 font-size: 14px;
#             }
#         """)

#     def keep_prompt(self, old_pos, new_pos):
#         """Prevent cursor from moving before the prompt."""
#         if self.cursorPosition() < len(self.prompt):
#             self.setCursorPosition(len(self.prompt))

#     def prevent_prompt_delete(self, text):
#         """Ensure the prompt cannot be erased."""
#         if not text.startswith(self.prompt):
#             self.setText(self.prompt)
#             self.setCursorPosition(len(self.prompt))

#     def keyPressEvent(self, event):
#         """Block backspace and left-arrow before the prompt."""
#         if (self.cursorPosition() <= len(self.prompt)
#                 and event.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Left)):
#             return
#         super().keyPressEvent(event)
    
#     def on_enter(self):
#         self.mission(self.text()[2:])
#         self.setText(self.prompt)
    
#     def mission(self, cmd):
#         cmd = cmd.replace(" ", "")
#         if (current_auth_token != ""):
#             url = ""
#             if ("getship" == cmd):
#                 url = "https://api.spacetraders.io/v2/my/ships"
#             if (url != ""):
#                 try:
#                     data = rq.get(url, headers = {"Authorization": "Bearer " + current_auth_token})
#                     print(data.json())
#                 except:
#                     print("Unable to fetch data")
#         else:
#             print("no ship set")