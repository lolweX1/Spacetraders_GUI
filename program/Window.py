import requests as rq
from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, 
                             QVBoxLayout, QLabel, QPushButton, QHBoxLayout, 
                             QSizePolicy, QTabWidget, QLineEdit)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QKeyEvent
from AccessAPI import *
from GlobalVariableAccess import *
from LoginWindow import *
from Canvas import *
import sys

def create_player(textBox):
    print(textBox.text())
    textBox.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # All input boxes go here
        # Standard set up is {"name": {"label": QLabel, "input": QLineEdit}}
        # However, there can be more keys to each name if it has specific attributes
        self.INPUTS = {
            "login": {
                "label": QLabel("Enter UID: "),
                "input": QLineEdit(),
                },
            "player_creation": {
                "label": QLabel("Create player: "),
                "input": QLineEdit(),
                },
        }

        # Setting window properties
        self.setWindowTitle("SpaceTrader API GUI")
        self.resize(400, 300)

        # Initalizing main window children
        self.window = QWidget()

        # Initalizing tabs
        self.tabs = QTabWidget()
        self.tab_names = {
            "player": {
                "layout": QVBoxLayout(),
                "tab": QWidget()
                }, 
            "info": {
                "layout": QVBoxLayout(),
                "tab": QWidget()
                }, 
            "map": {
                "layout": QVBoxLayout(),
                "tab": QWidget()
                },
            "prompt": {
                "layout": QVBoxLayout(),
                "tab": QWidget()
                },
        }

        # login

        # creating the player creation input, change to be optimized later 
        self.player_creation_container = QHBoxLayout()
        self.player_creation_container.addWidget(self.INPUTS["player_creation"]["label"], alignment=Qt.AlignmentFlag.AlignLeft)
        self.player_creation_container.addWidget(self.INPUTS["player_creation"]["input"], alignment=Qt.AlignmentFlag.AlignLeft)
        self.tab_names["player"]["layout"].addLayout(self.player_creation_container)
        self.INPUTS["player_creation"]["input"].returnPressed.connect(lambda: create_player(self.INPUTS["player_creation"]["input"]))

        # Creating tabs
        for tab in self.tab_names:
            self.tab_names[tab]["tab"].setLayout(self.tab_names[tab]["layout"])
            self.tabs.addTab(self.tab_names[tab]["tab"], tab.capitalize())

        # map canvas
        self.canvas = Canvas()
        self.tab_names["map"]["layout"].addWidget(self.canvas)

        # placing widgets into proper places
        temp_c = []

        # # create containers to store related widgets
        # for c in CHILDREN_CONTAINERS:
        #     CHILDREN_CONTAINERS[c][0] = QHBoxLayout()
        #     for i in CHILDREN_CONTAINERS[c][1]:
        #         # put the related widgets into the container before added the container to the window
        #         CHILDREN_CONTAINERS[c][0].addWidget(CHILDREN[i], alignment=Qt.AlignmentFlag.AlignLeft)
        #         temp_c.append(i)
        #         CHILDREN["missionsContainer"] = c

        # # add the children that are not in containers into the window
        # for c in CHILDREN:
        #     if "Container" in c:
        #         tab_names["info"]["layout"].addLayout(CHILDREN_CONTAINERS[CHILDREN[c]][0])
        #     elif (not (c in temp_c)):
        #         tab_names["info"]["layout"].addWidget(CHILDREN[c])

        # # Timers to for update data
        # self.constantUpdate = QTimer(self)
        # self.constantUpdate.timeout.connect(self.update_data_constant)
        # self.constantUpdate.start(2000)

        # self.rareUpdate = QTimer(self)
        # self.rareUpdate.timeout.connect(self.update_data_rare)
        # self.rareUpdate.start(30000)

        # toss main stuff into the window
        temp_layout = QVBoxLayout()
        temp_layout.addWidget(self.tabs)
        self.window.setLayout(temp_layout)
        self.setCentralWidget(self.window)
    
    # The update that updates quickly. Used for data that changes often such as location of ships
    def update_data_constant(self):
        pass

    # Update that updates slowly. Used for data that doesn't change often such as agent name and account details
    def update_data_rare(self):
        global data

        # checks API
        data = accessAgent(ID)

        # updates texts
        CHILDREN["agentName"].setText("Agent: " + data["data"]["symbol"])
        CHILDREN["credits"].setText("Credits: " + str(data["data"]["credits"]))