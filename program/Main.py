import requests as rq
from AccessAPI import *
import GlobalVariableAccess as gva
import re
from Prompts import *
from Authorize import *
from SystemCanvas import *
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
    "contract": "access contract functions",
    "subfunctions": "use \"-\" to call multiple subfunctions at once and use \"--\" to put in parameters for each subfunction\nex: nav -navigate --[name of destination]",
    "create": "create a window for give object"
}
commands = ["nav", "engage", "contract", "create", "cmdqt", "help"]



try:
    data = rq.get("https://api.spacetraders.io/v2/my/ships", headers = {"Authorization": "Bearer " + gva.current_auth_token})
    data = data.json()
    gva.system = data["data"][0]["nav"]["systemSymbol"] # CHANGE
    gva.ship = data["data"][0]["symbol"] # CHANGE
    gva.ship_data = data["data"][0] # CHANGE
    print("data retrieval successful")
except:
    print("Unable to fetch agent data")

fetch_waypoints()


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
    a = parent_options(nav_cmd, sel)
    return a

def scan_options(sel = None):
    a = parent_options(scan_cmd, sel)
    return a

def engage_options(sel = None):
    a = parent_options(engage_cmd, sel)
    return a

def contract_options(sel = None):
    a = parent_options(contract_cmd, sel)
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
        update_ship_data()
        return ""
    if ("fetch" in command):
        cmd = cmd.split("-", 1)
        data = get_generic_data(cmd[1])
        print(data)
    
    prompt = re.split("(?<= )-(?!-)", command)
    prompt = [i.replace(" ", "") for i in prompt]
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
            if (len(prompt) <= 1):
                engage_options()
                command = input("select cmd> ")
                command = engage_options(command)
                engage([command])
            else:
                engage(prompt[1:])
        case "contract":
            if (len(prompt) <= 1):
                contract_options()
                command = input("select cmd> ")
                command = contract_options(command)
                contract([command])
            else:
                contract(prompt[1:])
        case "create":
            create(prompt[1:] if len(prompt) > 1 else ["system"])
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


