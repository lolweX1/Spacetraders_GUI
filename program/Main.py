import requests as rq
from AccessAPI import *
import GlobalVariableAccess as gva
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, 
                             QVBoxLayout, QLabel, QPushButton, QHBoxLayout, 
                             QSizePolicy, QTabWidget, QLineEdit)
from LoginWindow import *
from Canvas import *
import sys
from Window import *

app = QApplication([])

def init():
    data = accessAgent(gva.current_auth_token)
    print(data)

# verify agent
login = Login()
if login.exec():
    init()
    window = MainWindow()
    window.show()

app.exec()

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


