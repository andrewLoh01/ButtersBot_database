from queue import Empty
from switch import switch
import os
import json
from switch import switchEncoder

    
def store(user, userName, switchName, switchNameType):
    with open('storage.json', "r+") as json_file:
        #check if no one has made list
        if os.stat("storage.json").st_size == 0:
            newSwitch = switch(switchNameType)
            userList = {user: {switchName:newSwitch}}
            json.dump(userList, json_file, cls=switchEncoder)
            json_file.truncate()
            return f"{userName}'s list has been created and {switchName} has been added."  
          
        else:
            data = json.load(json_file)
            #user has not create list yet
            if not user in data.keys():
                data[user] = {switchName: switch(switchNameType)}
                saveJson(data, json_file)
                
                return f"{userName}'s list has been created and {switchName} has been added."    
            #user has created list
            else:
                #if switch has not been added
                if not switchName in data[user]: 
                    data[user].update({switchName: switch(switchNameType)})
                    saveJson(data, json_file)
                    return f"{switchName} has been added to your list"
                
                elif switchName in data[user] and switchNameType != None:
                    data[user].update({switchName: switch(switchNameType)})
                    saveJson(data, json_file)
                    return f"{switchName} already in list, but added to {switchNameType} type switches"  
                                  
                #Switch has been added
                else:
                    return f"{switchName} has already been added"


def removeSwitch(user, switchName):
    with open('storage.json', "r+") as json_file:
        if os.stat("storage.json").st_size == 0:
            return "No one has made a list."
        else:
            data = json.load(json_file)
            if not user in data:
                return "Nothing to remove as you haven't made a list."
            
            userSwitches = data[user]
            
            #if its not in all then the switch has not been added
            if not switchName in userSwitches:
                return "Switch has not been added."
            else:
                #deletes the switch record in key[username]
                del userSwitches[switchName]
                saveJson(data, json_file)
                
                return f"{switchName} has been removed."
             
                
#Deletes user from list
def deleteAll(user):
    with open('storage.json', "r+") as json_file:
        if os.stat("storage.json").st_size == 0:
            return "No one has made a list."
        else:
            data = json.load(json_file)
            
            if not user in data:
                return "No list to delete"
            
            else:
                del data[user]
                saveJson(data, json_file)
                return f"Your list has been deleted."


#Adds store and weblinks to switch
def addLink(user, userName, switchName, nameAndlink, link):
    with open('storage.json', "r+") as json_file:
        if os.stat("storage.json").st_size == 0:
            store(user, userName, switchName, switchNameType=None)
        else:
            data = json.load(json_file)
            if not user in data or not switchName in data[user].keys():
                store(user, userName, switchName, switchNameType=None)
                
        userSwitchLinks = data[user][switchName]["links"]
        if (not ":" in nameAndlink) and link == None:
            return "Please include the store name and Hyperlink in format `store:Link` or `store` `link`"

        #Means storeName included and link included
        elif (not ":" in nameAndlink) and link != None:
            userSwitchLinks[nameAndlink] = link
            
        #If user decides to add storename:hyperLink hyperLink
        elif ":" in nameAndlink and link != None:
            name = nameAndlink.split(":")[0]
            userSwitchLinks[name] = link

        #User sends storeName:hyperLink
        else:
            name, hyperLink = nameAndlink.split(":")[0], nameAndlink.split(":")[1]
            userSwitchLinks[name] = hyperLink
            
        saveJson(data, json_file)
        return f"Link added to {switchName}"


#Removes a store link from switch
def removeLink(user, switchName, store):
    with open('storage.json', "r+") as json_file:
            if os.stat("storage.json").st_size == 0:
                return "Cannot remove link as no one has created a list."

            data = json.load(json_file)
            if not user in data:
                return "You have not made a list yet."
            
            elif not switchName in data[user].keys():
                return f"You have not added {switchName} to your switch list."
            
            userSwitchLinks = data[user][switchName]["links"]
            if not store in userSwitchLinks.keys():
                return f"{store} has not been added as a store"
            
            del userSwitchLinks[store]
            saveJson(data, json_file)
            return f"{store} has been removed from your {switchName} switch links."

      
#deletes all links of a switch
def delLinks(user, switchName):
    with open('storage.json', "r+") as json_file:
        if os.stat("storage.json").st_size == 0:
            return "Cannot remove link as no one has created a list."

        data = json.load(json_file)
        if not user in data:
            return "You have not made a list yet."
        
        elif not switchName in data[user].keys():
            return f"You have not added {switchName} to your switch list."
        
        data[user][switchName]["links"] = {}
        saveJson(data, json_file)
        return f"All links have been removed from your {switchName} switch links."
    
    
#returns all links     
def allLinks(user, switchName):
    with open('storage.json', "r+") as json_file:
        if os.stat("storage.json").st_size == 0:
            return "Cannot remove link as no one has created a list."

        data = json.load(json_file)
        if not user in data:
            return "You have not made a list yet."
        
        elif not switchName in data[user].keys():
            return f"You have not added any links to your {switchName} switch."
        
        elif data[user][switchName]["links"] == {} or data[user][switchName]["Links"] == None:
            return "No links found"

        #format the string
        string = f'{switchName} Links\n' +'\n'.join(f'{k}: {v}' for k, v in data[user][switchName]["links"].items())
        return string
  
    
def getShop(user, switchName, shop):
    with open('storage.json', "r+") as json_file:
        if os.stat("storage.json").st_size == 0:
            return "Cannot remove link as no one has created a list."

        data = json.load(json_file)
        if not user in data:
            return "You have not made a list yet."
        
        elif not switchName in data[user].keys():
            return f"You have not added any links to your {switchName} switch."
        
        
        for key in data[user][switchName]["links"].keys():
            if key == shop:
                return  f"{key} : "+ data[user][switchName]["links"][key]
            
        return f'{shop} was not found in {switchName} switch'
    
    
#save the json modification
def saveJson(data, json_file):
    json_file.seek(0)
    json.dump(data, json_file, cls=switchEncoder)
    json_file.truncate()
    json_file.close()        
    
