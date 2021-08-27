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
import typing
import random
import pymongo
from pymongo import collection
from collections import Counter
# import fuzzywuzzy (NEXT UPDATE)

cwd = str(Path(__file__).parents[0])
default = "+"
efile = 'C:/Users/Hao/PycharmProjects/master/error logs'
color = discord.Color.gold()  # apply later
pre = "⌬ "
custom_footer = "WIP"

coincord_file = 'https://cdn.discordapp.com/attachments/690681407256789012/879113682313957427/coincord.png'
orange_file = 'https://cdn.discordapp.com/attachments/690681407256789012/879113747476672572/orange.png'

#DATABASE
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["currency"]

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

async def cu(command, db):
    db["Total"][f"{command}"] += 1
    db["Daily"][f"{command}"] += 1
async def ctm(guild_id, db): db[str(guild_id)]["Total Messages"] += 1
async def cfish(user_id, db, type, amount): db[str(user_id)][str(type)] += amount
async def cl(user_id, db, league): db[str(user_id)]["League"] = league
async def ct(user_id, db, trophies): db[str(user_id)]["Trophies"] += trophies
async def ctc(guild_id, db): db[str(guild_id)]["Total Commands"] += 1
async def cs(guild_id, db, prefix): db[str(guild_id)]["Prefix"] = prefix
async def ci(guild_id, db, invite): db[str(guild_id)]["Invite"] = f"{invite}"
async def cmr(guild_id, db, role_id): db[str(guild_id)]["Mute Role"] = role_id
async def ud(user_id, db):
    if not str(user_id) in db:
        db[str(user_id)] = {}
        db[str(user_id)]["Daily"] = None
        db[str(user_id)]["Feeling Lucky"] = None
    else:
        return
async def lud(user_id, db, time):
    db[str(user_id)]["Daily"] = str(time)
async def luf(user_id, db, time):
    db[str(user_id)]["Feeling Lucky"] = str(time)

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
async def ufish(user_id, db):
    if not str(user_id) in db:
        db[str(user_id)] = {}
        db[str(user_id)]["Fish"],db[str(user_id)]["Shrimp"],db[str(user_id)]["Rare Fish"],db[str(user_id)]["Crab"],db[str(user_id)]["Squid"],db[str(user_id)]["Octopus"],db[str(user_id)]["Dolphin"],db[str(user_id)]["Blowfish"],db[str(user_id)]["Lobster"],db[str(user_id)]["Whale"],db[str(user_id)]["Shark"] = 0,0,0,0,0,0,0,0,0,0,0
    else:
        return
async def uleague(user_id, db):
    if not str(user_id) in db:
        db[str(user_id)] = {}
        db[str(user_id)]["League"] = None
        db[str(user_id)]["Trophies"] = 0
    else:
        return
async def uinv(user_id, db):
    if not str(user_id) in db:
        db[str(user_id)] = {}
    else:
        return

bot = Bot(command_prefix=determine_prefix, intents=discord.Intents().all(), owner_ids=[497903117241810945, 567487802900480000])
bot.remove_command('help')

"""ECONOMY"""
@commands.command(aliases=["deposit", "DEP", "Dep", "dEP", "DEPOSIT", "Deposit", "dEPOSIT"])
@commands.is_owner()
async def dep(ctx, arg):
    with open('commandusage.json', "r") as f:
        cdb = json.load(f)
        await cu("Deposit", cdb)
        with open('commandusage.json', "w") as f: json.dump(cdb, f, indent=4, sort_keys=True)
    locale.setlocale(locale.LC_ALL, 'en_US')
    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
    if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    if arg == "all" or arg == "max":
        if bank == bankl:
            embed = discord.Embed(description="Your bank is full", color=color)
        elif wallet == 0:
            embed = discord.Embed(description="You have nothing to deposit", color=color)
        else:
            if bank != 0:
                if bankl - bank > wallet:
                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - wallet}})
                    col.update_one({"USER ID": ctx.author.id, "Bank": bank}, {"$set": {"Bank": bank + wallet}})

                    embed = discord.Embed(
                        description=f"Deposited **{pre}{locale.format_string('%d', wallet, grouping=True)}**",
                        color=color)
                else:
                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - (bankl - bank)}})
                    col.update_one({"USER ID": ctx.author.id, "Bank": bank}, {"$set": {"Bank": bank + (bankl - bank)}})
                    embed = discord.Embed(
                        description=f"Deposited **{pre}{locale.format_string('%d', bankl - bank, grouping=True)}**",
                        color=color)
            else:
                if bankl > wallet:
                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - wallet}})
                    col.update_one({"USER ID": ctx.author.id, "Bank": bank}, {"$set": {"Bank": bank + wallet}})

                    embed = discord.Embed(
                        description=f"Deposited **{pre}{locale.format_string('%d', wallet, grouping=True)}**",
                        color=color)
                else:
                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - bankl}})
                    col.update_one({"USER ID": ctx.author.id, "Bank": bank}, {"$set": {"Bank": bank + bankl}})

                    embed = discord.Embed(
                        description=f"Deposited **{pre}{locale.format_string('%d', bankl, grouping=True)}**",
                        color=color)
        await ctx.send(embed=embed)
    else:
        if int(arg) > wallet:
            embed = discord.Embed(
                description=f"You only have **{pre}{locale.format_string('%d', wallet, grouping=True)}** in your wallet",
                color=color)
        elif int(arg) > bankl + bank:
            embed = discord.Embed(
                description=f"Your bank can only hold **{pre}{locale.format_string('%d', bankl, grouping=True)}**",
                color=color)
        elif bank == bankl:
            embed = discord.Embed(description="Your bank is full.", color=color)
        elif int(arg) == 0:
            embed = discord.Embed(description=f"Number must be greater than **{pre}0**", color=color)
        else:
            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - int(arg)}})
            col.update_one({"USER ID": ctx.author.id, "Bank": bank}, {"$set": {"Bank": bank + int(arg)}})

            embed = discord.Embed(
                description=f"Deposited **{pre}{locale.format_string('%d', int(arg), grouping=True)}**",
                color=color)
        await ctx.send(embed=embed)
@commands.command(aliases=["with", "WTIH", "With", "wITH", "WITHDRAW", "Withdraw", "wITHDRAW"])
@commands.is_owner()
async def withdraw(ctx, arg):
    with open('commandusage.json', "r") as f:
        cdb = json.load(f)
        await cu("Withdraw", cdb)
        with open('commandusage.json', "w") as f: json.dump(cdb, f, indent=4, sort_keys=True)
    locale.setlocale(locale.LC_ALL, 'en_US')
    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
    if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    if arg == "all" or arg == "max":
        if bank == 0:
            embed = discord.Embed(description="You have nothing to withdraw", color=color)
        else:
            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + bank}})
            col.update_one({"USER ID": ctx.author.id, "Bank": bank}, {"$set": {"Bank": bank - bank}})
            embed = discord.Embed(description=f"Withdrawn **{pre}{locale.format_string('%d', bank, grouping=True)}**",
                                  color=color)
    else:
        if int(arg) > bank:
            embed = discord.Embed(
                description=f"You only have **{pre}{locale.format_string('%d', bank, grouping=True)}** in your bank",
                color=color)
        elif int(arg) == 0:
            embed = discord.Embed(description=f"Needs to be a number greater than **{pre}0**", color=color)
        else:
            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + int(arg)}})
            col.update_one({"USER ID": ctx.author.id, "Bank": bank}, {"$set": {"Bank": bank - int(arg)}})

            embed = discord.Embed(
                description=f"Withdrawn **{pre}{locale.format_string('%d', int(arg), grouping=True)}**",
                color=color)
    await ctx.send(embed=embed)
