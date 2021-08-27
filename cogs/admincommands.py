import discord
import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
import time
from discord.ext import commands
import datetime
from datetime import datetime, timedelta, timezone
import asyncio
import random
import json
import re
from urllib.parse import quote_plus
from pathlib import Path
import sys
import locale
from num2words import num2words
import pymongo
import os
# import fuzzywuzzy (NEXT UPDATE)

cwd = Path(__file__).parents[0]
cwd = str(cwd)
default = "+"
status = [False, False, False, False]
statusdetails = [True, False, False, False]
efile = 'C:/Users/Hao/PycharmProjects/master/error logs'
dfile = 'C:/Users/Hao/PycharmProjects/master/dbinfo'
color = discord.Color.gold()  # apply later

def filterOnlyBots(member): return member.bot
def write_json(data, filename):
    with open(f"{cwd}/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)
def read_json(filename):
    with open(f"{cwd}/{filename}.json", "r") as file:
        data = json.load(file)
    return data
def community_report(ctx):
    guild = bot.get_guild(ctx.author.guild.id)
    online = 0
    idle = 0
    offline = 0
    dnd = 0
    for m in guild.members:
        if str(m.status) == "online":
            online += 1
        elif str(m.status) == "offline":
            offline += 1
        elif str(m.status) == "dnd":
            dnd += 1
        elif str(m.status) == "idle":
            idle += 1

    return online, idle, offline, dnd

async def cut(command, db): db["Total"][f"{command}"] += 1
async def cud(command, db): db["Daily"][f"{command}"] += 1
async def ctm(guild_id, db): db[str(guild_id)]["Total Messages"] += 1
async def ctc(guild_id, db): db[str(guild_id)]["Total Commands"] += 1
async def cs(guild_id, db, prefix): db[str(guild_id)]["Prefix"] = prefix
async def ci(guild_id, db, invite): db[str(guild_id)]["Invite"] = f"{invite}"
async def cmr(guild_id, db, role_id): db[str(guild_id)]["Mute Role"] = role_id
async def determine_prefix(bot, message):
    with open('serverdb.json', "r") as f:
        prefix = json.load(f)
    if str(message.guild.id) in prefix:
        if prefix[str(message.guild.id)]["Prefix"] is None:
            return default
        else:
            return prefix[str(message.guild.id)]["Prefix"]
    else:
        return default
async def udb(guild_id, db):
    if not str(guild_id) in db:
        db[str(guild_id)] = {}
        db[str(guild_id)]["Prefix"] = None
        db[str(guild_id)]["Invite"] = None
        db[str(guild_id)]["Mute Role"] = None
        db[str(guild_id)]["Total Messages"] = 0
        db[str(guild_id)]["Total Commands"] = 0
    else:
        return

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["currency"]

bot = Bot(command_prefix=determine_prefix, intents=discord.Intents().all(), owner_ids=[497903117241810945, 567487802900480000])
bot.remove_command('help')

@commands.command(aliases=["ac", "adminc", "ADMINC", "AC", "+", "AdminCommands", "Admincommands", "ADMINCOMMANDS"])
@commands.is_owner()
async def admincommands(ctx):
    with open('serverdb.json', 'r') as f:
        prefix = json.load(f)

    if str(ctx.author.guild.id) in prefix:
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None:
            theprefix = default
        else:
            theprefix = prefix[str(ctx.author.guild.id)]["Prefix"]
    else:
        theprefix = default

    await ctx.send('```json\n"ADMIN COMMANDS"```')
    await ctx.send(f"""```diff
Every indent is a argument
o = optional
# Grey means it is loading
- Red means it is under evaluation

`{theprefix}` is the prefix

+ Clear/Purge [arg]     |  Clear an amount of messages
+     Amount (Integer)
+ Change                |  Change the bots status
+ Exec [arg*]           |  Evaluate a piece code
+     Built in Python   
+ Load [arg*]           |  Load a cog
+     Cog Name          
+ Run                   |  Run the bot (after lockdown)
+ Reset                 |  Reset the daily command usage
+ Findprefix [arg]      |  Find a servers prefix
      Guild ID
+ Asay [arg*]           |  Make the bot say something
      Content
+ Cstocks [arg] [arg2]  |  Change a stock
      Stock
            Amount
+ DBinfo                |  Information about this database
+ Lockdown              |  Lock the bot down
+ Reload [arg*]         |  Reload a cog
+     Cog Name          
+ Status [arg (o)]      |  Status of the bot / cogs
+     Cog
+ Unload [arg*]         |  Unload a cog
+     Cog Name
```""")

@commands.command(aliases=["s", "S", "Status", "STATUS"])
@commands.is_owner()
async def status(ctx, arg=None):
    data = read_json("status")
    botworking, admincommands, adminchappen, misc, mischappen, moderation, moderationhappen, currency, currencyhappen = data["Bot Working"], data["Admin Cog"], data["Admin Cog Error"], data["Misc Cog"], data["Misc Cog Error"], data["Moderation Cog"], data['Moderation Cog Error'], data['Currency Cog'], data['Currency Cog Error']

    if admincommands is True:adminc = "+ admincommands.py"
    else:
        if adminchappen is True: adminc = "# admincommands.py"
        else: adminc = "- admincommands.py"
    if misc is True: misc2 = "+ misc.py"
    else:
        if mischappen is True: misc2 = "# misc.py"
        else: misc2 = "- misc.py"
    if moderation is True: modc = "+ moderation.py"
    else:
        if moderationhappen is True: modc = "# moderation.py"
        else: modc = "- moderation.py"
    if currency is True: cc = "+ currency.py"
    else:
        if currencyhappen is True: cc = "# currency.py"
        else: cc = "- currency.py"

    if botworking is True:
        if arg is None:
            await ctx.send("```diff\n+ 🟢 Bot is active```")
        else:
            if arg == "cogs" or arg == "Cogs" or arg == "cog" or arg == "Cog":
                await ctx.send(f"""```diff\n+ Green represents available\n- Red represents under evaluation\n# Grey represents an error or its loading\n\n{adminc}\n{misc2}\n{modc}\n{cc}\n\nOther Files\n\n+ commandusage.json\n+ serverdb.json\n+ status.json\n+ stocks.json\n+ mongodb://localhost:27017/```""")
                await ctx.send(f"""```ini\n[Refresh if needed]```""")
    else: await ctx.send("```diff\n- 🔴 Entire Bot is under WIP```")

@commands.command()
@commands.is_owner()
async def reset(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
    del db["Daily"]
    db["Daily"] = {
"Allroles": 0,
"Avatar": 0,
"Balance": 0,
"Ban": 0,
"Bon": 0,
"Botinfo": 0,
"Choose": 0,
"Commandlb": 0,
"Daily": 0,
"Date": 0,
"Deposit": 0,
"Dump": 0,
"Emojify": 0,
"Feelinglucky": 0,
"Flipcoin": 0,
"Gamble": 0,
"Give": 0,
"Google": 0,
"Guess": 0,
"Hello": 0,
"Help": 0,
"Invite": 0,
"Kick": 0,
"Membercount": 0,
"Mute": 0,
"Mystocks": 0,
"Nextupdate": 0,
"Num2Word": 0,
"Pat": 0,
"Pban": 0,
"Ping": 0,
"Say": 0,
"Serverinfo": 0,
"Setembedcolor": 0,
"Setmuterole": 0,
"Setprefix": 0,
"Simprate": 0,
"Stocks": 0,
"Taxcalc": 0,
"Tictactoe": 0,
"Timer": 0,
"Unban": 0,
"Unmute": 0,
"Uptime": 0,
"Userinfo": 0,
"Version": 0,
"War": 0,
"Withdraw": 0,
"IQrate":0,
"Luck":0
}
    with open('commandusage.json', 'w') as f:
        json.dump(db, f, indent=4, sort_keys=True)
    await ctx.send("```+ Reset daily command usage```")

@commands.command()
@commands.is_owner()
async def findprefix(ctx, guild):
    with open('serverdb.json', 'r') as f:
        db = json.load(f)
    if str(guild) in db:
        if db[str(guild)]["Prefix"] is None:
            sp = default
        else:
            sp = db[str(guild)]["Prefix"]
    else:
        sp = default
    await ctx.send(f"```({guild}) Server Prefix: {sp}```")

@commands.command(aliases=["as"])
@commands.is_owner()
async def asay(ctx, *, s=None):
    await ctx.send(f"{s}")

@commands.command()
@commands.is_owner()
async def cstocks(ctx, stock, new_amount:int):
    with open('stocks.json', 'r') as f:
        stocks = json.load(f)
    ca = stocks[f"{stock}"]["Current Amount"]
    stocks[f"{stock}"]["Previous Amount"] = ca
    stocks[f"{stock}"]["Current Amount"] = int(new_amount)
    with open('stocks.json', 'w') as f:
        json.dump(stocks, f, indent=4)

    await ctx.send(f"```+ Changed stock {stock} to {new_amount}```")

@commands.command()
@commands.is_owner()
async def dbinfo(ctx):
    col = db["currency"]

    await ctx.send(db.list_collection_names())
    await ctx.send(client.list_database_names())
    for x in col.find({}, {"_id": 0, "USER ID": 1, "USER":1, "Wallet":1,"Bank":1,"Bank Limit":1}):
        await ctx.send(x)

@commands.command()
@commands.is_owner()
async def finduser(ctx, arg:int):
    col = db["currency"]

    for x in col.find({"USER ID":arg}, {"_id": 0, "USER":1, "Wallet":1,"Bank":1,"Bank Limit":1}):
        await ctx.send(x)

@commands.command(aliases=["ua"])
@commands.is_owner()
async def useradd(ctx, arg:int, amount:int):
    col = db["currency"]
    a = []
    wallet = col.find_one({"USER ID": arg}, {"_id": 0, "Wallet": 1})["Wallet"]

    col.update_one({"USER ID": arg, "Wallet": wallet}, {"$set": {"Wallet": wallet + amount}})
    await ctx.send(f"```Added {amount} to {arg}```")

@commands.command(aliases=["ur"])
@commands.is_owner()
async def userremove(ctx, arg:int, amount:int):
    col = db["currency"]
    a = []
    wallet = col.find_one({"USER ID": arg}, {"_id": 0, "Wallet": 1})["Wallet"]

    col.update_one({"USER ID": arg, "Wallet": wallet}, {"$set": {"Wallet": wallet - amount}})
    await ctx.send(f"```Removed {amount} to {arg}```")

@commands.command()
@commands.is_owner()
async def dropdb(ctx):
    col = db["currency"]
    col.drop()
    await ctx.send("```DB: Currency has been removed```")

@commands.command()
@commands.is_owner()
async def dfile(ctx, arg):
    file = discord.File(f"C:/Users/Hao/PycharmProjects/master/{arg}", filename=f"{arg}")
    embed=discord.Embed()
    embed.set_image(url=f"attachment://{arg}")
    await ctx.send(file=file)

def setup(bot):
    bot.add_command(useradd)
    bot.add_command(userremove)
    bot.add_command(finduser)
    #bot.add_command(dropdb)
    bot.add_command(dfile)
    bot.add_command(dbinfo)
    bot.add_command(cstocks)
    bot.add_command(asay)
    bot.add_command(findprefix)
    bot.add_command(reset)
    bot.add_command(admincommands)
    bot.add_command(status)
