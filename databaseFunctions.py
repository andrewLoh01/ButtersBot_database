from types import NoneType
import databaseConnect

#Check if user and switch record exist
def check(user, switch):
    query = """
        SELECT owner, name
        FROM SWITCH
        WHERE EXISTS (SELECT * FROM SWITCH WHERE owner = '{0}' AND name = '{1}');
    """.format(user, switch)
    connection, cursor = databaseConnect.connect()
    cursor.execute(query)
    check = cursor.fetchall()
    if check == []:
        return False
    else:
        return True

def shopAndLinkAdded(user, switch, shop, link):
    #insert into json data cell of table SWITCH
    query = """
    UPDATE SWITCH 
    SET links = links || '{{"{2}":"{3}"}}'
    WHERE owner='{0}' AND name='{1}';
    """.format(user, switch, shop, link)
    return query

def shopAndLinkNotAdded(user, switch, shop, link):
    query = """
    UPDATE SWITCH 
    SET links = '{{"{2}":"{3}"}}'
    WHERE owner='{0}' AND name='{1}';
    """.format(user, switch, shop, link)
    return query

#Universal access to database
connection, cursor = databaseConnect.connect()


def addSwitch(user, username, switch, type=None):
    checkExistance = check(user, switch)
    
    #If record does not exist, add to db
    if checkExistance == False:
        query = """
            INSERT INTO SWITCH (owner, name, type)
            VALUES ('{0}', '{1}', '{2}');
        """.format(user, switch, type)
        cursor.execute(query)
        connection.commit()
        return "{1} switch has been added".format(switch)
    else:
        if type == None:
            return"{0} already added".format(switch)
        else:
            updateSwitchType(user, username, switch, type)
            return "Already added {0}, but updated type to {1}".format(switch, type)
            
            
def updateSwitchType(user, username, switch, type):
    checkExistance = check(user, switch)
    if checkExistance == False:
        return ( "{0} has not been added to their list".format(switch))
    else:
        query = """
        UPDATE SWITCH
        SET type='{2}'
        WHERE owner='{0}' AND name='{1}';
        """.format(user, switch, type)
        cursor.execute(query)
        connection.commit()
        return ("{0} type set to {1}".format(switch, type))



def getType(user, username, type):
    switchTypes = ['linear', 'tactile', 'clicky', 'None']
    if type in switchTypes:
        query = """
        SELECT name
        FROM SWITCH
        WHERE owner='{0}' AND type='{1}'
        ORDER BY name ASC;
        """.format(user, type)
        cursor.execute(query)
        switches = cursor.fetchall()
        if type == "None":
            switchList = "Unassigned switches for {0}:\n".format(username)        
        else:
            switchList = "{0} switches for {1}:\n".format(type.capitalize(), username)
        for switch in switches:
            switchList =  switchList +" - "+ switch[0]+ "\n"
        
        return (switchList)
    else:
        return("The {0} type is invalid".format(type))


def getSwitchLinks(user, switch):
    query = """
    SELECT links
    FROM SWITCH
    WHERE owner='{0}' AND name='{1}';
    """.format(user, switch)
    
    cursor.execute(query)
    links = cursor.fetchall()[0][0]

    formatString = "Vendors selling {0} switches:\n".format(switch)
    for key in links.keys():
        formatString = formatString + "- {0}\n  - Link:{1}\n\n".format(key.capitalize(), links[key])
        
    return(formatString)
    
#Format for shopLink = shop:link or shop link
def addLink(user, username,  switch, shopLink, link=None):
    checkExist = check(user, switch)
    if checkExist == False:
        return( "Record for {0} switch does not exist".format(switch))
    else:
        shopAndLink = shopLink
        #if shop:link is used
        query=""
        checkQuery = """
        SELECT links
        FROM SWITCH
        WHERE owner='{0}' AND name='{1}';
        """.format(user, switch)
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
                    query = shopAndLinkNotAdded(user, switch, shop, hyperlink)
                else:
                    query = shopAndLinkAdded(user, switch, shop, hyperlink)
                    
                cursor.execute(query)
                connection.commit()
                return("{0} link for {1} switch has been added".format(shop, switch))      
        #if shop link is used
        else:
            if type(existance) is NoneType:
                query = shopAndLinkNotAdded(user, switch, shop, hyperlink)
            else:
                #insert into json data cell of table SWITCH
                query = shopAndLinkAdded(user, switch, shop, hyperlink)
                
            cursor.execute(query)
            connection.commit()
            return("{0} link for {1} switch has been added".format(shop, switch))      
            
            