@commands.command(aliases=["bal", "BAL", "Bal", "bAL"])
@commands.is_owner()
async def balance(ctx, user: discord.Member=None):
    with open('commandusage.json', "r") as f:
        cdb = json.load(f)
        await cu("Balance", cdb)
        with open('commandusage.json', "w") as f: json.dump(cdb, f, indent=4, sort_keys=True)
    locale.setlocale(locale.LC_ALL, 'en_US')
    if user is None:
        col = db["currency"]
        a = []
        for x in col.find({}, {"_id": 0, "USER ID": 1}):a.append(x)
        if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
        userr = col.find_one({"USER ID":ctx.author.id}, {"_id":0, "USER":1})["USER"]
        if userr != str(ctx.author):col.update_one({"USER ID": ctx.author.id, "USER":userr}, {"$set": {"USER": str(ctx.author)}})
        wallet = col.find_one({"USER ID":ctx.author.id}, {"_id":0,"Wallet":1})["Wallet"]
        bank = col.find_one({"USER ID":ctx.author.id}, {"_id":0,"Bank":1})["Bank"]
        bankl = col.find_one({"USER ID":ctx.author.id}, {"_id":0,"Bank Limit":1})["Bank Limit"]

        if ctx.author.color == discord.Color.from_rgb(0, 0, 0):
            c = discord.Color.from_rgb(47, 49, 54)
        else:
            c = ctx.author.color
        embed = discord.Embed(description=f'**Wallet**: {pre}{locale.format_string("%d", wallet, grouping=True)}\n**Bank**: {pre}{locale.format_string("%d", bank, grouping=True)} / {locale.format_string("%d", bankl, grouping=True)} **(`{(bank/bankl)*100:.1f}%`)**\n**Total**: {pre}{locale.format_string("%d", wallet+bank, grouping=True)}', color=c)
        embed.set_author(name=f"{ctx.author.name}'s balance", icon_url=ctx.author.avatar)
        embed.set_footer(text=f"{custom_footer}")
        await ctx.send(embed=embed)
    else:
        col = db["currency"]
        a = []
        for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
        if {"USER ID": user.id} not in a:col.insert_one({"USER ID":user.id,"USER":str(user),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
        wallet = col.find_one({"USER ID": user.id}, {"_id": 0, "Wallet": 1})["Wallet"]
        bank = col.find_one({"USER ID": user.id}, {"_id": 0, "Bank": 1})["Bank"]
        bankl = col.find_one({"USER ID": user.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

        if user.color == discord.Color.from_rgb(0, 0, 0):
            c = discord.Color.from_rgb(47, 49, 54)
        else:
            c = user.color
        embed = discord.Embed(description=f'**Wallet**: {pre}{locale.format_string("%d", wallet, grouping=True)}\n**Bank**: {pre}{locale.format_string("%d", bank, grouping=True)} / {locale.format_string("%d", bankl, grouping=True)} **(`{(bank/bankl)*100:.1f}%`)**\n**Total**: {pre}{locale.format_string("%d", wallet + bank, grouping=True)}', color = c)
        embed.set_author(name=f"{user.name}'s balance", icon_url=user.avatar)
        embed.set_footer(text=f"{custom_footer}")
        await ctx.send(embed=embed)
@commands.command(aliases=["share", "Give", "Share", "GIVE", "SHARE"])
@commands.is_owner()
async def give(ctx, user: discord.Member, amount:int):
    with open('commandusage.json', "r") as f:
        cdb = json.load(f)
        await cu("Give", cdb)
        with open('commandusage.json', "w") as f: json.dump(cdb, f, indent=4, sort_keys=True)
    locale.setlocale(locale.LC_ALL, 'en_US')
    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    if {"USER ID": user.id} not in a: col.insert_one({"USER ID": user.id, "USER": str(user), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
    if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]
    mwallet = col.find_one({"USER ID": user.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    mbank = col.find_one({"USER ID": user.id}, {"_id": 0, "Bank": 1})["Bank"]
    mbankl = col.find_one({"USER ID": user.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    if ctx.message.author == user:
        embed = discord.Embed(description="You can't send money to yourself", color=color)
    elif amount > wallet:
        embed = discord.Embed(description=f"You only have **{pre}{locale.format_string('%d', wallet, grouping=True)}** in your wallet", color=color)
    elif amount == 0:
        embed = discord.Embed(description=f"Sending someone **{pre}0** is not necessary", color=color)
    else:
        col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - amount}})
        col.update_one({"USER ID": user.id, "Wallet": mwallet}, {"$set": {"Wallet": mwallet + amount}})
        embed = discord.Embed(description=f'You gave {user.mention} **{pre}{locale.format_string("%d", amount, grouping=True)}**. Now you have **{pre}{locale.format_string("%d", wallet-amount, grouping=True)}** and they have **{pre}{locale.format_string("%d", mwallet+amount, grouping=True)}**.', color=color)
        embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def top(ctx):
    locale.setlocale(locale.LC_ALL, 'en_US')
    col = db["currency"]
    cool = {}
    humans = [m for m in ctx.author.guild.members if not m.bot]
    for a in humans:
        for x in col.find({"USER ID":a.id}, {"_id": 0, "USER":1, "Wallet": 1}):
            if x["Wallet"] == 0:pass
            elif x["Wallet"] <= 1000: pass
            else:cool[x["USER"]] = x["Wallet"]
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    k = Counter(cool)
    high = k.most_common(10)
    place = 1
    thelist = []
    nameplace = None
    name = ctx.author
    emoji = ""
    for i in high:
        if place == 10:
            thelist.append(f"{place}. {locale.format_string('%d', i[1], grouping=True).ljust(20)}{i[0].ljust(1)}")
        else:
            thelist.append(f"{place}.  {locale.format_string('%d', i[1], grouping=True).ljust(20)}{i[0].ljust(1)}")
        if i[0] == str(ctx.author):
            if place == 1:
                nameplace = f"{place}st"
                emoji = "🥇"
            elif place == 2:
                nameplace = f"{place}nd"
                emoji = "🥈"
            elif place == 3:
                nameplace = f"{place}rd"
                emoji = "🥉"
            else:
                nameplace = f"{place}th"
                emoji = ""
        place += 1
    if nameplace != None:
        embed = discord.Embed(title=f"Top 10 Richest Users in **{ctx.author.guild}**",
                              description=f"```md\n#   {'Amount'.ljust(20)}{'Name'.ljust(1)}\n" + "\n".join(a for a in thelist) + "```",
                              color=color)
        embed.set_author(name="The Revolutionary",
                         icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
        embed.set_thumbnail(url=ctx.author.guild.icon)
        embed.set_footer(text=f"You are {nameplace}{emoji}!")
    else:
        embed = discord.Embed(title=f"Top 10 Richest Users in **{ctx.author.guild}**",
                              description=f"```md\n#   {'Amount'.ljust(20)}{'Name'.ljust(1)}\n" + "\n".join(
                                  a for a in thelist) + "```",
                              color=color)
        embed.set_author(name="The Revolutionary",
                         icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
        embed.set_thumbnail(url=ctx.author.guild.icon)
        embed.set_footer(text=f"You have {pre}{wallet}")
    await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def toptrophies(ctx):
    locale.setlocale(locale.LC_ALL, 'en_US')
    cool2 = {}
    humans = [m for m in ctx.author.guild.members if not m.bot]
    with open('leagues.json', "r") as f:
        l = json.load(f)
    for a in humans:
        if str(ctx.author.id) in l:
            cool2[f"{ctx.author}"] = l[str(ctx.author.id)]['Trophies']
    z = Counter(cool2)
    high2 = z.most_common(10)
    place2 = 1
    thelist2 = []
    for y in high2:
        if place2 == 10:
            thelist2.append(f"{place2}.  {locale.format_string('%d', y[1], grouping=True).ljust(15)}{y[0].ljust(10)}")

        else:
            thelist2.append(f"{place2}.   {locale.format_string('%d', y[1], grouping=True).ljust(15)}{y[0].ljust(10)}")
        place2 += 1
    embed2 = discord.Embed(title=f"Top 10 User Trophies in **{ctx.author.guild}**",
                           description=f"```md\n#    {'Trophies'.ljust(15)}{'Name'.ljust(10)}\n" + "\n".join(
                               a for a in thelist2) + "```",
                           color=color)
    embed2.set_author(name="The Revolutionary",
                      icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
    embed2.set_thumbnail(url='https://cdn.discordapp.com/attachments/690681407256789012/879794231156277308/751701583414165516.png')
    await ctx.send(embed=embed2)
@commands.command()
@commands.is_owner()
async def profile(ctx, member:discord.Member=None):
    locale.setlocale(locale.LC_ALL, 'en_US')
    if member is None:
        col = db["currency"]
        a = []
        for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
        if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
        userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
        if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
        wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
        bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
        bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]
        with open('fish.json', 'r') as f:
            fish = json.load(f)
        if str(ctx.author.id) not in fish:
            await ufish(ctx.author.id, fish)
        with open('fish.json', 'w') as f:
            json.dump(fish, f, indent=4)
        final = []
        for a in fish[str(ctx.author.id)]:
            if fish[str(ctx.author.id)][str(a)] != 0:
                if a == "Whale":
                    emoji = "whale2"
                elif a == "Rare Fish":
                    emoji = "tropical_fish"
                else:
                    emoji = a.lower()
                final.append(f"**{a}** :{emoji}: ─ {fish[str(ctx.author.id)][a]}")
        with open('leagues.json', "r") as f:
            l = json.load(f)
            if str(ctx.author.id) not in l:
                await uleague(str(ctx.author.id), l)
                await cl(str(ctx.author.id), l, league="🔰 Challenger 🔰")
            with open('leagues.json', "w") as f: json.dump(l, f, indent=4, sort_keys=True)
        embed=discord.Embed(description=f"**<:leaguetrophy:879793117555998790> {l[str(ctx.author.id)]['Trophies']} ─ {l[str(ctx.author.id)]['League']}**",color=color)
        embed.add_field(name="Coins",value=f'**Wallet:** {pre}{locale.format_string("%d", wallet, grouping=True)}\n**Bank:** {pre}{locale.format_string("%d", bank, grouping=True)}')
        embed.add_field(name="Fish", value="\n".join(b for b in final), inline=False)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
        embed.set_thumbnail(url=ctx.author.avatar)
        await ctx.send(embed=embed)




"""SHOP"""
@commands.command()
@commands.is_owner()
async def shop(ctx, arg=None):
    if arg is None:
        embed=discord.Embed(title="Shop", description=f"<:legendarybox:880229601043963905> **Legendary Box ─ [{pre}2,500,000](https://google.com)**\nVery rare items inside",color=color)
        await ctx.send(embed=embed)
    else:
        with open('inventory.json', 'r') as f:
            idb = json.load(f)
        if arg.lower() == "legendary" or arg.lower() == "legendarybox" or arg.lower() == "lbox":
            if idb[str(ctx.author.id)]["Legendary Box"] == 0:
                embed = discord.Embed(title="Legendary Box",description=F"Very rare items inside\n\n**BUY ─ [{pre}2,500,000](https://google.com)**\n**SELL** ─ Cannot be sold",color=color)
            else:
                embed = discord.Embed(title=f"Legendary Box **({idb[str(ctx.author.id)]['Legendary Box']})**",description=F"Very rare items inside\n\n**BUY ─ [{pre}2,500,000](https://google.com)**\n**SELL** ─ Cannot be sold",color=color)
            embed.add_field(name="Possible Items", value="""
`Trophy`, `Shark`, `Lobster`    
""")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/690681407256789012/880238375163007026/573151905513996298.png')
            await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def buy(ctx, arg, amount:int=None):
    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
    if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]
    with open('inventory.json', 'r') as f:
        idb = json.load(f)
    if str(ctx.author.id) not in idb:
        await uinv(str(ctx.author.id), idb)
        idb[str(ctx.author.id)]["Legendary Box"] = 0
    with open('inventory.json', 'w') as f:
        json.dump(idb, f, indent=4)
    if arg.lower() == "legendary" or arg.lower() == "legendarybox" or arg.lower() == "lbox":
        if amount is None:
            if wallet < 2500000:
                embed=discord.Embed(description=f"You don't have enough for **a Legendary Box <:legendarybox:880229601043963905>** (`{pre}2,500,000`)")
            else:
                idb[str(ctx.author.id)]["Legendary Box"] += 1
                with open('inventory.json', 'w') as f:
                    json.dump(idb, f, indent=4)
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet-2500000}})
                embed = discord.Embed(description=f"You bought **a Legendary Box <:legendarybox:880229601043963905>** for `{pre}2,500,000`",color=color)
                embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
        else:
            if wallet < 2500000*amount:
                embed=discord.Embed(description=f"You don't have enough for **{amount} Legendary Boxes <:legendarybox:880229601043963905>** (`{pre}{locale.format_string('%d', 2500000*amount, grouping=True)}`)")
            else:
                idb[str(ctx.author.id)]["Legendary Box"] += amount
                with open('inventory.json', 'w') as f:
                    json.dump(idb, f, indent=4)
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - 2500000*amount}})
                embed = discord.Embed(description=f'You bought **{amount} Legendary Boxes <:legendarybox:880229601043963905>** for `{pre}{locale.format_string("%d", amount*2500000, grouping=True)}`',color=color)
                embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
            await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def use(ctx, arg, amount:int=None):
    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
    if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]
    with open('inventory.json', 'r') as f:
        idb = json.load(f)
    with open('fish.json', 'r') as f:
        fish = json.load(f)
    with open('leagues.json', "r") as f:
        l = json.load(f)
        if str(ctx.author.id) not in l:
            await uleague(str(ctx.author.id), l)
            await cl(str(ctx.author.id), l, league="🔰 Challenger 🔰")
        with open('leagues.json', "w") as f: json.dump(l, f, indent=4, sort_keys=True)
    if arg.lower() == "legendary" or arg.lower() == "legendarybox" or arg.lower() == "lbox":
        if amount is None:
            if idb[str(ctx.author.id)]["Legendary Box"] == 0:
                embed=discord.Embed(description=f"You have **no Legendary Boxes <:legendarybox:880229601043963905>**",color=color)
                await ctx.send(embed=embed)
            else:
                idb[str(ctx.author.id)]["Legendary Box"] -= 1
                with open('inventory.json', 'w') as f:
                    json.dump(idb, f, indent=4)
                choice = random.randint(1, 3)
                trophy = random.randint(10, 100)
                famount = random.randint(1, 10)
                coins = random.randint(55555, 300000)
                embed = discord.Embed(description=f'Opening **1 Legendary Box <:legendarybox:880229601043963905>...**',color=color)
                message = await ctx.reply(embed=embed)
                time.sleep(2)
                item = ""
                if choice == 1:
                    item = f"**<:leaguetrophy:879793117555998790> Trophy ─ `{trophy}`**"
                    await ct(str(ctx.author.id), l, trophies=trophy)
                elif choice == 2:
                    item = f"**:shark: Shark ─ `{famount}`**"
                    if str(ctx.author.id) not in fish:
                        await ufish(ctx.author.id, fish)
                    await cfish(ctx.author.id, fish, type="Shark", amount=famount)
                    with open('fish.json', 'w') as f:
                        json.dump(fish, f, indent=4)
                else:
                    item = f"**:lobster: Lobster ─ `{famount}`**"
                    if str(ctx.author.id) not in fish:
                        await ufish(ctx.author.id, fish)
                    await cfish(ctx.author.id, fish, type="Lobster", amount=famount)
                    with open('fish.json', 'w') as f:
                        json.dump(fish, f, indent=4)
                embed2 = discord.Embed(title=f"Box Contents",
                                       description=f"**{pre}{locale.format_string('%d', coins, grouping=True)}**\n\n{item}", color=color)
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + coins}})
                await message.edit(embed=embed2)
                if l[str(ctx.author.id)]["Trophies"] + trophy >= 250 and l[str(ctx.author.id)]["Trophies"] + trophy < 500 and "Novice" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
                    await cl(str(ctx.author.id), l, league="🛡️ Novice Tier 🛡️")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 500 and l[str(ctx.author.id)]["Trophies"] + trophy < 1000 and "Gold" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
                    await cl(str(ctx.author.id), l, league="🔱 Gold Tier 🔱")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 1000 and l[str(ctx.author.id)]["Trophies"] + trophy < 2000 and "Purple Dragon" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
                    await cl(str(ctx.author.id), l, league="⚜️ Purple Dragon Tier ⚜️")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 2000 and l[str(ctx.author.id)]["Trophies"] + trophy < 3000 and "Diamond" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
                    await cl(str(ctx.author.id), l, league="💎 Diamond Tier 💎")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 3000 and l[str(ctx.author.id)]["Trophies"] + trophy < 4500 and "Master" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
                    await cl(str(ctx.author.id), l, league="⚔️ Master Tier ⚔️")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 4500 and l[str(ctx.author.id)]["Trophies"] + trophy < 5000 and "Legendary" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
                    await cl(str(ctx.author.id), l, league="🃏 Legendary Tier 🃏")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 5000 and "The Best of the Best" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
                    await cl(str(ctx.author.id), l, league="🏴‍☠️ The Best of the Best 🏴‍☠️")
                with open('leagues.json', 'w') as f:
                    json.dump(l, f, indent=4)
        else:
            if idb[str(ctx.author.id)]["Legendary Box"] < amount:
                embed=discord.Embed(description=f"You do not have **{amount} Legendary Boxes <:legendarybox:880229601043963905>**. You have `{idb[str(ctx.author.id)]['Legendary Box']}`", color=color)
                await ctx.send(embed=embed)
            else:
                idb[str(ctx.author.id)]["Legendary Box"] -= amount
                with open('inventory.json', 'w') as f:
                    json.dump(idb, f, indent=4)
                choice = random.randint(1, 3)
                trophy = random.randint(10*amount, 100*amount)
                famount = random.randint(1*amount, 10*amount)
                coins = random.randint(55555*amount, 300000*amount)
                embed = discord.Embed(description=f'Opening **{amount} Legendary Boxes <:legendarybox:880229601043963905>...**',color=color)
                message = await ctx.reply(embed=embed)
                time.sleep(2)
                if choice == 1:
                    item = f"**<:leaguetrophy:879793117555998790> Trophy ─ `{trophy}`**"
                    await ct(str(ctx.author.id), l, trophies=trophy)
                elif choice == 2:
                    item = f"**:shark: Shark ─ `{famount}`**"
                    if str(ctx.author.id) not in fish:
                        await ufish(ctx.author.id, fish)
                    await cfish(ctx.author.id, fish, type="Shark", amount=famount)
                    with open('fish.json', 'w') as f:
                        json.dump(fish, f, indent=4)
                else:
                    item = f"**:lobster: Lobster ─ `{famount}`**"
                    if str(ctx.author.id) not in fish:
                        await ufish(ctx.author.id, fish)
                    await cfish(ctx.author.id, fish, type="Lobster", amount=famount)
                    with open('fish.json', 'w') as f:
                        json.dump(fish, f, indent=4)
                embed2 = discord.Embed(title=f"Box Contents",description=f"**{pre}{locale.format_string('%d', coins, grouping=True)}**\n\n{item}", color=color)
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet + coins}})
                await message.edit(embed=embed2)
                if l[str(ctx.author.id)]["Trophies"] + trophy >= 250 and l[str(ctx.author.id)]["Trophies"] + trophy < 500 and "Novice" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
                    await cl(str(ctx.author.id), l, league="🛡️ Novice Tier 🛡️")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 500 and l[str(ctx.author.id)]["Trophies"] + trophy < 1000 and "Gold" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
                    await cl(str(ctx.author.id), l, league="🔱 Gold Tier 🔱")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 1000 and l[str(ctx.author.id)]["Trophies"] + trophy < 2000 and "Purple Dragon" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
                    await cl(str(ctx.author.id), l, league="⚜️ Purple Dragon Tier ⚜️")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 2000 and l[str(ctx.author.id)]["Trophies"] + trophy < 3000 and "Diamond" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
                    await cl(str(ctx.author.id), l, league="💎 Diamond Tier 💎")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 3000 and l[str(ctx.author.id)]["Trophies"] + trophy < 4500 and "Master" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
                    await cl(str(ctx.author.id), l, league="⚔️ Master Tier ⚔️")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 4500 and l[str(ctx.author.id)]["Trophies"] + trophy < 5000 and "Legendary" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
                    await cl(str(ctx.author.id), l, league="🃏 Legendary Tier 🃏")
                elif l[str(ctx.author.id)]["Trophies"] + trophy >= 5000 and "The Best of the Best" not in l[str(ctx.author.id)]["League"]:
                    await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
                    await cl(str(ctx.author.id), l, league="🏴‍☠️ The Best of the Best 🏴‍☠️")
                with open('leagues.json', 'w') as f:
                    json.dump(l, f, indent=4)

