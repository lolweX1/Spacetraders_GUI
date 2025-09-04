import requests as rq
from GlobalVariableAccess import *

URL = {
    "agent": "https://api.spacetraders.io/v2/my/agent",
    "missions": "https://api.spacetraders.io/v2/my/contracts",
    "ships": "https://api.spacetraders.io/v2/my/ships",
    "systems": "https://api.spacetraders.io/v2/systems",
}

def accessAgent(id: str):
    data = None
    try:
        data = rq.get(URL["agent"], headers = {"Authorization": "Bearer " + id})
        data.json()
    except:
        print("Unable to fetch agent data")
        return data
    else:
        return data.json()
    
def accessMissions(id: str):
    data = None
    try:
        data = rq.get(URL["missions"], headers = {"Authorization": "Bearer " + id})
        data.json()
    except:
        print("Unable to fetch mission data")
        return data
    else:
        return data.json()

def accessShip(id: str):
    data = None
    try:
        data = rq.get(URL["ships"], headers = {"Authorization": "Bearer " + id})
        data.json()
    except:
        print("Unable to fetch ship data")
        return data
    else:
        return data.json()
    
def accessAllSystems(id: str):
    data = None
    try:
        data = rq.get(URL["systems"], headers = {"Authorization": "Bearer " + id})
        data.json()
    except:
        print("Unable to fetch systems data")
        return data
    else:
        return data.json()

def accessSystem(id: str, systemName: str):
    data = None
    try:
        data = rq.get(URL["systems"] + "/" + systemName, headers = {"Authorization": "Bearer " + id})
        data.json()
    except:
        print("Unable to fetch system data")
        return data
    else:
        return data.json()



def expandMissions(id: str, missionWidget):
    data = CHILDREN["missions"]
    missionWidget.setText("hi")