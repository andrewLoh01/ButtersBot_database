from types import NoneType
import databaseConnect

#Check if username and switch record exist
def check(username, switch):
    query = """
        SELECT owner, name
        FROM SWITCH
        WHERE EXISTS (SELECT * FROM SWITCH WHERE owner = '{0}' AND name = '{1}');
    """.format(username, switch)
    connection, cursor = databaseConnect.connect()
    cursor.execute(query)
    check = cursor.fetchall()
    if check == []:
        return False
    else:
        return True

def shopAndLinkAdded(username, switch, shop, link):
    #insert into json data cell of table SWITCH
    query = """
    UPDATE SWITCH 
    SET links = links || '{{"{2}":"{3}"}}'
    WHERE owner='{0}' AND name='{1}';
    """.format(username, switch, shop, link)
    return query

def shopAndLinkNotAdded(username, switch, shop, link):
    query = """
    UPDATE SWITCH 
    SET links = '{{"{2}":"{3}"}}'
    WHERE owner='{0}' AND name='{1}';
    """.format(username, switch, shop, link)
    return query

#Universal access to database
connection, cursor = databaseConnect.connect()


def addSwitch(username, name, switch, type=None):
    checkExistance = check(username, switch)
    
    #If record does not exist, add to db
    if checkExistance == False:
        query = """
            INSERT INTO SWITCH (owner, name, type)
            VALUES ('{0}', '{1}', '{2}');
        """.format(username, switch, type)
        cursor.execute(query)
        connection.commit()
    else:
        if type == None:
            return"{0} already added for {1}".format(switch, name)
        else:
            updateSwitchType(username, name, switch, type)
            return "{0} has already added {1}, but updated type to {2}".format(name, switch, type)
            
            
def updateSwitchType(username, name, switch, type):
    checkExistance = check(username, switch)
    if checkExistance == False:
        return ( "{0} has not added {1} to their list".format(username, switch))
    else:
        query = """
        UPDATE SWITCH
        SET type='{2}'
        WHERE owner='{0}' AND name='{1}';
        """.format(username, switch, type)
        cursor.execute(query)
        connection.commit()
        return ("{0}'s {1} type set to {2}".format(name, switch, type))



def getType(username, type):
    switchType = ""
    switchTypes = ['linear', 'tactile', 'clicky']
    if type in switchTypes or type[0:-1] in switchTypes:
        if type[0:-1] in switchTypes:
            switchType = type[0:-1]
        else:
            switchType = type
        query = """
        SELECT name
        FROM SWITCH
        WHERE owner='{0}' AND type='{1}'
        ORDER BY name ASC;
        """.format(username, switchType)
        cursor.execute(query)
        switches = cursor.fetchall()
        switchList = "{0} switches:\n".format(switchType.capitalize())
        for switch in switches:
            switchList =  switchList +" - "+ switch[0]+ "\n"
            
        return (switchList)
    else:
        return("The {0} type is invalid".format(type))


def getSwitchLinks(username, switch):
    query = """
    SELECT links
    FROM SWITCH
    WHERE owner='{0}' AND name='{1}';
    """.format(username, switch)
    
    cursor.execute(query)
    links = cursor.fetchall()[0][0]

    formatString = "Vendors selling {0} switches:\n".format(switch)
    for key in links.keys():
        formatString = formatString + "- {0}\n  - Link:{1}\n\n".format(key.capitalize(), links[key])
        
    return(formatString)
    
#Format for shopLink = shop:link or shop link
def addLink(username, name,  switch, shopLink, link=None):
    checkExist = check(username, switch)
    if checkExist == False:
        print( "{0}'s record for {1} switch does not exist".format(name, switch))
    else:
        shopAndLink = shopLink
        #if shop:link is used
        query=""
        checkQuery = """
        SELECT links
        FROM SWITCH
        WHERE owner='{0}' AND name='{1}';
        """.format(username, switch)
        cursor.execute(checkQuery)
        existance = cursor.fetchall()[0][0]
        
        #shop:link format used
        if link==None:
            try:
                shopAndLink = shopLink.split(":", 1)
                shop = shopAndLink[0]
                hyperlink = shopAndLink[1]
            except LookupError as error:
                return("Try shop:link or shop link format")
            else:
                if type(existance) is NoneType:
                    query = shopAndLinkNotAdded(username, switch, shop, hyperlink)
                else:
                    query = shopAndLinkAdded(username, switch, shop, hyperlink)
                    
                cursor.execute(query)
                connection.commit()
                return("{0} link for {1} switch has been added".format(shop, switch))      
        #if shop link is used
        else:
            if type(existance) is NoneType:
                query = shopAndLinkNotAdded(username, switch, shop, hyperlink)
            else:
                #insert into json data cell of table SWITCH
                query = shopAndLinkAdded(username, switch, shop, hyperlink)
                
            cursor.execute(query)
            connection.commit()
            return("{0} link for {1} switch has been added".format(shop, switch))      
            
            

def deleteLinks(username, name, switch):
    try:
        query="""
        UPDATE SWITCH 
        SET links = Null
        WHERE owner='{0}' and name='{1}';
        """.format(username, switch)
        cursor.execute(query)
        connection.commit()
    except LookupError as error:
        return(error)
    else:
        return("{1} links have been deleted for {0}".format(name, switch))