@commands.command()
@commands.is_owner()
async def inventory(ctx):
    with open('inventory.json', 'r') as f:
        json.load(f)






"""LEAGUES"""
@commands.command()
@commands.is_owner()
async def leagues(ctx):
    with open('leagues.json', "r") as f:
        l = json.load(f)
        if str(ctx.author.id) not in l:
            await uleague(str(ctx.author.id), l)
            await cl(str(ctx.author.id), l, league="🔰 Challenger 🔰")
        with open('leagues.json', "w") as f: json.dump(l, f, indent=4, sort_keys=True)
    embed=discord.Embed(title="Leagues", description=f"<:leaguetrophy:879793117555998790> **0 ─ :beginner: Challenger Tier :beginner:**\n<:leaguetrophy:879793117555998790> **250 ─ :shield: Novice Tier :shield:**\n<:leaguetrophy:879793117555998790> **500 ─ :trident: Gold Tier :trident:**\n<:leaguetrophy:879793117555998790> **1000 ─ :fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**\n<:leaguetrophy:879793117555998790> **2000 ─ :gem: Diamond Tier :gem:**\n<:leaguetrophy:879793117555998790> **3000 ─ :crossed_swords: Master Tier :crossed_swords:**\n<:leaguetrophy:879793117555998790> **4500 ─ :black_joker: Legendary Tier :black_joker:**\n<:leaguetrophy:879793117555998790> **5000+ ─ :pirate_flag: The Best of the Best :pirate_flag:**\n<:leaguetrophy:879793117555998790> **???? ─ <:empty:880143730076688495> ???? <:empty:880143730076688495>**",color=color)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/690681407256789012/879794231156277308/751701583414165516.png')
    embed.set_footer(text=f"Your league: {l[str(ctx.author.id)]['League']}")
    await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def freetrophy(ctx):
    with open('leagues.json', "r") as f:
        l = json.load(f)
        if str(ctx.author.id) not in l:
            await uleague(str(ctx.author.id), l)
            await cl(str(ctx.author.id), l, league="🔰 Challenger Tier 🔰")
        with open('leagues.json', "w") as f: json.dump(l, f, indent=4, sort_keys=True)
    await ctx.send("You found `250` **Trophies** <:leaguetrophy:879793117555998790>!")
    if l[str(ctx.author.id)]["Trophies"]+250 >= 250 and l[str(ctx.author.id)]["Trophies"]+250 < 500 and "Novice" not in l[str(ctx.author.id)]["League"]:
        await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
        await cl(str(ctx.author.id),l, league="🛡️ Novice Tier 🛡️")
    elif l[str(ctx.author.id)]["Trophies"]+250 >= 500 and l[str(ctx.author.id)]["Trophies"]+250 < 1000 and "Gold" not in l[str(ctx.author.id)]["League"]:
        await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
        await cl(str(ctx.author.id), l, league="🔱 Gold Tier 🔱")
    elif l[str(ctx.author.id)]["Trophies"]+250 >= 1000 and l[str(ctx.author.id)]["Trophies"]+250 < 2000 and "Purple Dragon" not in l[str(ctx.author.id)]["League"]:
        await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
        await cl(str(ctx.author.id), l, league="⚜️ Purple Dragon Tier ⚜️")
    elif l[str(ctx.author.id)]["Trophies"]+250 >= 2000 and l[str(ctx.author.id)]["Trophies"]+250 < 3000 and "Diamond" not in l[str(ctx.author.id)]["League"]:
        await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
        await cl(str(ctx.author.id), l, league="💎 Diamond Tier 💎")
    elif l[str(ctx.author.id)]["Trophies"]+250 >= 3000 and l[str(ctx.author.id)]["Trophies"]+250 < 4500 and "Master" not in l[str(ctx.author.id)]["League"]:
        await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
        await cl(str(ctx.author.id), l, league="⚔️ Master Tier ⚔️")
    elif l[str(ctx.author.id)]["Trophies"]+250 >= 4500 and l[str(ctx.author.id)]["Trophies"]+250 < 5000 and "Legendary" not in l[str(ctx.author.id)]["League"]:
        await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
        await cl(str(ctx.author.id), l, league="🃏 Legendary Tier 🃏")
    elif l[str(ctx.author.id)]["Trophies"]+250 >= 5000 and "The Best of the Best" not in l[str(ctx.author.id)]["League"]:
        await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
        await cl(str(ctx.author.id), l, league="🏴‍☠️ The Best of the Best 🏴‍☠️")
    await ct(str(ctx.author.id), l, trophies=250)
    with open('leagues.json', 'w') as f:
        json.dump(l, f, indent=4)






