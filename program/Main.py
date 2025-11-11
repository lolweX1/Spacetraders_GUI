import requests as rq
from AccessAPI import *
import GlobalVariableAccess as gva
import re
from Prompts import *
from Authorize import *
# from PyQt6.QtCore import QTimer, Qt
# from PyQt6.QtWidgets import (QApplication, QWidget, QMainWindow, QPushButton, 
#                              QVBoxLayout, QLabel, QPushButton, QHBoxLayout, 
#                              QSizePolicy, QTabWidget, QLineEdit)
# from LoginWindow import *
# from Canvas import *
# from Window import *

# app = QApplication([])

# def init():
#     data = accessAgent(gva.current_auth_token)

# verify agent
# login = Login()
# if login.exec():
#     init()
#     window = MainWindow()
#     window.show()

# app.exec()

# PLEASE CHANGE ALL SHIPS GET 0 TO THE SHIP WANTED
version = "0.32 beta"

print(f"Welcome to Lolwe's UI for Space Trader API\nversion {version}\nTo find functions, please use command \"help\"")

commands_help = {
    "nav": "go into ship navigation mode",
    "engage": "actions that can be done while docked",
    "cmdqt": "exit the UI",
    "subfunctions": "use \"-\" to call multiple subfunctions at once and use \"--\" to put in parameters for each subfunction\nex: nav -navigate --[name of destination]"
}
commands = ["nav", "engage", "cmdqt", "help"]

try:
    data = rq.get("https://api.spacetraders.io/v2/my/ships", headers = {"Authorization": "Bearer " + gva.current_auth_token})
    data = data.json()
    gva.system = data["data"][0]["nav"]["systemSymbol"] # CHANGE
    gva.ship = data["data"][0]["symbol"] # CHANGE
    gva.ship_data = data["data"][0] # CHANGE
    print("data retrieval successful")
except:
    print("Unable to fetch agent data")


def int_convert(s):
    try:
        int(s)
        return int(s)
    except:
        return None


def parent_options(op, sel):
    if (not sel):
        print("".join(f"{i+1}) {op[i]} \n" for i in range(len(op))))
        return None
    else:
        return (op[int_convert(sel)-1] if (int_convert(sel) and int_convert(sel) <= len(op)) else None)


def flying_options(sel = None):
    op = ["orbit", "navigate", "dock", "status", "exit"]
    a = parent_options(op, sel)
    return a

def scan_options(sel = None):
    op = ["waypoints", "ships", "systems", "exit"]
    a = parent_options(op, sel)
    return a

def engage_options(sel = None):
    op = ["extract", "cooldown", "exit"]
    a = parent_options(op, sel)
    return a

cmd = input("command> ")
cmd_skip = False

def get_ship_data(command):
    command = command.lstrip().split(" ")[1:]
    if (len(command) == 0):
        print(gva.ship_data)
    else:
        try:
            print("".join(f"{call}: {gva.ship_data[call]}\n" for call in command))
        except Exception as e:
            print(f"parameter: '{e}' does not exist")
    return ""

def determine_prompt(command):
    global cmd
    global cmd_skip

    cmd_skip = False

    if ("get" in command):
        get_ship_data(command)
        return ""
    
    prompt = re.split("(?<!-)-(?!-)", command.replace(" ", ""))
    print(prompt)
    match prompt[0]:
        case "nav":
            if (len(prompt) <= 1):
                flying_options()
                command = input("select cmd> ")
                command = flying_options(command)
                navigate([command])
            else:
                navigate(prompt[1:])
        case "engage":
            engage_options()
            command = input("select cmd> ")
            command = engage_options(command)
            if (command != "exit"):
                if (not authorize_ship_engage(command)): # runs authorize_ship_nav
                    cmd_skip = True
                    return "engage"
        case "help":
            print("".join(f"{key} - {commands_help[key]}\n" for key in commands_help))

while (cmd != "cmdqt"):
    cmd = determine_prompt(cmd)
    if (not cmd_skip):
        cmd = input("command> ")

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


