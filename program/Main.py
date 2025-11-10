import requests as rq
from AccessAPI import *
import GlobalVariableAccess as gva
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

print(f"Welcome to Lolwe's UI for Space Trader API\nthis is version {version}\nTo find functions, please use command \"help\"")

ship = None
ship_data = None
system = None

try:
    data = rq.get("https://api.spacetraders.io/v2/my/ships", headers = {"Authorization": "Bearer " + gva.current_auth_token})
    data = data.json()
    system = data["data"][0]["nav"]["systemSymbol"] # CHANGE
    ship = data["data"][0]["symbol"] # CHANGE
    ship_data = data["data"][0] # CHANGE
except:
    print("Unable to fetch agent data")

def auth_access(li, post = False, bd = None):
    try:
        headers = {"Authorization": f"Bearer {gva.current_auth_token}"}

        if bd is not None:
            headers["Content-Type"] = "application/json"

        if post:
            response = rq.post(li, headers=headers, json=bd)
        else:
            response = rq.get(li, headers=headers)

        data = response.json()

        if "error" in data:
            print(f"Error {data['statusCode']}: {data['error']} - {data['message']}")
            return None

        return data

    except Exception as e:
        print("Unable to fetch data:", e)
        return None

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

def authorize_ship_engage(op):
    return auth_access(f"https://api.spacetraders.io/v2/my/ships/{ship}/{op}", True)

def authorize_ship_nav(op):
    def access(post=True, navi = None): # maybe remove later
        try:
            url = f"https://api.spacetraders.io/v2/my/ships/{ship}/{op}"
            headers = {"Authorization": f"Bearer {gva.current_auth_token}"}

            if navi:  # for navigate
                headers["Content-Type"] = "application/json"
                data = {"waypointSymbol": navi}
                response = rq.post(url, headers=headers, json=data)
            else:
                if post:
                    response = rq.post(url, headers=headers)
                else:
                    response = rq.get(url, headers=headers)

            data = response.json()
            if "error" in data:
                print(f"Error {data["error"]["code"]}: {data["error"]["message"]} ")
                return None
            return data
        except Exception as e:
            print("Unable to fetch data:", e)
            return None
    if (op == "navigate"):
        cmd = input("location> ")
        success = access(True, cmd)
    else: success = access()
    return success

def update_ship_data():
    global ship_data
    ship_data = auth_access(f"https://api.spacetraders.io/v2/my/ships/{ship}")["data"]

cmd = input("command> ")
while (cmd != "cmdqt"):
    cmd_skip = False
    if ("get" in cmd):
        cmd = cmd.lstrip().split(" ")[1:]
        if (len(cmd) == 0):
            print(ship_data)
        else:
            try:
                print("".join(f"{call}: {ship_data[call]}\n" for call in cmd))
            except Exception as e:
                print(f"parameter: '{e}' does not exist")
        # print("".join((f"\033[1m{name}\033[0m:" + ("    \n".join(f"{n2}: {ship_data[name][n2]}\n" for n2 in ship_data[name])) if isinstance(ship_data[name], dict) else f"{ship_data[name]}\n") for name in ship_data))
    elif (cmd == "nav"):
        flying_options()
        cmd = input("select cmd> ")
        cmd = flying_options(cmd)
        if (cmd == None):
            cmd = "nav"
            cmd_skip = True
        elif (cmd == "status"):
            print(f"STATUS: {ship_data["nav"]["status"]}")
            cmd = "nav"
            cmd_skip = True
        elif (cmd != "exit"):
            if (not authorize_ship_nav(cmd)): # runs authorize_ship_nav
                cmd = "nav"
                cmd_skip = True
                continue
            update_ship_data()
            print(f"STATUS: {ship_data["nav"]["status"]}")
    elif (cmd == "engage"):
        engage_options()
        cmd = input("select cmd> ")
        cmd = engage_options(cmd)
        if (cmd != "exit"):
            if (not authorize_ship_engage(cmd)): # runs authorize_ship_nav
                cmd = "engage"
                cmd_skip = True
                continue
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