def deleteLinks(user, username, switch):
    try:
        query="""
        UPDATE SWITCH 
        SET links = Null
        WHERE owner='{0}' and name='{1}';
        """.format(user, switch)
        cursor.execute(query)
        connection.commit()
    except LookupError as error:
        return(error)
    else:
        return("{0} links have been deleted}".format(switch))


#not removing link
def removeLink(user, store, switch):
    checkExist = check(user, switch)
    if checkExist is True:
        query = """WITH removeLink AS (        
            UPDATE SWITCH
            SET links = links::jsonb - '{1}'
            WHERE owner='{0}' AND name='{2}'
            RETURNING *
            )
            SELECT * FROM removeLink""".format(user, store, switch)
        cursor.execute(query)
        connection.commit()
        
        #leaves residue {} so have to set back to null
        checkLinks = """
        SELECT links
        FROM SWITCH
        WHERE owner='{0}' AND name='{1}'
        """.format(user, switch)
        cursor.execute(checkLinks)
        json = cursor.fetchall()[0][0]
        #if the json is {} and not NoneType/Null
        if json == {}:
            noneType = """
            UPDATE SWITCH
            SET links = Null
            WHERE owner='{0}' AND name='{1}'
            """.format(user, switch)
            cursor.execute(noneType)
            connection.commit()
        
        return("{0} has been removed for {1}".format(store, switch))
    else:
        return("{0} does not exist in your list".format(switch))

#Try to format, so discord bot show storename as hyperlink for switch
def getSwitchShop(user, switch, store):
    query = """
    SELECT links::json->'{2}'
    FROM SWITCH
    WHERE owner='{0}' AND name='{1}'
    """.format(user, switch, store)
    cursor.execute(query)
    links = cursor.fetchall()[0][0]
    if links is None:
        return("Store has not been added")
    else:
        return("Switch - {0}\n{1}: {2}".format(switch, store, links))
    

def getAll(user, username):
    #Check existance entries belonging to user
    query = """
    SELECT name, type
    FROM SWITCH
    WHERE owner='{0}'
    ORDER BY TYPE, NAME;
    """.format(user)
    cursor.execute(query)
    switches = cursor.fetchall()
    
    stringDic = {'linear': "Linear Switches:\n", 'tactile':"Tactile Switches:\n", 'clicky':"Clicky Switches:\n", 'None':"Unassigned Switches:\n"}
    
    if switches == []:
        return "You have not added any switches"
    else:  
        
        for switch in switches:
            switchName = switch[0]
            switchType = switch[1]
            stringDic[switchType] = stringDic[switchType] + " - " + switchName + "\n"
        
        returnString = ""
            
        for key in stringDic.keys():
            returnString = returnString + stringDic[key] + "\n\n"
        
        return(returnString)
            

        
def deleteSwitch(user, username,  switch):
    deleteQuery = """
    DELETE FROM SWITCH
    WHERE owner='{0}' AND name='{1}';
    """.format(user, switch)
    
    checkExist = check(user, switch)
    if checkExist is True:
        cursor.execute(deleteQuery)
        connection.commit()
        return "{0} switch has been deleted.".format(switch)
    else:
        return "{0} switch has not been added.".format(switch)
    

def deleteAll(user, username):
    deleteAllQuery = """
    DELETE FROM SWITCH
    WHERE owner='{0}';
    """.format(user)
    
    cursor.execute(deleteAllQuery)
    connection.commit()
    
    return("list has been wiped.")

#add methods to check and update switches if owned
#add in quantity amount
#add in where these switches used
#change in quantity methods