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

app = QApplication([])

ID = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9MV0VfWDIiLCJ2ZXJzaW9uIjoidjIuMy4wIiwicmVzZXRfZGF0ZSI6IjIwMjUtMDgtMzEiLCJpYXQiOjE3NTY3NDM3OTgsInN1YiI6ImFnZW50LXRva2VuIn0.MoB2TrV-5fd4EnXbxgKCy9vdilQhKVPTasLNXrqIzCOvVYo4qe8i6p0Af9NEbDbjQQ-72cI0rOJjyBhen1kB6y4wod-ACV9nft8Saq5uMkuJX_xvYMmd3U6JPNnUnNyK3AUPAVrrigkbElq7kV7ihL44Q45ecnPIgPqU-q7-Xo3tIwUVJBuSebqCNqvnShDXQ_ZFRZvBxm3kVdVR-oBqL5xXo5fLzSbWdsft71Im77H4LE7k1m0-CMqjSjY7ARXuvvJL5tMG96iNLYrg3-HgzS_YlzF8DNerNpZpYa2U85olO8N3mE06s0XkRi8bPbEdvqpcZFZUOrSfVo87MMh0E0RX0MG1tc9xqLZ9Y-EN0uAUGGf22W0ytVol8Qhtfq0QXCZaMSP-TuJzaCGcVoCYPGuKQntcK_1wlXJLaDUkGbX-RQf-Cp8Om9E-tJ0FkTnupPiDSTmt375BD7NZlUBwBpPpE3bGsYm0BGd4SHenkzx2qKxmvFhumYZdU6KOtr7wDL6R9t2oRAGc6MmSFz2xxShu1Ug7v24Rcytea96CD5o_Ok8MHi3C2n2PlPTDIJfVNfFIpZBxuOpEQQ8Iqrblxss49hznHvQ5AyQKBokxZWzxa6WAEYZiLYdRncZy4qhBoUWH1PUxzto6KWxuk3OglzXFgXsdXgR4tezZNb-pzwg"

# data = accessAgent(ID)
# missions = accessMissions(ID)
# ships = accessShip(ID)

# # check if data and mission work, then assign initial text
# if (data and missions and ships):
#     # data that relies on other data
#     system = accessSystem(ID, ships["data"][0]["nav"]["systemSymbol"])
#     systemsALL = accessAllSystems(ID)
#     # assign all CHILDREN children a value
#     CHILDREN["agentName"] = QLabel("Agent: " + data["data"]["symbol"])
#     CHILDREN["credits"] = QLabel("Credits: " + str(data["data"]["credits"]))
#     CHILDREN["missions"] = QLabel("Missions:")
#     CHILDREN["missions"].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
#     CHILDREN["missionExpand"] = QPushButton("\\/")
#     CHILDREN["missionText"] = QLabel("")
#     CHILDREN["ships"] = QLabel("ships: " + ships["data"][0]["nav"]["systemSymbol"])
#     CHILDREN["shipSystem"] = QLabel("system: ")
#     ORIGIN = [system["data"]["x"], system["data"]["y"]]
#     CURRENT_SYSTEM_WAYPOINTS.clear()
#     CURRENT_SYSTEM_WAYPOINTS.extend(system["data"]["waypoints"])

#     CONTRACTS.extend(missions["data"])

#     #assign buttons functions
#     CHILDREN["missionExpand"].clicked.connect(lambda: expandMissions(ID, CHILDREN["missionText"]))

# else:
#     # if unable to recieve data, close
#     print("unable to fetch data, closing window")
#     sys.exit()


# All input boxes go here
# Standard set up is {"name": {"label": QLabel, "input": QLineEdit}}
# However, there can be more keys to each name if it has specific attributes
INPUTS = {
    "login": {
        "label": QLabel("Enter UID: "),
        "input": QLineEdit(),
        },
    "player_creation": {
        "label": QLabel("Create player: "),
        "input": QLineEdit(),
        },
}

def create_player(textBox):
    print(textBox.text())
    textBox.clear()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
        self.player_creation_container.addWidget(INPUTS["player_creation"]["label"], alignment=Qt.AlignmentFlag.AlignLeft)
        self.player_creation_container.addWidget(INPUTS["player_creation"]["input"], alignment=Qt.AlignmentFlag.AlignLeft)
        self.tab_names["player"]["layout"].addLayout(self.player_creation_container)
        INPUTS["player_creation"]["input"].returnPressed.connect(lambda: create_player(INPUTS["player_creation"]["input"]))

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

login = Login()
if login.exec():
    window = MainWindow()
    window.show()

app.exec()



