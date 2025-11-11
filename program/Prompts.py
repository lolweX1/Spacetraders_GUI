import requests as rq
from AccessAPI import *
import GlobalVariableAccess as gva
import re
from Prompts import *
from Authorize import *

nav_cmd = ["orbit", "navigate", "dock", "status", "exit"]
scan_cmd = ["waypoints", "ships", "systems", "exit"]
engage_cmd = ["extract", "cooldown", "exit"]

def navigate(funcs):
    for cmd in funcs:
        cmd = cmd.replace(" ", "").split("--")
        if cmd[0] in nav_cmd:
            if cmd[0] == "status":
                print(f"STATUS: {gva.ship_data["nav"]["status"]}")
            elif cmd[0] == "exit":
                return True
            else:
                authorize_ship_nav(cmd[0], cmd[1] if len(cmd) > 1 else None)
        else:
            return False
        update_ship_data()
    return True