"""STOCKS"""
@commands.command(aliases=["stocks"])
@commands.is_owner()
async def stock(ctx, stock=None, action=None, amount=None):
    with open('commandusage.json', "r") as f:
        cdb = json.load(f)
        await cu("Stocks", cdb)
        with open('commandusage.json', "w") as f: json.dump(cdb, f, indent=4, sort_keys=True)
    locale.setlocale(locale.LC_ALL, 'en_US')
    with open('stocks.json', 'r') as f: stocks = json.load(f)

    with open('serverdb.json', "r") as f: prefix = json.load(f)
    if str(ctx.author.guild.id) in prefix:
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None: theprefix = default
        else: theprefix = prefix[str(ctx.author.guild.id)]["Prefix"]
    else: theprefix = default

    if stock is None:
        cca = stocks["Coincord"]["Current Amount"]
        cpa = stocks["Coincord"]["Previous Amount"]
        oca = stocks["Orange"]["Current Amount"]
        opa = stocks["Orange"]["Previous Amount"]
        if cca > cpa:
            if cca >= cpa * 2:
                ec = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca-cpa)/cpa*100:.2f}%)`**'
            else:
                ec = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca-cpa)/cpa*100:.2f}%)`**'
        elif cca == cpa:
            ec = f'**No Change** [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
        else:
            ec = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▼ {pre}{locale.format_string("%d", cpa-cca, grouping=True)} `(▼ {(cpa-cca)/cpa*100:.2f}%)`**'

        if oca > opa:
            if oca >= opa * 2:
                oc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca -opa, grouping=True)} `(▲ {(oca-opa)/opa*100:.2f}%)`**'
            else:
                oc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca-opa)/opa*100:.2f}%)`**'
        elif stocks["Coincord"]["Current Amount"] == stocks["Orange"]["Previous Amount"]:
            oc = f'**No Change** [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
        else:
            oc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▼ {pre}{locale.format_string("%d", opa-oca, grouping=True)} `(▼ {(opa-oca)/opa*100:.2f}%)`**'
        embed=discord.Embed(title="Available Stocks", color=color)
        embed.add_field(name="Coincord :coin:", value=f'{ec}\nA beautiful coin. Pretty useless, but they might be worth a fortune', inline=False)
        embed.add_field(name="Orange :tangerine:", value=f'{oc}\nA fresh orange orange. You can use it to flex to your friends.', inline=False)
        mview = stockselect(timeout=15)
        out = await ctx.send(f"```yaml\nSyntax: {theprefix}stocks [Choice] [Buy/Sell] [Amount]\n\nTo view your current stocks: {theprefix}mystocks\n\nStocks last reset on [{stocks['Reset']}]```",embed=embed, file=None, view=mview)
        mview.user = ctx.author.id
        mview.response = out
    else:
        if stock.lower() == "coincord" or stock.lower() == "cc":
            if action is None:
                pass
            else:
                col = db["currency"]
                a = []
                for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
                if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
                wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
                bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
                bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]
                if amount is None:
                    if action.lower() == "buy":
                        if wallet < stocks["Coincord"]["Current Amount"]: embed = discord.Embed(description=f"You don't have enough for **a coin :coin:** (`{pre}{locale.format_string('%d', stocks['Coincord']['Current Amount'], grouping=True)}`)", color=color)
                        else:
                            if str(ctx.author.id) not in stocks["Coincord"]: stocks["Coincord"][str(ctx.author.id)] = 1
                            else: stocks["Coincord"][str(ctx.author.id)] += 1

                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - stocks["Coincord"]["Current Amount"]}})

                            with open('stocks.json', 'w') as f: json.dump(stocks, f, indent=4)
                            embed = discord.Embed(description=f"You bought **a coin :coin:** for `{pre}{locale.format_string('%d', stocks['Coincord']['Current Amount'], grouping=True)}`",color=color)
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if str(ctx.author.id) not in stocks["Coincord"]: embed = discord.Embed(description="You have no coins :coin:",color=color)
                        else:
                            stocks["Coincord"][str(ctx.author.id)] -= 1

                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet + stocks["Coincord"]["Current Amount"]}})

                            with open('stocks.json', 'w') as f: json.dump(stocks, f, indent=4)
                            embed = discord.Embed(description=f":tada: You sold **a coin :coin:** and got `{pre}{locale.format_string('%d', stocks['Coincord']['Current Amount'], grouping=True)}`",color=color)
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                else:
                    if action.lower() == "buy":
                        if wallet < stocks["Coincord"]["Current Amount"] * int(amount): embed = discord.Embed(description=f"You don't have enough for **{amount} coins :coin:** (`{pre}{locale.format_string('%d', stocks['Coincord']['Current Amount']*int(amount), grouping=True)}`)", color=color)
                        else:
                            if str(ctx.author.id) not in stocks["Coincord"]: stocks["Coincord"][str(ctx.author.id)] = int(amount)
                            else: stocks["Coincord"][str(ctx.author.id)] += int(amount)

                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - stocks["Coincord"]["Current Amount"]*int(amount)}})

                            with open('stocks.json', 'w') as f:json.dump(stocks, f, indent=4)

                            embed=discord.Embed(description=f"You bought **{amount} coins :coin:** for `{pre}{locale.format_string('%d', stocks['Coincord']['Current Amount']*int(amount), grouping=True)}`",color=color)
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if amount.isnumeric() == True:
                            if str(ctx.author.id) not in stocks["Coincord"]: embed = discord.Embed(description="You have no coins :coin:",color=color)
                            else:
                                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + stocks["Coincord"]["Current Amount"]*int(amount)}})

                                stocks["Coincord"][str(ctx.author.id)] -= int(amount)
                                if stocks["Coincord"][str(ctx.author.id)] == 0:del stocks["Coincord"][str(ctx.author.id)]
                                with open('stocks.json', 'w') as f:json.dump(stocks, f, indent=4)

                                embed = discord.Embed(description=f":tada: You sold **{int(amount)} coins :coin:** and got `{pre}{locale.format_string('%d', stocks['Coincord']['Current Amount']*int(amount), grouping=True)}`",color=color)
                                embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                            await ctx.send(embed=embed)
                        else:
                            if amount.lower() == "all" or amount.lower() == "max":
                                if str(ctx.author.id) not in stocks["Coincord"]: embed = discord.Embed(description="You have no coins :coin:",color=color)
                                else:
                                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + stocks["Coincord"]["Current Amount"]*stocks["Coincord"][str(ctx.author.id)]}})

                                    embed = discord.Embed(description=f":tada: You sold **{stocks['Coincord'][str(ctx.author.id)]} coins :coin:** and got `{pre}{locale.format_string('%d', stocks['Coincord']['Current Amount'] * stocks['Coincord'][str(ctx.author.id)], grouping=True)}`",color=color)
                                    embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)

                                    del stocks["Coincord"][str(ctx.author.id)]
                                    with open('stocks.json', 'w') as f: json.dump(stocks, f, indent=4)
                                await ctx.send(embed=embed)
        elif stock.lower() == "orange" or stock.lower() == "o":
            if action is None:
                pass
            else:
                col = db["currency"]
                a = []
                for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
                if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
                wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
                bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
                bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]
                if amount is None:
                    if action.lower() == "buy":
                        if wallet < stocks["Orange"]["Current Amount"]: embed = discord.Embed(description=f"You don't have enough for **an orange :tangerine:** (`{pre}{locale.format_string('%d', stocks['Orange']['Current Amount'], grouping=True)}`)", color=color)
                        else:
                            if str(ctx.author.id) not in stocks["Orange"]: stocks["Orange"][str(ctx.author.id)] = 1
                            else: stocks["Orange"][str(ctx.author.id)] += 1

                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - stocks["Orange"]["Current Amount"]}})

                            with open('stocks.json', 'w') as f: json.dump(stocks, f, indent=4)

                            embed = discord.Embed(description=f"You bought **an orange :tangerine:** for `{pre}{locale.format_string('%d', stocks['Orange']['Current Amount'], grouping=True)}`",color=color)
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if str(ctx.author.id) not in stocks["Orange"]: embed = discord.Embed(description="You have no oranges :tangerine:",color=color)
                        else:
                            stocks["Orange"][str(ctx.author.id)] -= 1

                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + stocks["Orange"]["Current Amount"]}})

                            with open('stocks.json', 'w') as f:json.dump(stocks, f, indent=4)

                            embed = discord.Embed(description=f":tada: You sold **an orange :tangerine:** and got `{pre}{locale.format_string('%d', stocks['Orange']['Current Amount'], grouping=True)}`",color=color)
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                else:
                    if action.lower() == "buy":
                        if wallet < stocks["Orange"]["Current Amount"] * int(amount): embed = discord.Embed(description=f"You don't have enough for **{amount} oranges :tangerine:** (`{pre}{locale.format_string('%d', stocks['Orange']['Current Amount']*int(amount), grouping=True)}`)", color=color)
                        else:
                            if str(ctx.author.id) not in stocks["Orange"]: stocks["Orange"][str(ctx.author.id)] = int(amount)
                            else: stocks["Orange"][str(ctx.author.id)] += int(amount)

                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - stocks["Orange"]["Current Amount"]*int(amount)}})

                            with open('stocks.json', 'w') as f: json.dump(stocks, f, indent=4)

                            embed=discord.Embed(description=f"You bought **{amount} oranges :tangerine:** for `{pre}{locale.format_string('%d', stocks['Orange']['Current Amount']*int(amount), grouping=True)}`",color=color)
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if amount.isnumeric() == True:
                            if str(ctx.author.id) not in stocks["Orange"]: embed = discord.Embed(description="You have no oranges :tangerine:",color=color)
                            else:
                                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + stocks["Orange"]["Current Amount"]*int(amount)}})

                                stocks["Orange"][str(ctx.author.id)] -= int(amount)
                                if stocks["Orange"][str(ctx.author.id)] == 0: del stocks["Orange"][str(ctx.author.id)]
                                with open('stocks.json', 'w') as f: json.dump(stocks, f, indent=4)

                                embed = discord.Embed(description=f":tada: You sold **{int(amount)} oranges :tangerine:** and got `{pre}{locale.format_string('%d', stocks['Orange']['Current Amount']*int(amount), grouping=True)}`",color=color)
                                embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                            await ctx.send(embed=embed)
                        else:
                            if amount.lower() == "all" or amount.lower() == "max":
                                if str(ctx.author.id) not in stocks["Orange"]: embed = discord.Embed(description="You have no oranges :tangerine:",color=color)
                                else:
                                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + stocks["Orange"]["Current Amount"]*stocks["Orange"][str(ctx.author.id)]}})

                                    embed = discord.Embed(description=f":tada: You sold **{stocks['Orange'][str(ctx.author.id)]} oranges :tangerine:** and got `{pre}{locale.format_string('%d', stocks['Orange']['Current Amount'] * stocks['Orange'][str(ctx.author.id)], grouping=True)}`",color=color)
                                    embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)

                                    del stocks["Orange"][str(ctx.author.id)]
                                    with open('stocks.json', 'w') as f: json.dump(stocks, f, indent=4)
                                await ctx.send(embed=embed)
class stockselect(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.response = None
        self.user = None

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.response.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user:
            await interaction.response.send_message("You cannot use this menu.", ephemeral=True)
            return False
        else:
            return True

    @discord.ui.select(placeholder="Select Stock", min_values=1, max_values=1, options = [discord.SelectOption(label="Coincord", value="Coincord", emoji="🪙"),discord.SelectOption(label="Orange", value="Orange", emoji="🍊")])
    async def select(self, select:discord.ui.Select, interaction:discord.Interaction):
        locale.setlocale(locale.LC_ALL, 'en_US')
        with open('stocks.json', 'r') as f:
            stocks = json.load(f)

        with open('serverdb.json', "r") as f:
            prefix = json.load(f)
        if str(interaction.guild_id) in prefix:
            if prefix[str(interaction.guild_id)]["Prefix"] is None:
                theprefix = default
            else:
                theprefix = prefix[str(interaction.guild_id)]["Prefix"]
        else:
            theprefix = default
        cca = stocks["Coincord"]["Current Amount"]
        cpa = stocks["Coincord"]["Previous Amount"]
        oca = stocks["Orange"]["Current Amount"]
        opa = stocks["Orange"]["Previous Amount"]
        if select.values[0] == "Coincord":
            if cca > cpa:
                if cca >= cpa * 2:
                    ec = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**'
                else:
                    ec = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**'
            elif cca == cpa:
                ec = f'**No Change** [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
            else:
                ec = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▼ {pre}{locale.format_string("%d", cpa - cca, grouping=True)} `(▼ {(cpa - cca) / cpa * 100:.2f}%)`**'
            embed = discord.Embed(title="Coincord",
                                  description=f"A beautiful coin. Pretty useless, but they might be worth a fortune\n```yaml\nSyntax: {theprefix}stocks cc buy/sell [amount]```\n**Stats:**\n{ec}\n```yaml\nLast Updated: {stocks['Reset']}```",
                                  color=color)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/868290623394947102/875194040600133632/1fa99.png')
            embed.set_image(url=coincord_file)
            embed.set_footer(text="stonks")
            await interaction.response.edit_message(content=None, embed=embed)
        elif select.values[0] == "Orange":
            if oca > opa:
                if oca >= opa * 2:
                    ec = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**'
                else:
                    ec = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**'
            elif oca == opa:
                ec = f'**No Change** [{pre}{locale.format_string("%d", oca, grouping=True)} / coin](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
            else:
                ec = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / coin](https://google.com) ─ **▼ {pre}{locale.format_string("%d", opa - oca, grouping=True)} `(▲ {(opa - oca) / opa * 100:.2f}%)`**'
            embed = discord.Embed(title="Orange",
                                  description=f"A fresh orange orange. You can use it to flex to your friends.\n```yaml\nSyntax: {theprefix}stocks o buy/sell [amount]```\n**Stats:**\n{ec}\n```yaml\nLast Updated: {stocks['Reset']}```",
                                  color=color)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/868290623394947102/875196175286943744/orange-emoji-by-twitter.png')
            embed.set_image(url=orange_file)
            embed.set_footer(text="stonks")
            await interaction.response.edit_message(content=None, embed=embed)
@commands.command()
@commands.is_owner()
async def mystocks(ctx):
    with open('commandusage.json', "r") as f:
        cdb = json.load(f)
        await cu("Mystocks", cdb)
        with open('commandusage.json', "w") as f: json.dump(cdb, f, indent=4, sort_keys=True)
    with open('serverdb.json', "r") as f:
        prefix = json.load(f)
    if str(ctx.author.guild.id) in prefix:
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None:
            theprefix = default
        else:
            theprefix = prefix[str(ctx.author.guild.id)]["Prefix"]
    else:
        theprefix = default

    with open('stocks.json', 'r') as f:
        stocks = json.load(f)

    if str(ctx.author.id) not in stocks["Coincord"] and str(ctx.author.id) not in stocks["Orange"]:
        embed = discord.Embed(description=f"You have no stocks currently\nGo buy some: **`{theprefix}stocks`**", color=color)
    else:
        cca = stocks["Coincord"]["Current Amount"]
        cpa = stocks["Coincord"]["Previous Amount"]
        oca = stocks["Orange"]["Current Amount"]
        opa = stocks["Orange"]["Previous Amount"]
        embed=discord.Embed(description=f"Stocks reset on **{stocks['Reset']}**", color=color)
        embed.set_author(name=f"{ctx.author.name}'s stocks", icon_url=ctx.author.avatar)
        embed.set_footer(text="stonks")

        if str(ctx.author.id) in stocks["Coincord"]:
            if cca > cpa:
                if cca >= cpa * 2:
                    ec = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**\n\nYou have **{stocks["Coincord"][str(ctx.author.id)]} coins** (`{pre}{locale.format_string("%d", stocks["Coincord"][str(ctx.author.id)] * stocks["Coincord"]["Current Amount"], grouping=True)}`)'
                    footer = "Your professional investor advises you REALLY to sell"
                else:
                    ec = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**\n\nYou have **{stocks["Coincord"][str(ctx.author.id)]} coins** (`{pre}{locale.format_string("%d", stocks["Coincord"][str(ctx.author.id)] * stocks["Coincord"]["Current Amount"], grouping=True)}`)'
                    footer = "Your professional investor advises you to sell"
            elif cca == cpa:
                ec = f'**No Change** [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**\n\nYou have **{stocks["Coincord"][str(ctx.author.id)]} coins** (`{pre}{locale.format_string("%d", stocks["Coincord"][str(ctx.author.id)] * stocks["Coincord"]["Current Amount"], grouping=True)}`)'
                footer = "Your professional investor advises you to not sell"
            else:
                ec = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▼ {pre}{locale.format_string("%d", cpa - cca, grouping=True)} `(▼ {(cpa - cca) / cpa * 100:.2f}%)`**\n\nYou have **{stocks["Coincord"][str(ctx.author.id)]} coins** (`{pre}{locale.format_string("%d", stocks["Coincord"][str(ctx.author.id)] * stocks["Coincord"]["Current Amount"], grouping=True)}`)'
                footer = "Your professional investor advises you to not sell"

            embed.add_field(name="Coincord :coin:", value=f"{ec}\n```yaml\n{footer}```", inline=False)
        if str(ctx.author.id) in stocks["Orange"]:
            if oca > opa:
                if oca >= opa * 2:
                    oc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**\n\nYou have **{stocks["Orange"][str(ctx.author.id)]} oranges** (`{pre}{locale.format_string("%d", stocks["Orange"][str(ctx.author.id)] * stocks["Orange"]["Current Amount"], grouping=True)}`)'
                    footer2 = "Your professional investor advises you REALLY to sell"
                else:
                    oc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**\n\nYou have **{stocks["Orange"][str(ctx.author.id)]} oranges** (`{pre}{locale.format_string("%d", stocks["Orange"][str(ctx.author.id)] * stocks["Orange"]["Current Amount"], grouping=True)}`)'
                    footer2 = "Your professional investor advises you to sell"
            elif oca == opa:
                oc = f'**No Change** [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**\n\nYou have **{stocks["Orange"][str(ctx.author.id)]} oranges** (`{pre}{locale.format_string("%d", stocks["Orange"][str(ctx.author.id)] * stocks["Orange"]["Current Amount"], grouping=True)}`)'
                footer2 = "Your professional investor advises you to not sell"
            else:
                oc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▼ {pre}{locale.format_string("%d", opa - oca, grouping=True)} `(▼ {(opa - oca) / opa * 100:.2f}%)`**\n\nYou have **{stocks["Orange"][str(ctx.author.id)]} oranges** (`{pre}{locale.format_string("%d", stocks["Orange"][str(ctx.author.id)] * stocks["Orange"]["Current Amount"], grouping=True)}`)'
                footer2 = "Your professional investor advises you to not sell"
            embed.add_field(name='Orange :tangerine:', value=f"{oc}\n```yaml\n{footer2}```", inline=False)
    await ctx.send(embed=embed)




"""FISHING"""
@commands.command()
@commands.cooldown(1, 3, commands.BucketType.user)
@commands.is_owner()
async def fish(ctx):
    with open('fish.json', 'r') as f:
        fish = json.load(f)
    with open('leagues.json', "r") as f:
        l = json.load(f)
        if str(ctx.author.id) not in l:
            await uleague(str(ctx.author.id), l)
            await cl(str(ctx.author.id), l, league="🔰 Challenger 🔰")
        with open('leagues.json', "w") as f: json.dump(l, f, indent=4, sort_keys=True)
    rare = random.randint(1, 10000)
    trophy = random.randint(1, 10)
    rt = random.randint(1, 5)
    bonus = None
    if rare <=6500:
        afish = random.randint(1, 5)
        type = random.choice(["Fish", "Shrimp"])
        emoji = type.lower()
    elif rare > 6500 and rare <= 9000:
        afish = 1
        type = random.choice(["Rare Fish", "Crab", "Squid"])
        if rt == 1:
            if type =="Rare Fish":
                emoji = "tropical_fish"
            else:
                emoji = type.lower()
            with open('leagues.json', 'w') as f:
                json.dump(l, f, indent=4)
            if trophy > 1:
                bonus = f"**YOU LUCKY DUCKY!** You also found **`{trophy}` Trophies** <:leaguetrophy:879793117555998790>!"
            else:
                bonus = f"**YOU LUCKY DUCKY!** You also found **a Trophy** <:leaguetrophy:879793117555998790>!"
        else:
            if type =="Rare Fish":
                emoji = "tropical_fish"
            else:
                emoji = type.lower()
            bonus = ""
    elif rare > 9000 and rare <= 9950:
        afish = 1
        type = random.choice(["Octopus", "Dolphin", "Blowfish", "Lobster"])
        emoji = type.lower()
    else:
        afish = 1
        type = random.choice(["Whale", "Shark"])
        if type =="Whale":
            emoji = "whale2"
        else:
            emoji = type.lower()

    if str(ctx.author.id) not in fish:
        await ufish(ctx.author.id, fish)
        await cfish(ctx.author.id, fish, type=type, amount=afish)
    else:
        await cfish(ctx.author.id, fish, type=type, amount=afish)
    with open('fish.json', 'w') as f:
        json.dump(fish, f, indent=4)
    embed=discord.Embed(description=f"You caught **{afish} {type}** :{emoji}:!", color=color)
    await ctx.send(embed=embed)
    if bonus is not None:
        await ctx.send(bonus)

        if l[str(ctx.author.id)]["Trophies"]+trophy >= 250 and l[str(ctx.author.id)]["Trophies"]+trophy < 500 and "Novice" not in l[str(ctx.author.id)]["League"]:
            await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
            await cl(str(ctx.author.id),l, league="🛡️ Novice Tier 🛡️")
        elif l[str(ctx.author.id)]["Trophies"]+trophy >= 500 and l[str(ctx.author.id)]["Trophies"]+trophy < 1000 and "Gold" not in l[str(ctx.author.id)]["League"]:
            await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
            await cl(str(ctx.author.id), l, league="🔱 Gold Tier 🔱")
        elif l[str(ctx.author.id)]["Trophies"]+trophy >= 1000 and l[str(ctx.author.id)]["Trophies"]+trophy < 2000 and "Purple Dragon" not in l[str(ctx.author.id)]["League"]:
            await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
            await cl(str(ctx.author.id), l, league="⚜️ Purple Dragon Tier ⚜️")
        elif l[str(ctx.author.id)]["Trophies"]+trophy >= 2000 and l[str(ctx.author.id)]["Trophies"]+trophy < 3000 and "Diamond" not in l[str(ctx.author.id)]["League"]:
            await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
            await cl(str(ctx.author.id), l, league="💎 Diamond Tier 💎")
        elif l[str(ctx.author.id)]["Trophies"]+trophy >= 3000 and l[str(ctx.author.id)]["Trophies"]+trophy < 4500 and "Master" not in l[str(ctx.author.id)]["League"]:
            await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
            await cl(str(ctx.author.id), l, league="⚔️ Master Tier ⚔️")
        elif l[str(ctx.author.id)]["Trophies"]+trophy >= 4500 and l[str(ctx.author.id)]["Trophies"]+trophy < 5000 and "Legendary" not in l[str(ctx.author.id)]["League"]:
            await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
            await cl(str(ctx.author.id), l, league="🃏 Legendary Tier 🃏")
        elif l[str(ctx.author.id)]["Trophies"]+trophy >= 5000 and "The Best of the Best" not in l[str(ctx.author.id)]["League"]:
            await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
            await cl(str(ctx.author.id), l, league="🏴‍☠️ The Best of the Best 🏴‍☠️")
        await ct(str(ctx.author.id), l, trophies=trophy)
    with open('leagues.json', 'w') as f:
        json.dump(l, f, indent=4)
@fish.error
async def fish_e(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if int(s)+1 == 1:
            suffix = "second"
        else:
            suffix = "seconds"
        if int(h) == 0 and int(m) == 0:
            embed = discord.Embed(title="Slow it down",
                                  description=f"Your on cooldown. **{int(s)+1} {suffix}** left",
                                  color=color)
            await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def myfish(ctx):
    with open('fish.json', 'r') as f:
        fish = json.load(f)
    if str(ctx.author.id) not in fish:
        await ufish(ctx.author.id, fish)
    with open('fish.json', 'w') as f:
        json.dump(fish, f, indent=4)
    final = []
    for a in fish[str(ctx.author.id)]:
        if fish[str(ctx.author.id)][str(a)] != 0:
            if a == "Whale":
                emoji = "whale2"
            elif a == "Rare Fish":
                emoji = "tropical_fish"
            else:
                emoji = a.lower()
            final.append(f"**{a}** :{emoji}: ─ {fish[str(ctx.author.id)][a]}")

    embed=discord.Embed(title=f"{ctx.author.name}'s Fishing Inventory",description="\n".join(a for a in final), color=color)
    await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def fsell(ctx, arg, amount:int=None):
    with open('fish.json', 'r') as f:
        fish = json.load(f)
    if str(ctx.author.id) not in fish:
        await ufish(ctx.author.id, fish)
    with open('fish.json', 'w') as f:
        json.dump(fish, f, indent=4)
    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one(
        {"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
    if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},
                                                {"$set": {"USER": str(ctx.author)}})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]




"""GAMBLING"""
@commands.command()
@commands.is_owner()
async def flipcoin(ctx, choice=None):
    with open('commandusage.json', "r") as f:
        cdb = json.load(f)
        await cu("Flipcoin", cdb)
        with open('commandusage.json', "w") as f: json.dump(cdb, f, indent=4, sort_keys=True)
    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    if choice is None:
        await ctx.reply(f"You need to guess the landing face.")
    else:
        if choice.lower() == "heads" or choice.lower() == "head" or choice.lower() == "h" or choice.lower() == "tails" or choice.lower() == "tail" or choice.lower() == "t":
            message = await ctx.reply("Flipping the coin...")
            time.sleep(2)
            if choice.lower() == "heads" or choice.lower() == "tails": true = random.choice(("heads", "tails"))
            elif choice.lower() == "head" or choice.lower() == "tail": true = random.choice(("head", "tail"))
            else: true = random.choice(("h", "t"))
            coins = random.randint(1000, 10000)
            if choice.lower() == true:
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet+coins}})
                await message.edit(f"**You won {pre}{coins}!** The coin landed on **`{true}`**")
            else: await message.edit(f"You lost. The coin landed on **`{true}`**")
        else: await ctx.send("Your choices are: **`Heads`** or **`Tails`**")
@commands.command()
@commands.is_owner()
async def gamble(ctx, amount):
    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]




"""DAILY COINS"""
@commands.command()
@commands.is_owner()
async def feelinglucky(ctx):
    with open('commandusage.json', "r") as f:
        cdb = json.load(f)
        await cu("Feelinglucky", cdb)
        with open('commandusage.json', "w") as f: json.dump(cdb, f, indent=4, sort_keys=True)
    with open('daily.json', 'r') as f:
        d = json.load(f)
    if str(ctx.author.id) in d:
        if d[str(ctx.author.id)]["Feeling Lucky"] is None:
            cool = True
        else:
            cool = False
    else:
        cool = True

    if cool == True:
        await ud(str(ctx.author.id), d)
        with open('daily.json', 'w') as f:
            json.dump(d, f, indent=4)
        await luf(str(ctx.author.id), d, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        with open('daily.json', 'w') as f:
            json.dump(d, f, indent=4)

        col = db["currency"]
        a = []
        for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
        if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
        userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
        if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
        wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
        bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
        bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

        coins = random.randint(10000, 100000)
        col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + coins}})
        await ctx.send(f"You got your lucky **{pre}{coins}!**. Check in again in `24 hours`.")
    else:
        past = datetime(int(d[str(ctx.author.id)]["Feeling Lucky"][0:4]), int(d[str(ctx.author.id)]["Feeling Lucky"][5:7]),
                        int(d[str(ctx.author.id)]["Feeling Lucky"][8:10]), int(d[str(ctx.author.id)]["Feeling Lucky"][11:13]),
                        int(d[str(ctx.author.id)]["Feeling Lucky"][14:16]), int(d[str(ctx.author.id)]["Feeling Lucky"][17:19]))
        duration = past - datetime.utcnow()
        duration2 = datetime.utcnow() - past
        duration_in_s = duration.total_seconds()
        days = divmod(duration_in_s, 86400)  # Get days (without [0]!)
        hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
        minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
        seconds = divmod(minutes[1], 1)
        if duration2.days >= 1:
            await luf(str(ctx.author.id), d, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            with open('daily.json', 'w') as f:
                json.dump(d, f, indent=4)

            col = db["currency"]
            a = []
            for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
            if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
            userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
            if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
            wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
            bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
            bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

            coins = random.randint(10000, 100000)
            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + coins}})
            await ctx.send(f"You got your lucky **{pre}{coins}!**. Check in again in `24 hours`.")
        else:
            suffixh = ""
            suffixm = ""
            suffixs = ""
            if int(hours[0]) == 1:
                suffixh="hour"
            else:
                suffixh="hours"
            if int(minutes[0]) == 1:
                suffixm = "minute"
            else:
                suffixm = "minutes"
            if int(seconds[0]) == 1:
                suffixs = "second"
            else:
                suffixs="seconds"
            embed = discord.Embed(title="Slow it down",
                                  description=f"Your on cooldown. **{int(hours[0])} {suffixh}, {int(minutes[0])} {suffixm} and {int(seconds[0])} {suffixs}** left.",
                                  color=color)
            await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def daily(ctx):
    with open('commandusage.json', "r") as f:
        cdb = json.load(f)
        await cu("Daily", cdb)
        with open('commandusage.json', "w") as f: json.dump(cdb, f, indent=4, sort_keys=True)
    with open('daily.json', 'r') as f:
        d = json.load(f)
    if str(ctx.author.id) in d:
        if d[str(ctx.author.id)]["Daily"] is None:
            cool = True
        else:
            cool = False
    else:
        cool = True

    if cool == True:
        await ud(str(ctx.author.id), d)
        with open('daily.json', 'w') as f:
            json.dump(d, f, indent=4)
        await lud(str(ctx.author.id), d, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        with open('daily.json', 'w') as f:
            json.dump(d, f, indent=4)

        col = db["currency"]
        a = []
        for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
        if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
        userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
        if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
        wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
        bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
        bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

        coins = 100000
        col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + coins}})
        await ctx.send(f"You got your daily **{pre}{coins}!**. Check in again in `24 hours`.")
    else:
        past = datetime(int(d[str(ctx.author.id)]["Daily"][0:4]), int(d[str(ctx.author.id)]["Daily"][5:7]),
                        int(d[str(ctx.author.id)]["Daily"][8:10]), int(d[str(ctx.author.id)]["Daily"][11:13]),
                        int(d[str(ctx.author.id)]["Daily"][14:16]), int(d[str(ctx.author.id)]["Daily"][17:19]))
        duration = past - datetime.utcnow()
        duration2 = datetime.utcnow() - past
        duration_in_s = duration.total_seconds()
        days = divmod(duration_in_s, 86400)  # Get days (without [0]!)
        hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
        minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
        seconds = divmod(minutes[1], 1)
        if duration2.days >= 1:
            await lud(str(ctx.author.id), d, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            with open('daily.json', 'w') as f:
                json.dump(d, f, indent=4)

            col = db["currency"]
            a = []
            for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
            if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
            userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
            if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
            wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
            bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
            bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

            coins = 100000
            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + coins}})
            await ctx.send(f"You got your daily **{pre}{coins}!**. Check in again in `24 hours`.")
        else:
            suffixh = ""
            suffixm = ""
            suffixs = ""
            if int(hours[0]) == 1:
                suffixh = "hour"
            else:
                suffixh = "hours"
            if int(minutes[0]) == 1:
                suffixm = "minute"
            else:
                suffixm = "minutes"
            if int(seconds[0]) == 1:
                suffixs = "second"
            else:
                suffixs = "seconds"
            embed = discord.Embed(title="Slow it down",
                                  description=f"Your on cooldown. **{int(hours[0])} {suffixh}, {int(minutes[0])} {suffixm} and {int(seconds[0])} {suffixs}** left.",
                                  color=color)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(buy)
    bot.add_command(use)
    bot.add_command(inventory)
    bot.add_command(shop)
    bot.add_command(freetrophy)
    bot.add_command(profile)
    bot.add_command(leagues)
    bot.add_command(myfish)
    bot.add_command(fish)
    #bot.add_command(dice)
    bot.add_command(top)
    bot.add_command(daily)
    bot.add_command(feelinglucky)
    bot.add_command(flipcoin)
    bot.add_command(mystocks)
    bot.add_command(stock)
    #bot.add_command(slots)
    bot.add_command(dep)
    bot.add_command(withdraw)
    bot.add_command(balance)
    bot.add_command(give)
    bot.add_command(toptrophies)
