import discord
from discord.ext import commands
import random
import databaseFunctions 
import requests

intents = discord.Intents.all()
TOKEN ='MTAxNTkzMDQ3MTgxNDc5MTIzOQ.GWiF7Y.czzZeWb_hCo5UlUZa4iRiArBW5g4w5xFg1Z-BI'


bot = commands.Bot(command_prefix='!', intents=intents)
channel = bot.get_channel(1015931835525627904)

#shows how to use add, remove tierlist
@bot.command(name="commands")
#ctx context (information about how command was executed)
async def help(ctx):
    await ctx.channel.send("command works")
    embed=discord.Embed(title="Commands to use my features", \
        description=\
        "\
        Use `!add` `switch-name` `type of switch` to add a switch to its type, `type of switch` is optional. Add spaces with a -\n \
        Use `!linear` to get all linear switches\n\
        Use `!tactile` to get all tactile switches\n\
        Use `!clicky`  to get all clicky switches\n\
        Use `!all to get all switches`\n\
        Use `!remove` `switch name` `type of switch` will remove the switch. Leaving out `type of switch` will still remove the switch from everywhere\n\
        Use `!DELETE` to remove all switches\n\
        Use `!aLink` `switch name` `storeName:link` to get sale links from vendor\n\
        Use `!rLink` `switch name` `storeName` to remove store and link\n\
        Use `!DELETELinks` to get sale links from vendor\n\
        Use `!shop` `switch name` `storeName` to get store link from store\n\
        Use `!check` 'currency' 'amount 'to get exchange rate. Can exclude amount"\
        , color=0xFFFFFF)
    await ctx.send(embed=embed)
    return


@bot.command(name="add")
#ctx context (information about how command was executed)
async def switchAdd(ctx, switch=None, switchType=None):
    user, userName = getUsername(ctx)
    if switch == None:
        await ctx.channel.send("Please add a switch")
        return
    else:
        await ctx.channel.send(switchFunctions.store(user, userName, switch, switchType))
        return
        

@bot.command(name="linear")
async def switchReturn(ctx):
    user, userName = getUsername(ctx)
    linears = databaseFunctions.getType("linear")
    text = returnList(userName, linears)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return


@bot.command(name="tactile")
async def switchReturn(ctx):
    user, userName = getUsername(ctx)

    text = returnList(userName, switches)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return


@bot.command(name="clicky")
async def switchReturn(ctx):
    user, userName = getUsername(ctx)

    text = returnList(userName, switches)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return


@bot.command(name="all")
async def switchReturn(ctx):
    user, userName = getUsername(ctx)

    text = returnList(userName, switches)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return


@bot.command(name="del")
async def deleteSwitch(ctx, switchName):
    user, userName = getUsername(ctx)
    removalMessage = switchFunctions.removeSwitch(user, switchName)

    text = returnList(userName, switches)
    await ctx.channel.send(removalMessage)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return
    

@bot.command(name="DELETE")
async def switchReturn(ctx):
    user = str(ctx.author).lower()
    text = switchFunctions.deleteAll(user)
    await ctx.channel.send(text)
    return


#Adds link to certain switch
@bot.command(name="aLink")
async def switchReturn(ctx, switchName, nameAndlink, link=None):
    user, userName = getUsername(ctx)
    linkAddResult = switchFunctions.addLink(user, userName, switchName, nameAndlink, link)
    text = returnList(userName, linkAddResult)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return

@bot.command(name="rLink")
async def switchReturn(ctx, switchName, store):
    user, userName = getUsername(ctx)
    linkAddResult = switchFunctions.removeLink(user, switchName, store)
    text = returnList(userName, linkAddResult)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return

@bot.command(name="DELETELinks")
async def switchReturn(ctx, switchName):
    user, userName = getUsername(ctx)
    linkAddResult = switchFunctions.delLinks(user, switchName)
    text = returnList(userName, linkAddResult)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return

@bot.command(name="allLinks")
async def allLinks(ctx, switchName):
    user, userName = getUsername(ctx)
    linkAddResult = switchFunctions.allLinks(user, switchName)
    text = returnList(userName, linkAddResult)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return

@bot.command(name="shop")
async def getStore(ctx, switchName, shop):
    user, userName = getUsername(ctx)
    linkAddResult = switchFunctions.getShop(user, switchName, shop)
    text = returnList(userName, linkAddResult)
    channel = bot.get_channel(1015931835525627904)
    await channel.send(embed=text)
    return

@bot.command(name="convert")
async def usaToNZD(ctx, currency, amount=None):
    rate = conversionRate(currency.upper())
    channel = bot.get_channel(1023194596177625128)
    if amount == None:
        #1 currency to NZD
        rate = round(1/rate, 2)
        await channel.send("$1 {currency} = ${rate} NZD".format(currency = currency.upper(), rate = str(rate)) ) 
    else:
        #NZD to currency
        rate = round(float(amount)/ rate, 2)
        await channel.send("${amount} {currency} = ${rate} NZD".format(currency = currency.upper(), rate = str(rate))) 
       



"""
implement invalid command handling
Implement empty string send for commands
"""

#Reusable functions

#gives username used in discord 
def getUsername(ctx):
    user = str(ctx.author).lower()
    userName = user.split("#")[0]
    return user, userName

#returns the switches in a text box
def returnList(user, switches):
    embed=discord.Embed(title=f"Switches for {user}",\
        description=switches,\
        #random color
        color=random.randint(0, 16777215))
    return embed


def conversionRate(country):
    url = 'https://v6.exchangerate-api.com/v6/87f9ce30a979b0a13acbb218/latest/NZD'
    response = requests.get(url)
    data = response.json()["conversion_rates"][country]
    return data


bot.run(TOKEN)
databaseFunctions