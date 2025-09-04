import requests as rq
from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, 
                             QVBoxLayout, QLabel, QPushButton, QHBoxLayout, 
                             QSizePolicy, QTabWidget)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QPixmap, QKeyEvent
from AccessAPI import *
from GlobalVariableAccess import *
from Canvas import *
import sys

app = QApplication([])

ID = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiTE9MV0VfWDIiLCJ2ZXJzaW9uIjoidjIuMy4wIiwicmVzZXRfZGF0ZSI6IjIwMjUtMDgtMzEiLCJpYXQiOjE3NTY3NDM3OTgsInN1YiI6ImFnZW50LXRva2VuIn0.MoB2TrV-5fd4EnXbxgKCy9vdilQhKVPTasLNXrqIzCOvVYo4qe8i6p0Af9NEbDbjQQ-72cI0rOJjyBhen1kB6y4wod-ACV9nft8Saq5uMkuJX_xvYMmd3U6JPNnUnNyK3AUPAVrrigkbElq7kV7ihL44Q45ecnPIgPqU-q7-Xo3tIwUVJBuSebqCNqvnShDXQ_ZFRZvBxm3kVdVR-oBqL5xXo5fLzSbWdsft71Im77H4LE7k1m0-CMqjSjY7ARXuvvJL5tMG96iNLYrg3-HgzS_YlzF8DNerNpZpYa2U85olO8N3mE06s0XkRi8bPbEdvqpcZFZUOrSfVo87MMh0E0RX0MG1tc9xqLZ9Y-EN0uAUGGf22W0ytVol8Qhtfq0QXCZaMSP-TuJzaCGcVoCYPGuKQntcK_1wlXJLaDUkGbX-RQf-Cp8Om9E-tJ0FkTnupPiDSTmt375BD7NZlUBwBpPpE3bGsYm0BGd4SHenkzx2qKxmvFhumYZdU6KOtr7wDL6R9t2oRAGc6MmSFz2xxShu1Ug7v24Rcytea96CD5o_Ok8MHi3C2n2PlPTDIJfVNfFIpZBxuOpEQQ8Iqrblxss49hznHvQ5AyQKBokxZWzxa6WAEYZiLYdRncZy4qhBoUWH1PUxzto6KWxuk3OglzXFgXsdXgR4tezZNb-pzwg"

data = accessAgent(ID)
missions = accessMissions(ID)
ships = accessShip(ID)
system = accessSystem(ID, ships["data"][0]["nav"]["systemSymbol"])
systemsALL = accessAllSystems(ID)

# check if data and mission work, then assign initial text
if (data and missions and ships):
    # assign all CHILDREN children a value
    CHILDREN["agentName"] = QLabel("Agent: " + data["data"]["symbol"])
    CHILDREN["credits"] = QLabel("Credits: " + str(data["data"]["credits"]))
    CHILDREN["missions"] = QLabel("Missions:")
    CHILDREN["missions"].setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    CHILDREN["missionExpand"] = QPushButton("\\/")
    CHILDREN["missionText"] = QLabel("")
    CHILDREN["ships"] = QLabel("ships: " + ships["data"][0]["nav"]["systemSymbol"])
    CHILDREN["shipSystem"] = QLabel("system: ")
    ORIGIN = [system["data"]["x"], system["data"]["y"]]
    CURRENT_SYSTEM_WAYPOINTS.clear()
    CURRENT_SYSTEM_WAYPOINTS.extend(system["data"]["waypoints"])

    #assign buttons functions
    CHILDREN["missionExpand"].clicked.connect(lambda: expandMissions(ID, CHILDREN["missionText"]))

    # check for all missions and add them
    for m in missions["data"]:
        txt = "deadline: " + m["terms"]["deadline"] + ", " + m["type"] + ": " + "deliver " + m["terms"]["deliver"][0]["tradeSymbol"] + " " + str(m["terms"]["deliver"][0]["unitsRequired"])
        CHILDREN["missionText"].setText(CHILDREN["missions"].text() + "\n" + txt)
else:
    # if unable to recieve data, close
    print("unable to fetch data, closing window")
    sys.exit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting window properties
        self.setWindowTitle("SpaceTrader API GUI")
        self.resize(400, 300)

        # Initalizing main window children
        window = QWidget()

        # Initalizing tabs
        tabs = QTabWidget()
        infoTab = QWidget()
        mapTab = QWidget()
        
        # setting info layout
        infoLayout = QVBoxLayout()
        infoTab.setLayout(infoLayout)
        tabs.addTab(infoTab, "Info")

        # setting map layout
        mapLayout = QVBoxLayout()
        mapTab.setLayout(mapLayout)
        tabs.addTab(mapTab, "Map")

        # map canvas
        canvas = Canvas()
        mapLayout.addWidget(canvas)

        # placing widgets into proper places
        temp_c = []

        # create containers to store related widgets
        for c in CHILDREN_CONTAINERS:
            CHILDREN_CONTAINERS[c][0] = QHBoxLayout()
            for i in CHILDREN_CONTAINERS[c][1]:
                # put the related widgets into the container before added the container to the window
                CHILDREN_CONTAINERS[c][0].addWidget(CHILDREN[i], alignment=Qt.AlignmentFlag.AlignLeft)
                temp_c.append(i)
                CHILDREN["missionsContainer"] = c

        # add the children that are not in containers into the window
        for c in CHILDREN:
            if "Container" in c:
                infoLayout.addLayout(CHILDREN_CONTAINERS[CHILDREN[c]][0])
            elif (not (c in temp_c)):
                infoLayout.addWidget(CHILDREN[c])

        # Timers to for update data
        self.constantUpdate = QTimer(self)
        self.constantUpdate.timeout.connect(self.update_data_constant)
        self.constantUpdate.start(2000)

        self.rareUpdate = QTimer(self)
        self.rareUpdate.timeout.connect(self.update_data_rare)
        self.rareUpdate.start(30000)

        # toss main stuff into the window
        temp_layout = QVBoxLayout()
        temp_layout.addWidget(tabs)
        window.setLayout(temp_layout)
        self.setCentralWidget(window)
    
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

window = MainWindow()
window.show()

app.exec()



