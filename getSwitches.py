import json
import os

"""Returns strings of switches"""

#open the file and check
def openFile():
    with open('storage.json', "r+") as json_file:
        try:
            data = json.load(json_file)
        except:
            return None
        else:
            json_file.close()
            return data

#return the switch type 
#need to return a statement sends if switchType list is empty
def getSwitches(user, switchType):
    data = openFile()
    #If json file is empty
    if data == None:
        return "No one has made a list yet"
    #check if user is in data
    elif not user in data:
        return f"You do not any switches"
    
    switchList = findSwitches(user, switchType, data)
    
    if switchList == [] or switchList is None:
        return f"You have no {switchType} switches."
    
    switches = sorted(switchList)
    
    switchList = (f"\n{switchType.capitalize()} switches:\n") + ' | ' .join(switches)
    return switchList
    


#Returns all switches
def getAll(user):
    data = openFile()

    #If json file is empty
    if data == None:
        return "No one has made a list yet"
    #check if user is in data
    elif not user in data:
       return "You do not have any switches"

    linears = findSwitches(user, "linear", data)
    tactile = findSwitches(user, "tactile", data)
    clicky = findSwitches(user, "clicky", data)
            
    #format the string
    string = ("\nLinear switches:\n" + ' | ' .join(linears) +"\n\n"\
        "Tactile switches:\n" + ' | ' .join(tactile) +"\n\n"\
        "Clicky switches:\n" + ' | ' .join(clicky) +"\n")

    return string

def findSwitches(user, switchType, data):
    switchMatchingType = []
    for switch in data[user].keys():
        if data[user][switch]["switchType"] == switchType:
            switchMatchingType.append(switch)

    return switchMatchingType




