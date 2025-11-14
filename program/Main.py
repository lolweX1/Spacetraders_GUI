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

version = "0.32 beta"

commands_help = {
    "nav": "go into ship navigation mode",
    "engage": "actions that can be done while docked",
    "cmdqt": "exit the UI",
    "contract": "access contract functions",
    "subfunctions": "use \"-\" to call multiple subfunctions at once and use \"--\" to put in parameters for each subfunction\nex: nav -navigate --[name of destination]",
    "create": "create a window for give object"
}
commands = ["nav", "engage", "contract", "create", "cmdqt", "help"]

def int_convert(s):
    """
    Determines whether given value is Integer or not

    Args: 
        s: A value, it can be anything.

    Returns:
        The integer value of the parameter otherwise None
    """
    try:
        int(s)
        return int(s)
    except:
        return None

def parent_options(op, sel=None):
    """
    A generic function that prints out all the possible options or returns the selected function
    
    Args: 
        op (list): A list that has the names of the options you want to print out.
        sel (None|int): The selected option that you want, the value of the first option is 1.
    Returns:
        Any or None: The selected option (`op[sel-1]`), or None if `sel` is
        None. If `sel` is None, the function prints the options.
    """
    if (sel is None):
        print("".join(f"{i+1}) {op[i]} \n" for i in range(len(op))))
        return None
    else:
        int_op = int_convert(sel)
        return (op[int_op-1] if (int_op and int_op <= len(op) and int_op >= 1) else None)

def flying_options(sel = None):
    """
    A thin wrapper function for parent_options that prints out all options for the flying section

    Args:
        sel (int | None): The index of the option you want to be returned, the index of the first object is 1.
    
    Returns:
        str or None: The selected option string, or None if sel is None or invalid.
        If sel is None, the function prints the options instead of returning a value.    """
    a = parent_options(nav_cmd, sel)
    return a

def scan_options(sel = None):
    """
    A thin wrapper function for parent_options that prints out all options for the scan section

    Args:
        sel (int | None): The index of the option you want to be returned, the index of the first object is 1.
    
    Returns:
        str or None: The selected option string, or None if sel is None or invalid.
        If sel is None, the function prints the options instead of returning a value.    """
    a = parent_options(scan_cmd, sel)
    return a

def engage_options(sel = None):
    """
    A thin wrapper function for parent_options that prints out all options for the engage section

    Args:
        sel (int | None): The index of the option you want to be returned, the index of the first object is 1.
    
    Returns:
        str or None: The selected option string, or None if sel is None or invalid.
        If sel is None, the function prints the options instead of returning a value.    """
    a = parent_options(engage_cmd, sel)
    return a

def contract_options(sel = None):
    """
    A thin wrapper function for parent_options that prints out all options for the contract section

    Args:
        sel (int | None): The index of the option you want to be returned, the index of the first object is 1.
    
    Returns:
        str or None: The selected option string, or None if sel is None or invalid.
        If sel is None, the function prints the options instead of returning a value.
    """
    a = parent_options(contract_cmd, sel)
    return a

def get_ship_data(command):
    """
    Prints selected data for the current ship.

    The command is a space-separated string. The first word is ignored. Any
    following words are treated as attribute names. If no attributes are
    provided, all ship data is printed.

    Args:
        command (str): Space-separated string where the first segment is
            ignored and the remaining segments (if any) are attribute names.

    Returns:
        str: Always an empty string; printing is used for output.
    """
    command = command.lstrip().split(" ")[1:]
    if (len(command) == 0):
        print(gva.ship_data)
    else:
        try:
            print("".join(f"{call}: {gva.ship_data[call]}\n" for call in command))
        except Exception as e:
            print(f"parameter: '{e}' does not exist")
    return ""

values = {
    "nav": [flying_options, navigate],
    "engage": [engage_options, engage],
    "contract": [contract_options, contract],
}
def determine_prompt(command):
    """
        A function to break down the given command and execute it as such.
        Args:
            Command (str): The given command. Format - "[section] -function1(optional) --parameters (if needed) -function2..."
            You can have any amount of functions as long as they are all within the same section. If no functions are given, 
            you will be given an option screen with all possible options.
        Returns: 
            - Returns "Successful" if the function is able to execute the prompt(regardless of success or failure), 
            - Returns the string "None" if the function is able to catch a bad input.
            - Returns the Python object None if there is an error that the function could not catch 
    """
    global cmd
    global cmd_skip

    cmd_skip = False

    # updates the ship data if the user is attempting to get info on ship
    if ("get" in command):
        get_ship_data(command)
        update_ship_data()
        return "Successful"
    
    # fetch is a special function because it's generic, meaning that it has no specific function except for the user to get any data
    if ("fetch" in command):
        cmd = cmd.split("-", 1)
        data = get_generic_data(cmd[1])
        print(data)
        return "Successful"
    
    # splits the prompts
    prompt = re.split("(?<= )-(?!-)", command)
    prompt = [i.replace(" ", "") for i in prompt]
    
    # grouping the functions in values (variable) because executing them have the same lines of code
    if prompt[0] in values:
        if (len(prompt) <= 1):
            values[prompt[0]][0]()
            command = input("select cmd> ")
            command = values[prompt[0]][0](command)
            if (command == None):
                cmd_skip = True
                return "Failure"
            values[prompt[0]][1]([command])
        else:
            values[prompt[0]][1](prompt[1:])

    # seperate miscellanous functions
    match prompt[0]:
        case "create":
            create(prompt[1:] if len(prompt) > 1 else ["system"])
        case "help":
            print("".join(f"{key} - {commands_help[key]}\n" for key in commands_help))
    return "Successful"

if __name__ == "__main__":
    print(f"Welcome to Lolwe's UI for Space Trader API\nversion {version}\nTo find functions, please use command \"help\"")

    # Intialize all necessary data
    try:
        data = rq.get("https://api.spacetraders.io/v2/my/ships", headers = {"Authorization": "Bearer " + gva.current_auth_token})
        data = data.json()
        gva.system = data["data"][0]["nav"]["systemSymbol"] # CHANGE, have the ability to select different ships
        gva.ship = data["data"][0]["symbol"] # CHANGE
        gva.ship_data = data["data"][0] # CHANGE
        print("data retrieval successful")
    except:
        print("Unable to fetch agent data")

    # obtain all waypoints within system to make "create" faster
    fetch_waypoints()

    # begin the prompt process
    cmd = input("command> ")
    cmd_skip = False

    # prompt process
    while (cmd != "cmdqt"):
        cmd = determine_prompt(cmd)
        print(cmd)
        if (not cmd_skip):
            cmd = input("command> ")