#not removing link
def removeLink(username, store, switch):
    checkExist = check(username, switch)
    if checkExist is True:
        query = """WITH removeLink AS (        
            UPDATE SWITCH
            SET links = links::jsonb - '{1}'
            WHERE owner='{0}' AND name='{2}'
            RETURNING *
            )
            SELECT * FROM removeLink""".format(username, store, switch)
        cursor.execute(query)
        connection.commit()
        
        #leaves residue {} so have to set back to null
        checkLinks = """
        SELECT links
        FROM SWITCH
        WHERE owner='{0}' AND name='{1}'
        """.format(username, switch)
        cursor.execute(checkLinks)
        json = cursor.fetchall()[0][0]
        #if the json is {} and not NoneType/Null
        if json == {}:
            noneType = """
            UPDATE SWITCH
            SET links = Null
            WHERE owner='{0}' AND name='{1}'
            """.format(username, switch)
            cursor.execute(noneType)
            connection.commit()
        
        return("{0} has been removed for {1}".format(store, switch))
    else:
        return("{0} does not exist in {1}'s list".format(switch, username))

#Try to format, so discord bot show storename as hyperlink for switch
def getSwitchShop(username, switch, store):
    query = """
    
    """

def getSwitchType(username, name, switch):
    query = """
    SELECT type FROM SWITCH
    WHERE owner='{0}' AND name='{1}';
    """.format(username, switch)
    
    cursor.execute(query)
    switchType = cursor.fetchall()[0][0]
    if switchType == 'None':
        return "{0} type for {1} has not been set".format(name, switch)
    else:
        return switchType
    

def getAll(username, name):
    #Check existance entries belonging to user
    query = """
    SELECT name, type
    FROM SWITCH
    WHERE owner='{0}'
    ORDER BY TYPE, NAME;
    """.format(username)
    cursor.execute(query)
    switches = cursor.fetchall()
    

    stringDic = {'linear': "Linear Switches:\n", 'tactile':"Tactile Switches:\n", 'clicky':"Clicky Switches:\n", 'None':"Unassigned Switches:\n"}
    
    if switches == []:
        return "{0} has not added any switches".format(name)
    else:  
        
        for switch in switches:
            switchName = switch[0]
            switchType = switch[1]
            stringDic[switchType] = stringDic[switchType] + " - " + switchName + "\n"
        
        returnString = ""
            
        for key in stringDic.keys():
            returnString = returnString + stringDic[key] + "\n\n"
        
        return(returnString)
            

        
def deleteSwitch(username,name,  switch):
    deleteQuery = """
    DELETE FROM SWITCH
    WHERE owner='{0}' AND name='{1}';
    """.format(username, switch)
    
    checkExist = check(username, switch)
    if checkExist is True:
        cursor.execute(deleteQuery)
        connection.commit()
        return "{0} switch has been delete for {1}.".format(switch, name)
    else:
        return "{0} switch has not been added for {1}.".format(switch, name)
    

def deleteAll(username, name):
    deleteAllQuery = """
    DELETE FROM SWITCH
    WHERE owner='{0}';
    """.format(username)
    
    cursor.execute(deleteAllQuery)
    connection.commit()
    
    return("{0}'s list has been wiped.".format(name))

#add methods to check and update switches if owned
#add in quantity amount
#add in where these switches used
#change in quantity methods

    

addSwitch("01and01#4025", "01and01", "durock-pom")
addSwitch("01and01#4025", "01and01", "ktt-fang-whites")
addSwitch("01and01#4025", "01and01", "ktt-seasalt")
addSwitch("01and01#4025", "01and01", "ktt-peaches", 'linear')
addSwitch("01and01#4025", "01and01", "tangerines", 'linear')
addSwitch("01and01#4025", "01and01", "kiwis", 'tactile')
addSwitch("01and01#4025", "01and01", "sp-metor-white", 'linear')
addSwitch("01and01#4025", "01and01", "boba-lt", 'linear')
addSwitch("01and01#4025", "01and01", "boba-gums", 'linear')
addSwitch("01and01#4025", "01and01", "t1", 'tactile')
addSwitch("01and01#4025", "01and01", "blue-bubblegums", 'linear')

"""addLink("01and01#4025", "01and01", "blue-bubblegums", "keygem:https://keygem.com/products/grouo-buy-blue-bubblegum-linear")
addLink("01and01#4025", "01and01", "blue-bubblegums", "allcaps:https://allcaps.store/products/gb-bubblegum-linear-switch")
addLink("01and01#4025", "01and01", "blue-bubblegums", "swagkeys:https://swagkeys.com/products/gateron-blue-bubblegum-linear-switch10pcs")
addLink("01and01#4025", "01and01", "boba-lt", "daily-clack:https://dailyclack.com/products/gazzew-boba-linear-thock")"""

addLink("01and01#4025", "01and01", "kiwis", "daily-clack:https://dailyclack.com/products/gazzew-boba-linear-thock")
removeLink("01and01#4025", 'daily-clack', 'kiwis')
removeLink("01and01#4025", 'adf', 'blue-bubblegums')