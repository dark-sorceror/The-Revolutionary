import time
import datetime
import json
import locale
import random
import pymongo
import asyncio
from datetime import datetime, timedelta, timezone
from collections import Counter

import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot

from variables import (
    color,
    cu,
    cfish,
    cl,
    ct,
    lud,
    luf,
    ufish,
    ud,
    uleague,
    uinv,
    pre,
    bot,
    custom_footer,
    default_prefix,
    luw,
    cdfish,
    default_prefix
)

slot_machine_1 = [":clown:", "<:TheRevolutionary:879794710334545951>", ":fire:", ":flushed:", ":sunglasses:", ":peach:", ":watermelon:", ":eggplant:", ":gem:", ":moneybag:", ":medal:", ":punch:"]
slot_machine_2 = [":clown:", "<:TheRevolutionary:879794710334545951>", ":fire:", ":flushed:", ":sunglasses:", ":peach:", ":watermelon:", ":eggplant:", ":gem:", ":moneybag:", ":medal:", ":punch:"]
slot_machine_3 = [":clown:", "<:TheRevolutionary:879794710334545951>", ":fire:", ":flushed:", ":sunglasses:", ":peach:", ":watermelon:", ":eggplant:", ":gem:", ":moneybag:", ":medal:", ":punch:"]

slot_rate = {
    ":clown:": round(random.uniform(1.1, 1.2), 4),
    "<:TheRevolutionary:879794710334545951>": round(random.uniform(1.8, 1.9), 4),
    ":fire:": round(random.uniform(1.9, 2), 4),
    ":flushed:": round(random.uniform(1.4, 1.5), 4),
    ":sunglasses:": round(random.uniform(1.3, 1.4), 4),
    ":peach:": round(random.uniform(1.5, 1.6), 4),
    ":watermelon:": round(random.uniform(1.6, 1.7), 4),
    ":eggplant:": round(random.uniform(1.5, 1.6), 4),
    ":gem:": round(random.uniform(1.6, 1.7), 4),
    ":moneybag:": round(random.uniform(1.7, 1.8), 4),
    ":medal:": round(random.uniform(1.7, 1.8), 4),
    ":punch:": round(random.uniform(1.7, 1.8), 4)
}
chart = {
    "Fish :fish:": 50,
    "Shrimp :shrimp:": 62,
    "Rare Fish :tropical_fish:": 125,
    "Crab :crab:": 150,
    "Squid :squid:": 250,
    "Octopus :octopus:": 500,
    "Dolphin :dolphin:": 1500,
    "Blowfish :blowfish:": 1750,
    "Lobster :lobster:": 1500,
    "Whale :whale2:": 6250,
    "Shark :shark:": 18750,
    "Crocodile :crocodile:": 40000,
    "Sea Dragon :dragon:": 1125000,
    "Mythical Fish <:MythicalFish:892182628717953024>": 1250000
}
items={
"<:mythicalbox:881252527235018753> Mythical Box": [10000000,"There is a possibility of getting unknown items :eyes:"],
"<:legendarybox:880229601043963905> Legendary Box": [2500000,"Very rare items inside"],
"<:christmasbox:881252565503868958> Christmas Box": [500000,"Decent items, it's a gift for any season"],
":worm: Worm": [100, "A one-time power-up when fishing. Helps to get more rare stuff!"],
":fishing_pole_and_fish: Fishing Rod": [50000, "Use this to start fishing."],
"<:biggerfr:898645851461783594> Platinum Fishing Rod": [250000, "With this rod, you can fish out more quantities of fish!"]
}

db = pymongo.MongoClient("mongodb+srv://abcd:abcde@cluster0.ctiwz.mongodb.net/currency?retryWrites=true&w=majority")["currency"]
fishdb = pymongo.MongoClient("mongodb+srv://abcd:abcde@cluster0.ctiwz.mongodb.net/fish?retryWrites=true&w=majority")["fish"]
dailydb = pymongo.MongoClient("mongodb+srv://abcd:abcde@cluster0.ctiwz.mongodb.net/daily?retryWrites=true&w=majority")["daily"]
commandsdb = pymongo.MongoClient("mongodb+srv://abcd:abcde@cluster0.ctiwz.mongodb.net/commands?retryWrites=true&w=majority")["commands"]
leaugesdb = pymongo.MongoClient("mongodb+srv://abcd:abcde@cluster0.ctiwz.mongodb.net/leagues?retryWrites=true&w=majority")["leagues"]
serverdb = pymongo.MongoClient("mongodb+srv://abcd:abcde@cluster0.ctiwz.mongodb.net/serverdb?retryWrites=true&w=majority")["serverdb"]
indb = pymongo.MongoClient("mongodb+srv://abcd:abcde@cluster0.ctiwz.mongodb.net/inventory?retryWrites=true&w=majority")["inventory"]
stocksdb = pymongo.MongoClient("mongodb+srv://abcd:abcde@cluster0.ctiwz.mongodb.net/stocks?retryWrites=true&w=majority")["stocks"]
farmdb = pymongo.MongoClient("mongodb+srv://abcd:abcde@cluster0.ctiwz.mongodb.net/farm?retryWrites=true&w=majority")["farm"]

"""ECONOMY"""
@commands.command(aliases=["deposit", "DEP", "Dep", "dEP", "DEPOSIT", "Deposit", "dEPOSIT"])
async def dep(ctx, arg):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Deposit": 1})["Deposit"]
    colc.update_one({"Deposit":tc}, {"$set": {"Deposit": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Deposit": 1})["Deposit"]
    cold.update_one({"Deposit": tcd}, {"$set": {"Deposit": tcd + 1}})


    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
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
                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - wallet}})
                    col.update_one({"USER ID": ctx.author.id, "Bank": bank}, {"$set": {"Bank": bank + wallet}})
                    embed = discord.Embed(
                        description=f"Deposited **{pre}{locale.format_string('%d', wallet, grouping=True)}**",
                        color=color)
                else:

                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - (bankl - bank)}})
                    col.update_one({"USER ID": ctx.author.id, "Bank": bank}, {"$set": {"Bank": bank + (bankl - bank)}})
                    embed = discord.Embed(
                        description=f"Deposited **{pre}{locale.format_string('%d', bankl - bank, grouping=True)}**",
                        color=color)
            else:
                if bankl > wallet:
                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - wallet}})
                    col.update_one({"USER ID": ctx.author.id, "Bank": bank},{"$set": {"Bank": bank + wallet}})
                    embed = discord.Embed(
                        description=f"Deposited **{pre}{locale.format_string('%d', wallet, grouping=True)}**",
                        color=color)
                else:
                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - bankl}})
                    col.update_one({"USER ID": ctx.author.id, "Bank": bank},{"$set": {"Bank": bank + bankl}})
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
async def withdraw(ctx, arg):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Withdraw": 1})["Withdraw"]
    colc.update_one({"Withdraw": tc}, {"$set": {"Withdraw": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Withdraw": 1})["Withdraw"]
    cold.update_one({"Withdraw": tcd}, {"$set": {"Withdraw": tcd + 1}})

    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
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
async def balance(ctx, user: discord.Member=None):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Balance": 1})["Balance"]
    colc.update_one({"Balance": tc}, {"$set": {"Balance": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Balance": 1})["Balance"]
    cold.update_one({"Balance": tcd}, {"$set": {"Balance": tcd + 1}})

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
        micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

        if ctx.author.color == discord.Color.from_rgb(0, 0, 0):
            c = discord.Color.from_rgb(47, 49, 54)
        else:
            c = ctx.author.color
        embed = discord.Embed(description=f'**Wallet**: {pre}{locale.format_string("%d", wallet, grouping=True)}\n**Bank**: {pre}{locale.format_string("%d", bank, grouping=True)} / {locale.format_string("%d", bankl, grouping=True)} **(`{(bank/bankl)*100:.1f}%`)**\n**Total**: {pre}{locale.format_string("%d", wallet+bank, grouping=True)}', color=c)
        embed.set_author(name=f"{ctx.author.name}'s balance", icon_url=micon)
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
        micon = user.default_avatar if not user.avatar else user.avatar.url

        if user.color == discord.Color.from_rgb(0, 0, 0):
            c = discord.Color.from_rgb(47, 49, 54)
        else:
            c = user.color
        embed = discord.Embed(description=f'**Wallet**: {pre}{locale.format_string("%d", wallet, grouping=True)}\n**Bank**: {pre}{locale.format_string("%d", bank, grouping=True)} / {locale.format_string("%d", bankl, grouping=True)} **(`{(bank/bankl)*100:.1f}%`)**\n**Total**: {pre}{locale.format_string("%d", wallet + bank, grouping=True)}', color = c)
        embed.set_author(name=f"{user.name}'s balance", icon_url=micon)
        embed.set_footer(text=f"{custom_footer}")
        await ctx.send(embed=embed)
@commands.command(aliases=["share", "Give", "Share", "GIVE", "SHARE"])
async def give(ctx, user: discord.Member, amount:int):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Give": 1})["Give"]
    colc.update_one({"Give": tc}, {"$set": {"Give": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Give": 1})["Give"]
    cold.update_one({"Give": tcd}, {"$set": {"Give": tcd + 1}})

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
        embed = discord.Embed(description="You can't send money to yourself",color=discord.Color.red())
        embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
    elif amount > wallet:
        embed = discord.Embed(description=f"You only have **{pre}{locale.format_string('%d', wallet, grouping=True)}** in your wallet",color=discord.Color.red())
        embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
    elif amount == 0:
        embed = discord.Embed(description=f"Sending someone **{pre}0** is not necessary", color=color)
        embed.set_author(name='Warning', icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
    else:
        col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - amount}})
        col.update_one({"USER ID": user.id, "Wallet": mwallet}, {"$set": {"Wallet": mwallet + amount}})
        embed = discord.Embed(description=f'You gave {user.mention} **{pre}{locale.format_string("%d", amount, grouping=True)}**. Now you have **{pre}{locale.format_string("%d", wallet-amount, grouping=True)}** and they have **{pre}{locale.format_string("%d", mwallet+amount, grouping=True)}**.', color=discord.Color.green())
        micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url
        embed.set_author(name="Successful Transaction", icon_url=micon)
    await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def top(ctx):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Top": 1})["Top"]
    colc.update_one({"Top": tc}, {"$set": {"Top": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Top": 1})["Top"]
    cold.update_one({"Top": tcd}, {"$set": {"Top": tcd + 1}})

    col = db["currency"]
    cool = {}
    humans = [m for m in ctx.author.guild.members if not m.bot]
    for a in humans:
        for x in col.find({"USER ID":a.id}, {"_id": 0, "USER":1, "Wallet": 1}):
            if x["Wallet"] <= 1000: pass
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
        embed.set_footer(text=f"You have {pre}{locale.format_string('%d',wallet, grouping=True)}")
    await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def toptrophies(ctx):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Toptrophies": 1})["Toptrophies"]
    colc.update_one({"Toptrophies": tc}, {"$set": {"Toptrophies": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Toptrophies": 1})["Toptrophies"]
    cold.update_one({"Toptrophies": tcd}, {"$set": {"Toptrophies": tcd + 1}})

    cool2 = {}
    humans = [m for m in ctx.author.guild.members if not m.bot]
    colt = leaugesdb["leagues"]

    for b in humans:
        for x in colt.find({"USER ID": b.id}, {"_id": 0, "USER":1,"Trophies": 1}):
            if x["Trophies"] == 0:
                pass
            else:
                cool2[x["USER"]] = x["Trophies"]
    b = []
    for x in colt.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colt.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "League": "🔰 Challenger 🔰", "Trophies": 0})
    trophye = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Trophies": 1})["Trophies"]
    league = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "League": 1})["League"]
    trophy = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Trophies": 1})["Trophies"]
    z = Counter(cool2)
    high2 = z.most_common(10)
    place2 = 1
    thelist2 = []
    nameplace = None
    emoji = ""
    for i in high2:
        if place2 == 10:
            thelist2.append(f"{place2}. {locale.format_string('%d', i[1], grouping=True).ljust(20)}{i[0].ljust(1)}")
        else:
            thelist2.append(f"{place2}.  {locale.format_string('%d', i[1], grouping=True).ljust(20)}{i[0].ljust(1)}")
        if i[0] == str(ctx.author):
            if place2 == 1:
                nameplace = f"{place2}st"
                emoji = "🥇"
            elif place2 == 2:
                nameplace = f"{place2}nd"
                emoji = "🥈"
            elif place2 == 3:
                nameplace = f"{place2}rd"
                emoji = "🥉"
            else:
                nameplace = f"{place2}th"
                emoji = ""
        place2 += 1
    if nameplace != None:
        embed = discord.Embed(title=f"Top 10 User Trophies in **{ctx.author.guild}**",
                              description=f"```md\n#   {'Amount'.ljust(20)}{'Name'.ljust(1)}\n" + "\n".join(
                                  a for a in thelist2) + "```",
                              color=color)
        embed.set_author(name="The Revolutionary",
                         icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
        embed.set_thumbnail(url=ctx.author.guild.icon)
        embed.set_footer(text=f"You are {nameplace}{emoji}!")
    else:
        embed = discord.Embed(title=f"Top 10 User Trophies in **{ctx.author.guild}**",
                              description=f"```md\n#   {'Amount'.ljust(20)}{'Name'.ljust(1)}\n" + "\n".join(
                                  a for a in thelist2) + "```",
                              color=color)
        embed.set_author(name="The Revolutionary",
                         icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
        embed.set_thumbnail(url=ctx.author.guild.icon)
        embed.set_footer(text=f"You have {locale.format_string('%d', trophy, grouping=True)} trophies")
    await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def profile(ctx, member:discord.Member=None):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Profile": 1})["Profile"]
    colc.update_one({"Profile": tc}, {"$set": {"Profile": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Profile": 1})["Profile"]
    cold.update_one({"Profile": tcd}, {"$set": {"Profile": tcd + 1}})

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
        networth = wallet+bank

        colt = leaugesdb["leagues"]
        b = []
        for x in colt.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
        if {"USER ID": ctx.author.id} not in b: colt.insert_one({"USER ID": ctx.author.id, "League": "🔰 Challenger 🔰", "Trophies": 0})
        trophy = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Trophies": 1})["Trophies"]
        league = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "League": 1})["League"]

        uscol = stocksdb["userstock"]
        cols = stocksdb["stocks"]

        uscol = stocksdb["userstock"]
        aab = []
        for x in uscol.find({}, {"_id": 0, "USER ID": 1}): aab.append(x)
        if {"USER ID": ctx.author.id} not in aab: uscol.insert_one({"USER ID": ctx.author.id, "Coincord": 0, "Orange": 0, "Golden Statue of Statue of Golden": 0,"The Revolutionary": 0})

        c = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Coincord": 1})["Coincord"]
        o = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Orange": 1})["Orange"]
        s = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Golden Statue of Statue of Golden": 1})["Golden Statue of Statue of Golden"]
        t = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "The Revolutionary": 1})["The Revolutionary"]
        cca = cols.find_one({"Stock": "Coincord"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        cpa = cols.find_one({"Stock": "Coincord"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        oca = cols.find_one({"Stock": "Orange"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        opa = cols.find_one({"Stock": "Orange"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        sca = cols.find_one({"Stock": "Golden Statue of Statue of Golden"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        spa = cols.find_one({"Stock": "Golden Statue of Statue of Golden"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        tca = cols.find_one({"Stock": "The Revolutionary"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        tpa = cols.find_one({"Stock": "The Revolutionary"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]

        col2 = fishdb["fish"]
        b = []
        for x in col2.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
        if {"USER ID": ctx.author.id} not in b: col2.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Fish :fish:": 0, "Shrimp :shrimp:": 0,"Rare Fish :tropical_fish:": 0, "Crab :crab:": 0, "Squid :squid:": 0, "Octopus :octopus:": 0,"Dolphin :dolphin:": 0, "Blowfish :blowfish:": 0, "Lobster :lobster:": 0, "Whale :whale2:": 0,"Shark :shark:": 0, "Crocodile :crocodile:": 0, "Sea Dragon :dragon:": 0,"Mythical Fish <:MythicalFish:892182628717953024>": 0, "Prized Fish": None})

        tf = col2.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Prized Fish": 1})["Prized Fish"]

        networth+=c*cca+o*oca+t*tca+s*sca

        for c in col2.find({"USER ID": ctx.author.id}, {"_id": 0, "USER ID": 0, "USER": 0}):
            for b in list(c.keys()):
                if c.get(b) != 0 and b != "Prized Fish":
                    networth += c.get(b)*chart.get(b)

        embed=discord.Embed(description=f"**<:leaguetrophy:891844638380556319> {trophy} ─ {league}**",color=color)
        embed.add_field(name="Coins",value=f'**Wallet:** {pre}{locale.format_string("%d", wallet, grouping=True)}\n**Bank:** {pre}{locale.format_string("%d", bank, grouping=True)}\n**Networth:** {pre}{locale.format_string("%d", networth, grouping=True)}')
        if tf is not None:
            embed.add_field(name="Most Prized Catch", value=f"**{tf}**", inline=False)
        micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url
        embed.set_author(name=ctx.author.name, icon_url=micon)
        embed.set_thumbnail(url=micon)
        await ctx.send(embed=embed)
    else:
        col = db["currency"]
        a = []
        for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
        if {"USER ID": member.id} not in a: col.insert_one({"USER ID": member.id, "USER": str(member), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
        userr = col.find_one({"USER ID": member.id}, {"_id": 0, "USER": 1})["USER"]
        if userr != str(member): col.update_one({"USER ID": member.id, "USER": userr},{"$set": {"USER": str(member)}})
        wallet = col.find_one({"USER ID": member.id}, {"_id": 0, "Wallet": 1})["Wallet"]
        bank = col.find_one({"USER ID": member.id}, {"_id": 0, "Bank": 1})["Bank"]
        bankl = col.find_one({"USER ID": member.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]
        networth = wallet + bank

        uscol = stocksdb["userstock"]
        cols = stocksdb["stocks"]

        aab = []
        for x in uscol.find({}, {"_id": 0, "USER ID": 1}): aab.append(x)
        if {"USER ID": member.id} not in aab: uscol.insert_one({"USER ID": member.id, "Coincord": 0, "Orange": 0, "Golden Statue of Statue of Golden": 0,"The Revolutionary": 0})

        c = uscol.find_one({"USER ID": member.id}, {"_id": 0, "Coincord": 1})["Coincord"]
        o = uscol.find_one({"USER ID": member.id}, {"_id": 0, "Orange": 1})["Orange"]
        s = uscol.find_one({"USER ID": member.id}, {"_id": 0, "Golden Statue of Statue of Golden": 1})["Golden Statue of Statue of Golden"]
        t = uscol.find_one({"USER ID": member.id}, {"_id": 0, "The Revolutionary": 1})["The Revolutionary"]
        cca = cols.find_one({"Stock": "Coincord"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        cpa = cols.find_one({"Stock": "Coincord"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        oca = cols.find_one({"Stock": "Orange"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        opa = cols.find_one({"Stock": "Orange"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        sca = cols.find_one({"Stock": "Golden Statue of Statue of Golden"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        spa = cols.find_one({"Stock": "Golden Statue of Statue of Golden"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        tca = cols.find_one({"Stock": "The Revolutionary"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        tpa = cols.find_one({"Stock": "The Revolutionary"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]

        colt = leaugesdb["leagues"]
        b = []
        for x in colt.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
        if {"USER ID": member.id} not in b: colt.insert_one({"USER ID": member.id, "League": "🔰 Challenger 🔰", "Trophies": 0})
        trophy = colt.find_one({"USER ID": member.id}, {"_id": 0, "Trophies": 1})["Trophies"]
        league = colt.find_one({"USER ID": member.id}, {"_id": 0, "League": 1})["League"]

        col2 = fishdb["fish"]
        b = []
        for x in col2.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
        if {"USER ID": member.id} not in b: col2.insert_one({"USER ID": member.id, "USER": str(member), "Fish :fish:": 0, "Shrimp :shrimp:": 0,"Rare Fish :tropical_fish:": 0, "Crab :crab:": 0, "Squid :squid:": 0, "Octopus :octopus:": 0,"Dolphin :dolphin:": 0, "Blowfish :blowfish:": 0, "Lobster :lobster:": 0, "Whale :whale2:": 0,"Shark :shark:": 0, "Crocodile :crocodile:": 0, "Sea Dragon :dragon:": 0,"Mythical Fish <:MythicalFish:892182628717953024>": 0, "Prized Fish": None})

        tf = col2.find_one({"USER ID": member.id}, {"_id": 0, "Prized Fish": 1})["Prized Fish"]

        networth+=c*cca+o*oca+t*tca+s*sca

        for c in col2.find({"USER ID": member.id}, {"_id": 0, "USER ID": 0, "USER": 0}):
            for b in list(c.keys()):
                if c.get(b) != 0 and b != "Prized Fish":
                    networth += c.get(b)*chart.get(b)

        embed = discord.Embed(
            description=f"**<:leaguetrophy:891844638380556319> {trophy} ─ {league}**",
            color=color)
        embed.add_field(name="Coins",
                        value=f'**Wallet:** {pre}{locale.format_string("%d", wallet, grouping=True)}\n**Bank:** {pre}{locale.format_string("%d", bank, grouping=True)}\n**Networth:** {pre}{locale.format_string("%d", networth, grouping=True)}')
        if tf is not None:
            embed.add_field(name="Most Prized Catch", value=f"**{tf}**", inline=False)
        micon = member.default_avatar if not member.avatar else member.avatar.url
        embed.set_author(name=member.name, icon_url=micon)
        embed.set_thumbnail(url=micon)
        await ctx.send(embed=embed)

"""SHOP"""
@commands.command()
@commands.is_owner()
async def shop(ctx, arg=None):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Shop": 1})["Shop"]
    colc.update_one({"Shop": tc}, {"$set": {"Shop": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Shop": 1})["Shop"]
    cold.update_one({"Shop": tcd}, {"$set": {"Shop": tcd + 1}})

    coli = indb["inventory"]
    a = []
    for x in coli.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: coli.insert_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown": 0, ":star: Star": 0,"<:legendarybox:880229601043963905> Legendary Box": 0, "<:mythicalbox:881252527235018753> Mythical Box": 0,":medal: Medal": 0, ":fog: Air": 0, ":tickets: Ticket": 0, ":fishing_pole_and_fish: Fishing Rod":0,"<:biggerfr:898645851461783594> Platinum Fishing Rod":0,":worm: Worm":0})
    tr = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:therevolutionary:865728876546097174> Crown": 1})["<:therevolutionary:865728876546097174> Crown"]
    st = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":star: Star": 1})[":star: Star"]
    fog = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":fog: Air":1})[":fog: Air"]
    medal = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":medal: Medal":1})[":medal: Medal"]
    ticket = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":tickets: Ticket": 1})[":tickets: Ticket"]
    lbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:legendarybox:880229601043963905> Legendary Box": 1})["<:legendarybox:880229601043963905> Legendary Box"]
    mbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:mythicalbox:881252527235018753> Mythical Box": 1})["<:mythicalbox:881252527235018753> Mythical Box"]
    frod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":fishing_pole_and_fish: Fishing Rod": 1})[":fishing_pole_and_fish: Fishing Rod"]
    pfrod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:biggerfr:898645851461783594> Platinum Fishing Rod": 1})["<:biggerfr:898645851461783594> Platinum Fishing Rod"]
    worm = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":worm: Worm": 1})[":worm: Worm"]

    thelist = []
    for a,b in items.items():
        thelist.append(f"**{a} ─ [{pre}{locale.format_string('%d', b[0], grouping=True)}](https://google.com)**\n{b[1]}")
    if arg is None:
        embed=discord.Embed(title="Shop", description="\n\n".join(a for a in thelist),color=color)
        await ctx.send(embed=embed)
    else:
        if arg.lower() == "legendary" or arg.lower() == "legendarybox" or arg.lower() == "lbox":
            if lbox == 0:
                embed = discord.Embed(title="Legendary Box",description=F"Very rare items inside\n\n**BUY ─ [{pre}2,500,000](https://google.com)**\n**SELL** ─ Cannot be sold",color=color)
            else:
                embed = discord.Embed(title=f"Legendary Box **({lbox})**",description=F"Very rare items inside\n\n**BUY ─ [{pre}2,500,000](https://google.com)**\n**SELL** ─ Cannot be sold",color=color)
            embed.add_field(name="Possible Items", value="""
`Trophy`, `Shark`, `Whale`, `Crocodile`, ~~`Christmas Box`~~, `Star`
""")
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/690681407256789012/880238375163007026/573151905513996298.png')
            await ctx.send(embed=embed)
        elif arg.lower() == "mythical" or arg.lower() == "mythicalbox" or arg.lower() == "mbox":
            if mbox == 0:
                embed = discord.Embed(title="Mythical Box",
                                      description=F"Very *mythical* items inside\n\n**BUY ─ [{pre}10,000,000](https://google.com)**\n**SELL** ─ Cannot be sold",
                                      color=color)
            else:
                embed = discord.Embed(title=f"Mythical Box **({mbox})**",
                                      description=F"Very *mythical* items inside\n\n**BUY ─ [{pre}10,000,000](https://google.com)**\n**SELL** ─ Cannot be sold",
                                      color=color)
            embed.add_field(name="Possible Items", value="""
`Trophy`, `Sea Dragon`, `Mythical Fish`, `Air`, `Medal`, `Ticket`, `Crown`
""")
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/690681407256789012/899487183495364608/881252527235018753.png')
            await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def buy(ctx, arg, amount:int=None):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Buy": 1})["Buy"]
    colc.update_one({"Buy": tc}, {"$set": {"Buy": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Buy": 1})["Buy"]
    cold.update_one({"Buy": tcd}, {"$set": {"Buy": tcd + 1}})

    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
    if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    coli = indb["inventory"]
    a = []
    for x in coli.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: coli.insert_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown": 0, ":star: Star": 0,"<:legendarybox:880229601043963905> Legendary Box": 0, "<:mythicalbox:881252527235018753> Mythical Box": 0,":medal: Medal": 0, ":fog: Air": 0, ":tickets: Ticket": 0, ":fishing_pole_and_fish: Fishing Rod":0,"<:biggerfr:898645851461783594> Platinum Fishing Rod":0,":worm: Worm":0})
    tr = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:therevolutionary:865728876546097174> Crown": 1})["<:therevolutionary:865728876546097174> Crown"]
    st = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":star: Star": 1})[":star: Star"]
    fog = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":fog: Air":1})[":fog: Air"]
    medal = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":medal: Medal":1})[":medal: Medal"]
    ticket = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":tickets: Ticket": 1})[":tickets: Ticket"]
    lbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:legendarybox:880229601043963905> Legendary Box": 1})["<:legendarybox:880229601043963905> Legendary Box"]
    mbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:mythicalbox:881252527235018753> Mythical Box": 1})["<:mythicalbox:881252527235018753> Mythical Box"]
    frod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":fishing_pole_and_fish: Fishing Rod": 1})[":fishing_pole_and_fish: Fishing Rod"]
    pfrod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:biggerfr:898645851461783594> Platinum Fishing Rod": 1})["<:biggerfr:898645851461783594> Platinum Fishing Rod"]
    worm = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":worm: Worm": 1})[":worm: Worm"]
    bee = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":bee: Bee": 1})[":bee: Bee"]
    honeypot = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":honey_pot: Honey Pot": 1})[":honey_pot: Honey Pot"]
    seedling = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":seedling: Seedling": 1})[":seedling: Seedling"]
    apple = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":apple: Apple": 1})[":apple: Apple"]

    zx = []
    for x in coli.find({"USER ID":ctx.author.id}, {"_id": 0, "USER ID": 0}): zx.append(x)

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url
    if arg.lower() == "legendary" or arg.lower() == "legendarybox" or arg.lower() == "lbox":
        if amount is None:
            if wallet < 2500000:
                embed=discord.Embed(description=f"You don't have enough for **a Legendary Box <:legendarybox:880229601043963905>** (`{pre}2,500,000`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, "<:legendarybox:880229601043963905> Legendary Box":lbox}, {"$set":{"<:legendarybox:880229601043963905> Legendary Box":lbox+1}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet-2500000}})
                embed = discord.Embed(description=f"You bought **a Legendary Box <:legendarybox:880229601043963905>** for `{pre}2,500,000`",color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        else:
            if wallet < 2500000*amount:
                embed=discord.Embed(description=f"You don't have enough for **{amount} Legendary Boxes <:legendarybox:880229601043963905>** (`{pre}{locale.format_string('%d', 2500000*amount, grouping=True)}`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, "<:legendarybox:880229601043963905> Legendary Box":lbox}, {"$set":{"<:legendarybox:880229601043963905> Legendary Box":lbox+int(amount)}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - 2500000*amount}})
                embed = discord.Embed(description=f'You bought **{amount} Legendary Boxes <:legendarybox:880229601043963905>** for `{pre}{locale.format_string("%d", amount*2500000, grouping=True)}`',color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        await ctx.send(embed=embed)
    elif arg.lower() == "mythical" or arg.lower() == "mythicalbox" or arg.lower() == "mbox":
        if amount is None:
            if wallet < 10000000:
                embed=discord.Embed(description=f"You don't have enough for **a Mythical Box <:mythicalbox:881252527235018753>** (`{pre}10,000,000`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, "<:mythicalbox:881252527235018753> Mythical Box":mbox}, {"$set":{"<:mythicalbox:881252527235018753> Mythical Box":mbox+1}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet-10000000}})
                embed = discord.Embed(description=f"You bought **a Mythical Box <:mythicalbox:881252527235018753>** for `{pre}10,000,000`",color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        else:
            if wallet < 10000000*amount:
                embed=discord.Embed(description=f"You don't have enough for **{amount} Mythical Boxes <:mythicalbox:881252527235018753>** (`{pre}{locale.format_string('%d', 10000000*amount, grouping=True)}`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, "<:mythicalbox:881252527235018753> Mythical Box":mbox}, {"$set":{"<:mythicalbox:881252527235018753> Mythical Box":mbox+int(amount)}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - 10000000*amount}})
                embed = discord.Embed(description=f'You bought **{amount} Mythical Boxes <:mythicalbox:881252527235018753>** for `{pre}{locale.format_string("%d", amount*10000000, grouping=True)}`',color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        await ctx.send(embed=embed)
    elif arg.lower() == "worm":
        if amount is None:
            if wallet < 100:
                embed=discord.Embed(description=f"You don't have enough for **a Worm :worm:` (`{pre}100`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, ":worm: Worm":mbox}, {"$set":{":worm: Worm":worm+1}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet-100}})
                embed = discord.Embed(description=f"You bought **a Worm :worm:** for `{pre}100`",color=color)
                embed.set_author(name="Successful Transaction", icon_url=micon)
        else:
            if wallet < 100*amount:
                embed=discord.Embed(description=f"You don't have enough for **{amount} Worm :worm:** (`{pre}{locale.format_string('%d', 100*amount, grouping=True)}`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, ":worm: Worm":worm}, {"$set":{":worm: Worm":worm+int(amount)}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - 100*amount}})
                embed = discord.Embed(description=f'You bought **{amount} Worm :worm:** for `{pre}{locale.format_string("%d", amount*100, grouping=True)}`',color=color)
                embed.set_author(name="Successful Transaction", icon_url=micon)
        await ctx.send(embed=embed)
    elif arg.lower() == "fishingrod" or arg.lower() == "fishing" or arg.lower() == "frod" or arg.lower() == "fpole":
        if amount is None:
            if wallet < 50000:
                embed=discord.Embed(description=f"You don't have enough for **a Fishing Rod :fishing_pole_and_fish:` (`{pre}50,000`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, ":fishing_pole_and_fish: Fishing Rod":mbox}, {"$set":{":fishing_pole_and_fish: Fishing Rod":frod+1}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet-50000}})
                embed = discord.Embed(description=f"You bought **a Fishing Rod :fishing_pole_and_fish:** for `{pre}50,000`",color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        else:
            if wallet < 50000*amount:
                embed=discord.Embed(description=f"You don't have enough for **{amount} Fishing Rod :fishing_pole_and_fish:** (`{pre}{locale.format_string('%d', 50000*amount, grouping=True)}`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, ":fishing_pole_and_fish: Fishing Rod":frod}, {"$set":{":fishing_pole_and_fish: Fishing Rod":frod+int(amount)}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - 50000*amount}})
                embed = discord.Embed(description=f'You bought **{amount} Fishing Rod :fishing_pole_and_fish:** for `{pre}{locale.format_string("%d", amount*50000, grouping=True)}`',color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        await ctx.send(embed=embed)
    elif arg.lower() == "platinumrod" or arg.lower() == "platinum" or arg.lower() == "prod" or arg.lower() == "ppole":
        if amount is None:
            if wallet < 250000:
                embed=discord.Embed(description=f"You don't have enough for **a Platinum Fishing Rod <:biggerfr:898645851461783594>** (`{pre}250,000`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, "<:biggerfr:898645851461783594> Platinum Fishing Rod":pfrod}, {"$set":{"<:biggerfr:898645851461783594> Platinum Fishing Rod":pfrod+1}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet-250000}})
                embed = discord.Embed(description=f"You bought **a Platinum Fishing Rod <:biggerfr:898645851461783594>** for `{pre}250,000`",color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        else:
            if wallet < 250000*amount:
                embed=discord.Embed(description=f"You don't have enough for **{amount} Platinum Fishing Rod <:biggerfr:898645851461783594>** (`{pre}{locale.format_string('%d', 50000*amount, grouping=True)}`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, "<:biggerfr:898645851461783594> Platinum Fishing Rod":pfrod}, {"$set":{"<:biggerfr:898645851461783594> Platinum Fishing Rod":pfrod+int(amount)}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - 250000*amount}})
                embed = discord.Embed(description=f'You bought **{amount} Platinum Fishing Rod <:biggerfr:898645851461783594>** for `{pre}{locale.format_string("%d", amount*250000, grouping=True)}`',color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        await ctx.send(embed=embed)
    elif arg.lower() == "bee":
        if amount is None:
            if wallet < 50:
                embed=discord.Embed(description=f"You don't have enough for **a Bee :bee:** (`{pre}50`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, ":bee: Bee":mbox}, {"$set":{":bee: Bee":bee+1}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet-50}})
                embed = discord.Embed(description=f"You bought **a Bee :bee:** for `{pre}50`",color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        else:
            if wallet < 50*amount:
                embed=discord.Embed(description=f"You don't have enough for **{amount} Bee :bee:** (`{pre}{locale.format_string('%d', 50*amount, grouping=True)}`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, ":bee: Bee":bee}, {"$set":{":bee: Bee":bee+int(amount)}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - 50*amount}})
                embed = discord.Embed(description=f'You bought **{amount} Bee :bee:** for `{pre}{locale.format_string("%d", amount*50, grouping=True)}`',color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        await ctx.send(embed=embed)
    elif arg.lower() == "seedling":
        if amount is None:
            if wallet < 125000:
                embed=discord.Embed(description=f"You don't have enough for **a Seedling :seedling:** (`{pre}125,000`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, ":seedling: Seedling":mbox}, {"$set":{":seedling: Seedling":seedling+1}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet-125000}})
                embed = discord.Embed(description=f"You bought **a Seedling :seedling:** for `{pre}125,000`",color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        else:
            if wallet < 125000*amount:
                embed=discord.Embed(description=f"You don't have enough for **{amount} Seedling :seedling:** (`{pre}{locale.format_string('%d', 125000*amount, grouping=True)}`)",color=discord.Color.red())
                embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                coli.update_one({"USER ID": ctx.author.id, ":seedling: Seedling":frod}, {"$set":{":seedling: Seedling":seedling+int(amount)}})
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - 125000*amount}})
                embed = discord.Embed(description=f'You bought **{amount} Seedling :seedling:** for `{pre}{locale.format_string("%d", amount*125000, grouping=True)}`',color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        await ctx.send(embed=embed)

    """
    elif arg.lower() == "christmas" or arg.lower() == "christmasbox" or arg.lower() == "cbox":
        if amount is None:
            if wallet < 500000:
                embed=discord.Embed(description=f"You don't have enough for **a Christmas Box <:christmasbox:881252565503868958>` (`{pre}500,000`)")
            else:
                if "<:christmasbox:881252565503868958> Christmas Box" not in idb[str(ctx.author.id)].keys():
                    idb[str(ctx.author.id)]["<:christmasbox:881252565503868958> Christmas Box"] = 0
                idb[str(ctx.author.id)]["<:christmasbox:881252565503868958> Christmas Box"] += 1
                with open('inventory.json', 'w') as f:
                    json.dump(idb, f, indent=4)
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet-500000}})
                embed = discord.Embed(description=f"You bought **a Christmas Box <:christmasbox:881252565503868958>` for `{pre}500,000`",color=color)
                embed.set_author(name="Successful Transaction", icon_url=micon)
            await ctx.send(embed=embed)
        else:
            if wallet < 500000*amount:
                embed=discord.Embed(description=f"You don't have enough for **{amount} Christmas Boxes <:christmasbox:881252565503868958>` (`{pre}{locale.format_string('%d', 500000*amount, grouping=True)}`)")
            else:
                if "<:christmasbox:881252565503868958> Christmas Box" not in idb[str(ctx.author.id)].keys():
                    idb[str(ctx.author.id)]["<:christmasbox:881252565503868958> Christmas Box"] = 0
                idb[str(ctx.author.id)]["<:christmasbox:881252565503868958> Christmas Box"] += amount
                with open('inventory.json', 'w') as f:
                    json.dump(idb, f, indent=4)
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - 500000*amount}})
                embed = discord.Embed(description=f'You bought **{amount} Christmas Boxes <:christmasbox:881252565503868958>` for `{pre}{locale.format_string("%d", amount*500000, grouping=True)}`',color=color)
                embed.set_author(name="Successful Transaction", icon_url=micon)
            await ctx.send(embed=embed)
    """
@commands.command()
@commands.is_owner()
async def use(ctx, arg, amount:int=None):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Use": 1})["Use"]
    colc.update_one({"Use": tc}, {"$set": {"Use": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Use": 1})["Use"]
    cold.update_one({"Use": tcd}, {"$set": {"Use": tcd + 1}})

    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
    if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    coli = indb["inventory"]
    a = []
    for x in coli.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: coli.insert_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown": 0, ":star: Star": 0,"<:legendarybox:880229601043963905> Legendary Box": 0, "<:mythicalbox:881252527235018753> Mythical Box": 0,":medal: Medal": 0, ":fog: Air": 0, ":tickets: Ticket": 0, ":fishing_pole_and_fish: Fishing Rod":0,"<:biggerfr:898645851461783594> Platinum Fishing Rod":0,":worm: Worm":0})
    tr = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:therevolutionary:865728876546097174> Crown": 1})["<:therevolutionary:865728876546097174> Crown"]
    st = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":star: Star": 1})[":star: Star"]
    fog = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":fog: Air":1})[":fog: Air"]
    medal = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":medal: Medal":1})[":medal: Medal"]
    ticket = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":tickets: Ticket": 1})[":tickets: Ticket"]
    lbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:legendarybox:880229601043963905> Legendary Box": 1})["<:legendarybox:880229601043963905> Legendary Box"]
    mbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:mythicalbox:881252527235018753> Mythical Box": 1})["<:mythicalbox:881252527235018753> Mythical Box"]
    frod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":fishing_pole_and_fish: Fishing Rod": 1})[":fishing_pole_and_fish: Fishing Rod"]
    pfrod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:biggerfr:898645851461783594> Platinum Fishing Rod": 1})["<:biggerfr:898645851461783594> Platinum Fishing Rod"]
    st = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":worm: Worm": 1})[":worm: Worm"]

    colf = fishdb["fish"]
    ab = []
    for x in colf.find({}, {"_id": 0, "USER ID": 1}): ab.append(x)
    if {"USER ID": ctx.author.id} not in ab: colf.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Fish :fish:": 0, "Shrimp :shrimp:": 0,"Rare Fish :tropical_fish:": 0, "Crab :crab:": 0, "Squid :squid:": 0, "Octopus :octopus:": 0,"Dolphin :dolphin:": 0, "Blowfish :blowfish:": 0, "Lobster :lobster:": 0, "Whale :whale2:": 0,"Shark :shark:": 0, "Crocodile :crocodile:": 0, "Sea Dragon :dragon:": 0,"Mythical Fish <:MythicalFish:892182628717953024>": 0, "Prized Fish": None})

    colt = leaugesdb["leagues"]
    b = []
    for x in colt.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colt.insert_one({"USER ID": ctx.author.id, "League": "🔰 Challenger 🔰", "Trophies": 0})
    trophye = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Trophies": 1})["Trophies"]
    league = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "League": 1})["League"]

    if arg.lower() == "legendary" or arg.lower() == "legendarybox" or arg.lower() == "lbox":
        if lbox == 0:
            embed=discord.Embed(description=f"You have no **Legendary Boxes <:legendarybox:880229601043963905>**",color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
            await ctx.send(embed=embed)
        else:
            if amount is not None:
                if amount > lbox:
                    embed=discord.Embed(description=f"You do not have **{amount} Legendary Boxes <:legendarybox:880229601043963905>**. You have `{lbox}`", color=color)
                    embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
                    await ctx.send(embed=embed)
                    tam=None
                else:
                    tam = amount
            else:
                tam = 1
            if tam is not None:
                coli.update_one({"USER ID": ctx.author.id, "<:legendarybox:880229601043963905> Legendary Box":lbox}, {"$set":{"<:legendarybox:880229601043963905> Legendary Box":lbox-tam}})

                coins = 0
                item = {"Trophy <:leaguetrophy:891844638380556319>": 0, "Shark :shark:": 0, "Star :star:": 0,"Whale :whale2:": 0, "Crocodile :crocodile:": 0}
                for i in range(tam):
                    choice = random.randint(1, 4)
                    coins += random.randint(55555, 300000)
                    trophy2 = random.randint(100,500)
                    samount = random.randint(10, 100)
                    famount = random.randint(1, 10)
                    item["Trophy <:leaguetrophy:891844638380556319>"] += trophy2
                    if choice == 1:
                        item["Star :star:"] +=samount
                    elif choice == 2:
                        item["Shark :shark:"] += famount
                    elif choice == 3:
                        item["Whale :whale2:"] += famount
                    else:
                        item["Crocodile :crocodile:"] += famount

                trophy = item.get('Trophy <:leaguetrophy:891844638380556319>')

                item2 = []
                for b in list(item.keys()):
                    if item.get(b) == 0:
                        pass
                    elif b == "Trophy <:leaguetrophy:891844638380556319>":
                        colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye},{"$set": {"Trophies": trophye + trophy}})
                    else:
                        item2.append(f"**{b}** ─ **`{item.get(b)}`**")

                    if b == "Shark :shark:" or b == "Whale :whale2:":
                        tf = colf.find_one({"USER ID": ctx.author.id}, {"_id": 0, f"{b}": 1})[f"{b}"]
                        colf.update_one({"USER ID": ctx.author.id, f"{b}": item.get(b)},{"$set": {f"{b}": item.get(b) + tf}})
                    elif b == "Trophy <:leaguetrophy:891844638380556319>":
                        colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye}, {"$set": {"Trophies": trophye+trophy}})
                    else:
                        coli.update_one({"USER ID": ctx.author.id, ":star: Star": st},{"$set": {":star: Star": st + item.get('Star :star:')}})

                embed = discord.Embed(
                    description=f'Opening **{tam} Legendary Boxes <:legendarybox:880229601043963905>...**',
                    color=color)
                message = await ctx.reply(embed=embed)
                time.sleep(2)
                embed2 = discord.Embed(title=f"Box Contents",description=f"**{pre}{locale.format_string('%d', coins, grouping=True)}**\n**<:leaguetrophy:891844638380556319> Trophy ─ `{trophy}`**\n\n" + "\n".join(a for a in item2), color=color)
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet + coins}})
                await message.edit(embed=embed2)
                if trophye + trophy >= 250 and trophye + trophy < 500 and "Novice" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🛡️ Novice Tier 🛡️"}})
                elif trophye + trophy >= 500 and trophye + trophy < 1000 and "Gold" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🔱 Gold Tier 🔱"}})
                elif trophye + trophy >= 1000 and trophye + trophy < 2000 and "Purple Dragon" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "⚜️Purple Dragon Tier ⚜️"}})
                elif trophye + trophy >= 2000 and trophye + trophy < 3000 and "Diamond" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "💎 Diamond Tier 💎"}})
                elif trophye + trophy >= 3000 and trophye + trophy < 4500 and "Master" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "⚔️ Master Tier ⚔️"}})
                elif trophye + trophy >= 4500 and trophye + trophy < 5000 and "Legendary" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🃏 Legendary Tier 🃏"}})
                elif trophye + trophy >= 5000 and "The Best of the Best" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🏴‍☠️ The Best of the Best 🏴‍☠️"}})
    elif arg.lower() == "mythical" or arg.lower() == "mythicalbox" or arg.lower() == "mbox":
        if mbox == 0:
            embed = discord.Embed(description=f"You have no **Mythical Boxes <:mythicalbox:881252527235018753>**",
                                  color=color)
            embed.set_author(name='Warning',
                             icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
            await ctx.send(embed=embed)
        else:
            if amount is not None:
                if amount > mbox:
                    embed = discord.Embed(
                        description=f"You do not have **{amount} Mythical Boxes <:mythicalbox:881252527235018753>**. You have `{mbox}`",
                        color=color)
                    embed.set_author(name='Warning',
                                     icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
                    await ctx.send(embed=embed)
                    tam=None
                else:
                    tam = amount
            else:
                tam = 1
            if tam is not None:
                coli.update_one({"USER ID": ctx.author.id, "<:mythicalbox:881252527235018753> Mythical Box": mbox},{"$set": {"<:mythicalbox:881252527235018753> Mythical Box": mbox - tam}})

                coins = 0
                item = {"Trophy <:leaguetrophy:891844638380556319>": 0, "Sea Dragon :dragon:": 0,"Mythical Fish <:MythicalFish:892182628717953024>": 0, "Star :star:": 0,"Crown <:therevolutionary:865728876546097174>": 0, "Air :fog:": 0, "Medal :medal:": 0,"Ticket :ticket:": 0}
                for i in range(tam):
                    choice = random.randint(1, 7)
                    coins += random.randint(500000, 3000000)
                    trophy2 = random.randint(250, 1000)
                    samount = random.randint(100, 500)
                    aamount = random.randint(1, 5)
                    mamount = random.randint(1, 5)
                    tamount = random.randint(1,2)
                    famount = random.randint(10, 100)
                    item["Trophy <:leaguetrophy:891844638380556319>"] += trophy2
                    if choice == 1:
                        item["Sea Dragon :dragon:"] += famount
                    elif choice == 2:
                        item["Mythical Fish <:MythicalFish:892182628717953024>"] += famount
                    elif choice == 3:
                        item["Star :star:"] += samount
                    elif choice == 4:
                        item["Crown <:therevolutionary:865728876546097174>"] += famount
                    elif choice == 5:
                        item["Air :fog:"] += aamount
                    elif choice == 6:
                        item["Medal :medal:"] += mamount
                    else:
                        item["Ticket :ticket:"] += tamount
                trophy = item.get('Trophy <:leaguetrophy:891844638380556319>')

                item2 = []
                for b in list(item.keys()):
                    if item.get(b) == 0:
                        pass
                    elif b == "Trophy <:leaguetrophy:891844638380556319>":
                        colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye},{"$set": {"Trophies": trophye + trophy}})
                    else:
                        item2.append(f"**{b}** ─ **`{item.get(b)}`**")

                        if b == "Sea Dragon :dragon:" or b == "Mythical Fish <:MythicalFish:892182628717953024>":
                            tf = colf.find_one({"USER ID": ctx.author.id}, {"_id": 0, f"{b}": 1})[f"{b}"]
                            colf.update_one({"USER ID": ctx.author.id, f"{b}": tf},{"$set": {f"{b}": item.get(b) + tf}})
                        elif b == "Crown <:therevolutionary:865728876546097174>":
                            coli.update_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown": tr},{"$set": {"<:therevolutionary:865728876546097174> Crown": tr + item.get('Crown <:therevolutionary:865728876546097174>')}})
                        elif b == "Air :fog:":
                            coli.update_one({"USER ID": ctx.author.id, ":fog: Air": fog},{"$set": {":fog: Air": fog + item.get('Air :fog:')}})
                        elif b == "Medal :medal:":
                            coli.update_one({"USER ID": ctx.author.id, ":medal: Medal": medal},{"$set": {":medal: Medal": medal + item.get('Medal :medal:')}})
                        else:
                            coli.update_one({"USER ID": ctx.author.id, ":star: Star": st},{"$set": {":star: Star": st + item.get('Star :star:')}})
                embed = discord.Embed(
                    description=f'Opening **{tam} Mythical Boxes <:mythicalbox:881252527235018753>...**',
                    color=color)
                message = await ctx.reply(embed=embed)
                time.sleep(2)
                embed2 = discord.Embed(title=f"Box Contents",
                                       description=f"**{pre}{locale.format_string('%d', coins, grouping=True)}**\n**<:leaguetrophy:891844638380556319> Trophy ─ `{trophy}`**\n\n" + "\n".join(a for a in item2), color=color)
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + coins}})
                await message.edit(embed=embed2)
                if trophye + trophy >= 250 and trophye + trophy < 500 and "Novice" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🛡️ Novice Tier 🛡️"}})
                elif trophye + trophy >= 500 and trophye + trophy < 1000 and "Gold" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🔱 Gold Tier 🔱"}})
                elif trophye + trophy >= 1000 and trophye + trophy < 2000 and "Purple Dragon" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "⚜️Purple Dragon Tier ⚜️"}})
                elif trophye + trophy >= 2000 and trophye + trophy < 3000 and "Diamond" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "💎 Diamond Tier 💎"}})
                elif trophye + trophy >= 3000 and trophye + trophy < 4500 and "Master" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "⚔️ Master Tier ⚔️"}})
                elif trophye + trophy >= 4500 and trophye + trophy < 5000 and "Legendary" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🃏 Legendary Tier 🃏"}})
                elif trophye + trophy >= 5000 and "The Best of the Best" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🏴‍☠️ The Best of the Best 🏴‍☠️"}})
@commands.command(aliases=["myinv"])
async def inventory(ctx):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Inventory": 1})["Inventory"]
    colc.update_one({"Inventory": tc}, {"$set": {"Inventory": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Inventory": 1})["Inventory"]
    cold.update_one({"Inventory": tcd}, {"$set": {"Inventory": tcd + 1}})

    coli = indb["inventory"]
    a = []
    for x in coli.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: coli.insert_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown": 0, ":star: Star": 0,"<:legendarybox:880229601043963905> Legendary Box": 0, "<:mythicalbox:881252527235018753> Mythical Box": 0,":medal: Medal": 0, ":fog: Air": 0, ":tickets: Ticket": 0})
    tr = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:therevolutionary:865728876546097174> Crown": 1})["<:therevolutionary:865728876546097174> Crown"]
    st = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":star: Star": 1})[":star: Star"]
    fog = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":fog: Air":1})[":fog: Air"]
    medal = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":medal: Medal":1})[":medal: Medal"]
    ticket = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":tickets: Ticket": 1})[":tickets: Ticket"]
    lbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:legendarybox:880229601043963905> Legendary Box": 1})["<:legendarybox:880229601043963905> Legendary Box"]
    mbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:mythicalbox:881252527235018753> Mythical Box": 1})["<:mythicalbox:881252527235018753> Mythical Box"]

    final = []
    for c in coli.find({"USER ID": ctx.author.id}, {"_id": 0, "USER ID": 0}):
        for b in list(c.keys()):
            if c.get(b) != 0:
                final.append(f"**{b}** ─ {c.get(b)}")
    col = fishdb["fish"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Fish :fish:": 0, "Shrimp :shrimp:": 0,"Rare Fish :tropical_fish:": 0, "Crab :crab:": 0, "Squid :squid:": 0, "Octopus :octopus:": 0,"Dolphin :dolphin:": 0, "Blowfish :blowfish:": 0, "Lobster :lobster:": 0, "Whale :whale2:": 0,"Shark :shark:": 0, "Crocodile :crocodile:": 0, "Sea Dragon :dragon:": 0,"Mythical Fish <:MythicalFish:892182628717953024>": 0, "Prized Fish": None})

    final2 = []
    for c in col.find({"USER ID": ctx.author.id}, {"_id": 0, "USER ID": 0, "USER": 0}):
        for b in list(c.keys()):
            if c.get(b) != 0 and b != "Prized Fish":
                final2.append(f"**{b}** ─ {c.get(b)}")
    if len(final) == 0 and len(final2) == 0:
        embed = discord.Embed(description="You don't have any items or fish",color=discord.Color.red())
        embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
    else:
        micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url
        if ctx.author.color == discord.Color.from_rgb(0, 0, 0):
            c = discord.Color.from_rgb(47, 49, 54)
        else:
            c = ctx.author.color
        embed = discord.Embed(color=c)
        embed.set_author(name=f"{ctx.author.name}'s Inventory", icon_url=micon)
        if len(final) != 0:
            embed.add_field(name="Items", value='\n'.join(a for a in final))
        if len(final2) != 0:
            embed.add_field(name="Fish", value='\n'.join(a for a in final2))
    await ctx.send(embed=embed)

"""LEAGUES"""
@commands.command()
@commands.is_owner()
async def leagues(ctx):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Leauges": 1})["Leauges"]
    colc.update_one({"Leauges": tc}, {"$set": {"Leauges": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Leauges": 1})["Leauges"]
    cold.update_one({"Leauges": tcd}, {"$set": {"Leauges": tcd + 1}})

    colt = leaugesdb["leagues"]
    b = []
    for x in colt.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colt.insert_one({"USER ID": ctx.author.id, "USER":str(ctx.author),"League": "🔰 Challenger 🔰", "Trophies": 0})
    trophy = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Trophies": 1})["Trophies"]
    league = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "League": 1})["League"]

    embed=discord.Embed(title="Leagues", description=f"<:leaguetrophy:891844638380556319> **0 ─ :beginner: Challenger Tier :beginner:**\n<:leaguetrophy:891844638380556319> **250 ─ :shield: Novice Tier :shield:**\n<:leaguetrophy:891844638380556319> **500 ─ :trident: Gold Tier :trident:**\n<:leaguetrophy:891844638380556319> **1000 ─ :fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**\n<:leaguetrophy:891844638380556319> **2000 ─ :gem: Diamond Tier :gem:**\n<:leaguetrophy:891844638380556319> **3000 ─ :crossed_swords: Master Tier :crossed_swords:**\n<:leaguetrophy:891844638380556319> **4500 ─ :black_joker: Legendary Tier :black_joker:**\n<:leaguetrophy:891844638380556319> **5000+ ─ :pirate_flag: The Best of the Best :pirate_flag:**\n<:leaguetrophy:891844638380556319> **???? ─ <:empty:880143730076688495> ???? <:empty:880143730076688495>**",color=color)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/690681407256789012/879794231156277308/751701583414165516.png')
    embed.set_footer(text=f"Your league: {league}")
    await ctx.send(embed=embed)

"""STOCKS"""
@commands.command(aliases=["stocks"])
async def stock(ctx, stock=None, action=None, amount=None):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Stocks": 1})["Stocks"]
    colc.update_one({"Stocks": tc}, {"$set": {"Stocks": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Stocks": 1})["Stocks"]
    cold.update_one({"Stocks": tcd}, {"$set": {"Stocks": tcd + 1}})

    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
    if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    cols = stocksdb["stocks"]
    cca = cols.find_one({"Stock":"Coincord"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
    cpa = cols.find_one({"Stock":"Coincord"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
    oca = cols.find_one({"Stock":"Orange"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
    opa = cols.find_one({"Stock":"Orange"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
    sca = cols.find_one({"Stock":"Golden Statue of Statue of Golden"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
    spa = cols.find_one({"Stock":"Golden Statue of Statue of Golden"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
    tca = cols.find_one({"Stock":"The Revolutionary"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
    tpa = cols.find_one({"Stock":"The Revolutionary"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
    reset = cols.find_one({"Stock":"Reset"}, {"_id": 0, "Reset": 1})["Reset"]

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

    uscol = stocksdb["userstock"]
    aab = []
    for x in uscol.find({}, {"_id": 0, "USER ID": 1}): aab.append(x)
    if {"USER ID": ctx.author.id} not in aab: uscol.insert_one({"USER ID": ctx.author.id, "Coincord": 0, "Orange": 0, "Golden Statue of Statue of Golden": 0,"The Revolutionary": 0})
    c = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Coincord": 1})["Coincord"]
    o = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Orange": 1})["Orange"]
    s = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Golden Statue of Statue of Golden": 1})["Golden Statue of Statue of Golden"]
    t = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "The Revolutionary": 1})["The Revolutionary"]

    cols = serverdb["serverdb"]
    aa = []
    for x in cols.find({}, {"_id": 0, "GUILD ID": 1}): aa.append(x)
    if {"GUILD ID": ctx.author.guild.id} not in aa: cols.insert_one({"GUILD ID": ctx.author.guild.id, "Prefix": None, "Mute Role": None, "Total Commands": 0, "Total Messages": 0})
    theprefix = cols.find_one({"GUILD ID": ctx.author.guild.id}, {"_id": 0, "Prefix": 1})["Prefix"]
    if theprefix is None: theprefix = default_prefix

    if cca > cpa:
        if cca >= cpa * 2:
            ec = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**'
        else:
            ec = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**'
    elif cca == cpa:
        ec = f'**No Change** [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
    else:
        ec = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▼ {pre}{locale.format_string("%d", cpa - cca, grouping=True)} `(▼ {(cpa - cca) / cpa * 100:.2f}%)`**'

    if oca > opa:
        if oca >= opa * 2:
            oc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**'
        else:
            oc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**'
    elif oca == opa:
        oc = f'**No Change** [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
    else:
        oc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▼ {pre}{locale.format_string("%d", opa - oca, grouping=True)} `(▼ {(opa - oca) / opa * 100:.2f}%)`**'

    if sca > spa:
        if sca >= spa * 2:
            sc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", sca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", sca - spa, grouping=True)} `(▲ {(sca - spa) / spa * 100:.2f}%)`**'
        else:
            sc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", sca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", sca - spa, grouping=True)} `(▲ {(sca - spa) / spa * 100:.2f}%)`**'
    elif sca == spa:
        sc = f'**No Change** [{pre}{locale.format_string("%d", sca, grouping=True)} / orange](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
    else:
        sc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", sca, grouping=True)} / orange](https://google.com) ─ **▼ {pre}{locale.format_string("%d", spa - sca, grouping=True)} `(▼ {(spa - sca) / spa * 100:.2f}%)`**'

    if stock is None:
        embed=discord.Embed(title="Available Stocks", description=f"\n**Coincord :coin:**\n{ec}\nA beautiful coin. Pretty useless, but they might be worth a fortune\n\n**Golden Statue of Statue of Golden <:gsosg:897599783785619487>**\n{sc}\nA golden statue that is a statue of gold\n\n**Orange :tangerine:**\n{oc}\nA fresh orange orange. You can use it to flex to your friends.",color=color)
        mview = stockselect(timeout=15)
        out = await ctx.send(f"```yaml\nSyntax: {theprefix}stocks [Choice] [Buy/Sell] [Amount]\n\nTo view your current stocks: {theprefix}mystocks\n\nStocks last reset on [{reset}]```",embed=embed, file=None, view=mview)
        mview.user = ctx.author.id
        mview.response = out
    else:
        if stock.lower() == "coincord" or stock.lower() == "cc":
            if action is None:
                file = discord.File("C:/Users/Hao/PycharmProjects/master/coincord.png", filename="coincord.png")
                embed = discord.Embed(title="Coincord",description=f"A beautiful coin. Pretty useless, but they might be worth a fortune\n```yaml\nSyntax: {theprefix}stocks cc buy/sell [amount]```\n**Stats:**\n{ec}\n```yaml\nLast Updated: {reset}```",color=color)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/868290623394947102/875194040600133632/1fa99.png')
                embed.set_image(url='attachment://coincord.png')
                embed.set_footer(text="stonks")
                await ctx.send(file=file, embed=embed)
            else:
                if amount is None:
                    if action.lower() == "buy":
                        if wallet < cca:
                            embed = discord.Embed(description=f"You don't have enough for **a coin :coin:** (`{pre}{locale.format_string('%d', cca, grouping=True)}`)", color=discord.Color.red())
                            embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                        else:
                            uscol.update_one({"USER ID": ctx.author.id, "Coincord":c},{"$set":{"Coincord":c+1}})
                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - cca}})

                            embed = discord.Embed(description=f"You bought **a coin :coin:** for `{pre}{locale.format_string('%d', cca, grouping=True)}`",color=discord.Color.green())
                            embed.set_author(name="Successful Transaction", icon_url=micon)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if int(c) == 0:
                            embed = discord.Embed(description="You have no coins :coin:",color=discord.Color.red())
                            embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                        else:
                            uscol.update_one({"USER ID": ctx.author.id, "Coincord":c},{"$set":{"Coincord":c-1}})
                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet + cca}})

                            embed = discord.Embed(description=f":tada: You sold **a coin :coin:** and got `{pre}{locale.format_string('%d', cca, grouping=True)}`",color=discord.Color.green())
                            embed.set_author(name="Successful Transaction", icon_url=micon)
                        await ctx.send(embed=embed)
                else:
                    if action.lower() == "buy":
                        if wallet < cca * int(amount):
                            embed = discord.Embed(description=f"You don't have enough for **{amount} coins :coin:** (`{pre}{locale.format_string('%d', cca*int(amount), grouping=True)}`)", color=discord.Color.red())
                            embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                        else:
                            uscol.update_one({"USER ID": ctx.author.id, "Coincord":c},{"$set":{"Coincord":c+int(amount)}})
                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - cca*int(amount)}})

                            embed=discord.Embed(description=f"You bought **{amount} coins :coin:** for `{pre}{locale.format_string('%d', cca*int(amount), grouping=True)}`",color=discord.Color.green())
                            embed.set_author(name="Successful Transaction", icon_url=micon)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if amount.isnumeric() == True:
                            if int(c) == 0:
                                embed = discord.Embed(description="You have no coins :coin:",color=discord.Color.red())
                                embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                            else:
                                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + cca*int(amount)}})
                                uscol.update_one({"USER ID": ctx.author.id, "Coincord":c},{"$set":{"Coincord":c-int(amount)}})

                                embed = discord.Embed(description=f":tada: You sold **{int(amount)} coins :coin:** and got `{pre}{locale.format_string('%d', cca*int(amount), grouping=True)}`",color=discord.Color.green())
                                embed.set_author(name="Successful Transaction", icon_url=micon)
                            await ctx.send(embed=embed)
                        else:
                            if amount.lower() == "all" or amount.lower() == "max":
                                if int(c) == 0:
                                    embed = discord.Embed(description="You have no coins :coin:",color=color)
                                else:
                                    uscol.update_one({"USER ID": ctx.author.id, "Coincord": c},{"$set": {"Coincord": 0}})
                                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + cca*c}})

                                    embed = discord.Embed(description=f":tada: You sold **{c} coins :coin:** and got `{pre}{locale.format_string('%d', cca * c, grouping=True)}`",color=discord.Color.green())
                                    embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                                await ctx.send(embed=embed)
        elif stock.lower() == "orange" or stock.lower() == "o":
            if action is None:
                file = discord.File("C:/Users/Hao/PycharmProjects/master/orange.png", filename="orange.png")
                embed = discord.Embed(title="Orange",description=f"A fresh orange orange. You can use it to flex to your friends.\n```yaml\nSyntax: {theprefix}stocks o buy/sell [amount]```\n**Stats:**\n{oc}\n```yaml\nLast Updated: {reset}```",color=color)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/868290623394947102/875196175286943744/orange-emoji-by-twitter.png')
                embed.set_image(url='attachment://orange.png')
                embed.set_footer(text="stonks")
                await ctx.send(file=file, embed=embed)
            else:
                if amount is None:
                    if action.lower() == "buy":
                        if wallet < oca:
                            embed = discord.Embed(description=f"You don't have enough for **an orange :tangerine:** (`{pre}{locale.format_string('%d', oca, grouping=True)}`)", color=discord.Color.red())
                            embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                        else:
                            uscol.update_one({"USER ID": ctx.author.id, "Orange":o},{"$set":{"Orange":c+1}})
                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - oca}})

                            embed = discord.Embed(description=f"You bought **an orange :tangerine:** for `{pre}{locale.format_string('%d', oca, grouping=True)}`",color=discord.Color.green())
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if int(o) == 0:
                            embed = discord.Embed(description="You have no oranges :tangerine:",color=discord.Color.red())
                            embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                        else:
                            uscol.update_one({"USER ID": ctx.author.id, "Orange":o},{"$set":{"Orange":c-1}})
                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + oca}})

                            embed = discord.Embed(description=f":tada: You sold **an orange :tangerine:** and got `{pre}{locale.format_string('%d', oca, grouping=True)}`",color=discord.Color.green())
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                else:
                    if action.lower() == "buy":
                        if wallet < oca * int(amount):
                            embed = discord.Embed(description=f"You don't have enough for **{amount} oranges :tangerine:** (`{pre}{locale.format_string('%d', oca*int(amount), grouping=True)}`)", color=discord.Color.red())
                            embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                        else:
                            uscol.update_one({"USER ID": ctx.author.id, "Orange":o},{"$set":{"Orange":c+int(amount)}})
                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - oca*int(amount)}})

                            embed=discord.Embed(description=f"You bought **{amount} oranges :tangerine:** for `{pre}{locale.format_string('%d', oca*int(amount), grouping=True)}`",color=discord.Color.green())
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if amount.isnumeric() == True:
                            if int(o) == 0:
                                embed = discord.Embed(description="You have no oranges :tangerine:",color=discord.Color.red())
                                embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                            else:
                                uscol.update_one({"USER ID": ctx.author.id, "Orange": o},{"$set": {"Orange": c - int(amount)}})
                                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + oca*int(amount)}})

                                embed = discord.Embed(description=f":tada: You sold **{int(amount)} oranges :tangerine:** and got `{pre}{locale.format_string('%d', oca*int(amount), grouping=True)}`",color=discord.Color.green())
                                embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                            await ctx.send(embed=embed)
                        else:
                            if amount.lower() == "all" or amount.lower() == "max":
                                if int(o) == 0:
                                    embed = discord.Embed(description="You have no oranges :tangerine:",color=discord.Color.red())
                                    embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                                else:
                                    uscol.update_one({"USER ID": ctx.author.id, "Orange": o}, {"$set": {"Orange": 0}})
                                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + oca*o}})

                                    embed = discord.Embed(description=f":tada: You sold **{o} oranges :tangerine:** and got `{pre}{locale.format_string('%d', oca * o, grouping=True)}`",color=discord.Color.green())
                                    embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                                await ctx.send(embed=embed)
        elif stock.lower() == "golden" or stock.lower() == "g" or stock.lower() == "statue" or stock.lower() == "goldenstatue":
            if action is None:
                file = discord.File("C:/Users/Hao/PycharmProjects/master/gsosog.png", filename="gsosog.png")
                embed = discord.Embed(title="Golden Statue of Statue of Golden",description=f"A golden statue that is a statue of gold.\n```yaml\nSyntax: {theprefix}stocks statue buy/sell [amount]```\n**Stats:**\n{sc}\n```yaml\nLast Updated: {reset}```",color=color)
                embed.set_image(url='attachment://gsosog.png')
                embed.set_footer(text="stonks")
                await ctx.send(file=file, embed=embed)
            else:
                if amount is None:
                    if action.lower() == "buy":
                        if wallet < sca:
                            embed = discord.Embed(description=f"You don't have enough for **an statue** (`{pre}{locale.format_string('%d', sca, grouping=True)}`)", color=discord.Color.red())
                            embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                        else:
                            uscol.update_one({"USER ID": ctx.author.id, "Golden Statue of Statue of Golden":s},{"$set":{"Golden Statue of Statue of Golden":s+1}})
                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet - sca}})

                            embed = discord.Embed(description=f"You bought **an statue** for `{pre}{locale.format_string('%d', sca, grouping=True)}`",color=discord.Color.green())
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if int(s) == 0:
                            embed = discord.Embed(description="You have no statues",color=discord.Color.red())
                            embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                        else:
                            uscol.update_one({"USER ID": ctx.author.id, "Golden Statue of Statue of Golden":s},{"$set":{"Golden Statue of Statue of Golden":s-1}})
                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + sca}})

                            embed = discord.Embed(description=f":tada: You sold **an statue** and got `{pre}{locale.format_string('%d', sca, grouping=True)}`",color=discord.Color.green())
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                else:
                    if action.lower() == "buy":
                        if wallet < sca * int(amount):
                            embed = discord.Embed(description=f"You don't have enough for **{amount} statues** (`{pre}{locale.format_string('%d', sca*int(amount), grouping=True)}`)", color=discord.Color.red())
                            embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                        else:
                            uscol.update_one({"USER ID": ctx.author.id, "Golden Statue of Statue of Golden":s},{"$set":{"Golden Statue of Statue of Golden":s+int(amount)}})
                            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - sca*int(amount)}})

                            embed=discord.Embed(description=f"You bought **{amount} statues** for `{pre}{locale.format_string('%d', sca*int(amount), grouping=True)}`",color=discord.Color.green())
                            embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                        await ctx.send(embed=embed)
                    elif action.lower() == "sell":
                        if amount.isnumeric() == True:
                            if int(s) == 0:
                                embed = discord.Embed(description="You have no statues",color=discord.Color.red())
                                embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                            else:
                                uscol.update_one({"USER ID": ctx.author.id, "Golden Statue of Statue of Golden": s},{"$set": {"Golden Statue of Statue of Golden": s - int(amount)}})
                                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + sca*int(amount)}})

                                embed = discord.Embed(description=f":tada: You sold **{int(amount)} statues** and got `{pre}{locale.format_string('%d', sca*int(amount), grouping=True)}`",color=discord.Color.green())
                                embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
                            await ctx.send(embed=embed)
                        else:
                            if amount.lower() == "all" or amount.lower() == "max":
                                if int(s) == 0:
                                    embed = discord.Embed(description="You have no statues",color=discord.Color.red())
                                    embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                                else:
                                    uscol.update_one({"USER ID": ctx.author.id, "Golden Statue of Statue of Golden": s},{"$set": {"Golden Statue of Statue of Golden": 0}})
                                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + sca*s}})

                                    embed = discord.Embed(description=f":tada: You sold **{s} statues** and got `{pre}{locale.format_string('%d', sca * s, grouping=True)}`",color=discord.Color.green())
                                    embed.set_author(name="Successful Transaction", icon_url=ctx.author.avatar)
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

    @discord.ui.select(placeholder="Filter...", min_values=1, max_values=1, options = [discord.SelectOption(label="Cheap", value="cheap", emoji="🪙"),discord.SelectOption(label="Expensive", value="expensive", emoji="🍊")])
    async def select(self, select:discord.ui.Select, interaction:discord.Interaction):

        cols = serverdb["serverdb"]
        aa = []
        for x in cols.find({}, {"_id": 0, "GUILD ID": 1}): aa.append(x)
        if {"GUILD ID": interaction.guild.id} not in aa: cols.insert_one({"GUILD ID": interaction.guild.id, "Prefix": None, "Mute Role": None, "Total Commands": 0,"Total Messages": 0})
        theprefix = cols.find_one({"GUILD ID": interaction.guild.id}, {"_id": 0, "Prefix": 1})["Prefix"]

        if theprefix is None: theprefix = default_prefix

        cols = stocksdb["stocks"]
        cca = cols.find_one({"Stock": "Coincord"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        cpa = cols.find_one({"Stock": "Coincord"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        oca = cols.find_one({"Stock": "Orange"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        opa = cols.find_one({"Stock": "Orange"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        sca = cols.find_one({"Stock": "Golden Statue of Statue of Golden"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        spa = cols.find_one({"Stock": "Golden Statue of Statue of Golden"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        tca = cols.find_one({"Stock": "The Revolutionary"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
        tpa = cols.find_one({"Stock": "The Revolutionary"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
        reset = cols.find_one({"Stock": "Reset"}, {"_id": 0, "Reset": 1})["Reset"]
        if cca > cpa:
            if cca >= cpa * 2:
                ec = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**'
            else:
                ec = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**'
        elif cca == cpa:
            ec = f'**No Change** [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
        else:
            ec = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▼ {pre}{locale.format_string("%d", cpa - cca, grouping=True)} `(▼ {(cpa - cca) / cpa * 100:.2f}%)`**'

        if oca > opa:
            if oca >= opa * 2:
                oc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**'
            else:
                oc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**'
        elif oca == opa:
            oc = f'**No Change** [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
        else:
            oc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▼ {pre}{locale.format_string("%d", opa - oca, grouping=True)} `(▼ {(opa - oca) / opa * 100:.2f}%)`**'

        if sca > spa:
            if sca >= spa * 2:
                sc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", sca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", sca - spa, grouping=True)} `(▲ {(sca - spa) / spa * 100:.2f}%)`**'
            else:
                sc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", sca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", sca - spa, grouping=True)} `(▲ {(sca - spa) / spa * 100:.2f}%)`**'
        elif sca == spa:
            sc = f'**No Change** [{pre}{locale.format_string("%d", sca, grouping=True)} / orange](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
        else:
            sc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", sca, grouping=True)} / orange](https://google.com) ─ **▼ {pre}{locale.format_string("%d", spa - sca, grouping=True)} `(▼ {(spa - sca) / spa * 100:.2f}%)`**'

        if tca > tpa:
            if tca >= tpa * 2:
                tc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", tca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", tca - tpa, grouping=True)} `(▲ {(tca - tpa) / tpa * 100:.2f}%)`**'
            else:
                tc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", tca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", tca - tpa, grouping=True)} `(▲ {(tca - tpa) / tpa * 100:.2f}%)`**'
        elif tca == tpa:
            tc = f'**No Change** [{pre}{locale.format_string("%d", tca, grouping=True)} / orange](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**'
        else:
            tc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", tca, grouping=True)} / orange](https://google.com) ─ **▼ {pre}{locale.format_string("%d", tpa - tca, grouping=True)} `(▼ {(tpa - tca) / tpa * 100:.2f}%)`**'

        if select.values[0] == "cheap":
            embed = discord.Embed(title="Available Stocks", color=color)
            embed.add_field(name="Orange :tangerine:",
                            value=f'{oc}\nA fresh orange orange. You can use it to flex to your friends.', inline=False)
            embed.add_field(name="Coincord :coin:",
                            value=f'{ec}\nA beautiful coin. Pretty useless, but they might be worth a fortune',
                            inline=False)
            embed.add_field(name="Golden Statue of Statue of Golden",
                            value=f'{sc}\nA golden statue that is a statue of gold', inline=False)
            await interaction.response.edit_message(embed=embed)
        elif select.values[0] == "expensive":
            embed = discord.Embed(title="Available Stocks", color=color)
            embed.add_field(name="Golden Statue of Statue of Golden",
                            value=f'{sc}\nA golden statue that is a statue of gold', inline=False)
            embed.add_field(name="Coincord :coin:",
                            value=f'{ec}\nA beautiful coin. Pretty useless, but they might be worth a fortune',
                            inline=False)
            embed.add_field(name="Orange :tangerine:",
                            value=f'{oc}\nA fresh orange orange. You can use it to flex to your friends.', inline=False)
            await interaction.response.edit_message(embed=embed)
@commands.command()
@commands.is_owner()
async def mystocks(ctx):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Mystocks": 1})["Mystocks"]
    colc.update_one({"Mystocks": tc}, {"$set": {"Mystocks": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Mystocks": 1})["Mystocks"]
    cold.update_one({"Mystocks": tcd}, {"$set": {"Mystocks": tcd + 1}})
    cols = serverdb["serverdb"]
    aa = []
    for x in cols.find({}, {"_id": 0, "GUILD ID": 1}): aa.append(x)
    if {"GUILD ID": ctx.author.guild.id} not in aa: cols.insert_one({"GUILD ID": ctx.author.guild.id, "Prefix": None, "Mute Role": None, "Total Commands": 0, "Total Messages": 0})
    theprefix = cols.find_one({"GUILD ID": ctx.author.guild.id}, {"_id": 0, "Prefix": 1})["Prefix"]

    if theprefix is None: theprefix = default_prefix

    cols = stocksdb["stocks"]
    uscol = stocksdb["userstock"]
    aab = []
    for x in uscol.find({}, {"_id": 0, "USER ID": 1}): aab.append(x)
    if {"USER ID": ctx.author.id} not in aab: uscol.insert_one({"USER ID": ctx.author.id, "Coincord":0,"Orange":0,"Golden Statue of Statue of Golden":0,"The Revolutionary":0})
    c = uscol.find_one({"USER ID": ctx.author.id}, {"_id":0, "Coincord":1})["Coincord"]
    o = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Orange": 1})["Orange"]
    s = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Golden Statue of Statue of Golden": 1})["Golden Statue of Statue of Golden"]
    t = uscol.find_one({"USER ID": ctx.author.id}, {"_id": 0, "The Revolutionary": 1})["The Revolutionary"]
    cca = cols.find_one({"Stock":"Coincord"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
    cpa = cols.find_one({"Stock":"Coincord"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
    oca = cols.find_one({"Stock":"Orange"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
    opa = cols.find_one({"Stock":"Orange"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
    sca = cols.find_one({"Stock":"Golden Statue of Statue of Golden"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
    spa = cols.find_one({"Stock":"Golden Statue of Statue of Golden"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
    tca = cols.find_one({"Stock":"The Revolutionary"}, {"_id": 0, "Current Amount": 1})["Current Amount"]
    tpa = cols.find_one({"Stock":"The Revolutionary"}, {"_id": 0, "Previous Amount": 1})["Previous Amount"]
    reset = cols.find_one({"Stock":"Reset"}, {"_id": 0, "Reset": 1})["Reset"]

    if int(c) == 0 and int(o) == 0 and int(t) == 0 and int(s) == 0:
        embed = discord.Embed(description=f"You have no stocks currently\nGo buy some: **`{theprefix}stocks`**", color=color)
    else:
        embed=discord.Embed(description=f"Stocks reset on **{reset}**", color=color)
        embed.set_author(name=f"{ctx.author.name}'s stocks", icon_url=ctx.author.avatar)
        embed.set_footer(text="stonks")

        if int(c) > 0:
            if cca > cpa:
                if cca >= cpa * 2:
                    ec = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**\n\nYou have **{c} coins** (`{pre}{locale.format_string("%d", c * cca, grouping=True)}`)'
                    footer = "Your professional investor advises you to REALLY sell"
                else:
                    ec = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▲ {pre}{locale.format_string("%d", cca - cpa, grouping=True)} `(▲ {(cca - cpa) / cpa * 100:.2f}%)`**\n\nYou have **{c} coins** (`{pre}{locale.format_string("%d", c * cca, grouping=True)}`)'
                    footer = "Your professional investor advises you to sell"
            elif cca == cpa:
                ec = f'**No Change** [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**\n\nYou have **{c} coins** (`{pre}{locale.format_string("%d", c * cca, grouping=True)}`)'
                footer = "Your professional investor advises you to not sell"
            else:
                ec = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", cca, grouping=True)} / coin](https://google.com) ─ **▼ {pre}{locale.format_string("%d", cpa - cca, grouping=True)} `(▼ {(cpa - cca) / cpa * 100:.2f}%)`**\n\nYou have **{c} coins** (`{pre}{locale.format_string("%d", c * cca, grouping=True)}`)'
                footer = "Your professional investor advises you to not sell"
            embed.add_field(name="Coincord :coin:", value=f"{ec}\n```yaml\n{footer}```", inline=False)
        if int(o) > 0:
            if oca > opa:
                if oca >= opa * 2:
                    oc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**\n\nYou have **{o} oranges** (`{pre}{locale.format_string("%d", o * oca, grouping=True)}`)'
                    footer2 = "Your professional investor advises you to REALLY sell"
                else:
                    oc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▲ {pre}{locale.format_string("%d", oca - opa, grouping=True)} `(▲ {(oca - opa) / opa * 100:.2f}%)`**\n\nYou have **{o} oranges** (`{pre}{locale.format_string("%d", o * oca, grouping=True)}`)'
                    footer2 = "Your professional investor advises you to sell"
            elif oca == opa:
                oc = f'**No Change** [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**\n\nYou have **{o} oranges** (`{pre}{locale.format_string("%d", o * oca, grouping=True)}`)'
                footer2 = "Your professional investor advises you to not sell"
            else:
                oc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", oca, grouping=True)} / orange](https://google.com) ─ **▼ {pre}{locale.format_string("%d", opa - oca, grouping=True)} `(▼ {(opa - oca) / opa * 100:.2f}%)`**\n\nYou have **{o} oranges** (`{pre}{locale.format_string("%d", o * oca, grouping=True)}`)'
                footer2 = "Your professional investor advises you to not sell"
            embed.add_field(name='Orange :tangerine:', value=f"{oc}\n```yaml\n{footer2}```", inline=False)
        if int(s) > 0:
            if sca > spa:
                if sca >= spa * 2:
                    sc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", sca, grouping=True)} / statue](https://google.com) ─ **▲ {pre}{locale.format_string("%d", sca - spa, grouping=True)} `(▲ {(sca - spa) / spa * 100:.2f}%)`**\n\nYou have **{s} statues** (`{pre}{locale.format_string("%d", s * sca, grouping=True)}`)'
                    footer3 = "Your professional investor advises you to REALLY sell"
                else:
                    sc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", sca, grouping=True)} / statue](https://google.com) ─ **▲ {pre}{locale.format_string("%d", sca - spa, grouping=True)} `(▲ {(sca - spa) / spa * 100:.2f}%)`**\n\nYou have **{s} statues** (`{pre}{locale.format_string("%d", s * sca, grouping=True)}`)'
                    footer3 = "Your professional investor advises you to sell"
            elif sca == spa:
                sc = f'**No Change** [{pre}{locale.format_string("%d", sca, grouping=True)} / statue](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**\n\nYou have **{s} statues** (`{pre}{locale.format_string("%d", s * sca, grouping=True)}`)'
                footer3 = "Your professional investor advises you not to sell"
            else:
                sc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", sca, grouping=True)} / statue](https://google.com) ─ **▼ {pre}{locale.format_string("%d", spa - sca, grouping=True)} `(▼ {(spa - sca) / spa * 100:.2f}%)`**\n\nYou have **{s} statues** (`{pre}{locale.format_string("%d", s * sca, grouping=True)}`)'
                footer3 = "Your professional investor advises you not to sell"
            embed.add_field(name="Golden Statue of Statue of Golden", value=f"{sc}\n```yaml\n{footer3}```", inline=False)
        if int(t) > 0:
            if tca > tpa:
                if tca >= tpa * 2:
                    tc = f'<:stonks:870758818093600768> [{pre}{locale.format_string("%d", tca, grouping=True)} / share](https://google.com) ─ **▲ {pre}{locale.format_string("%d", tca - tpa, grouping=True)} `(▲ {(tca - tpa) / tpa * 100:.2f}%)`**\n\nYou have **{t} shares** (`{pre}{locale.format_string("%d", t * tca, grouping=True)}`)'
                    footer4 = "Your professional investor advises you to REALLY sell"
                else:
                    tc = f':chart_with_upwards_trend: [{pre}{locale.format_string("%d", tca, grouping=True)} / share](https://google.com) ─ **▲ {pre}{locale.format_string("%d", tca - tpa, grouping=True)} `(▲ {(tca - tpa) / tpa * 100:.2f}%)`**\n\nYou have **{t} shares** (`{pre}{locale.format_string("%d", t * tca, grouping=True)}`)'
                    footer4 = "Your professional investor advises you to sell"
            elif tca == tpa:
                tc = f'**No Change** [{pre}{locale.format_string("%d", tca, grouping=True)} / share](https://google.com) ─ **⬍ {pre}0 `(⬍ 0.00%)`**\n\nYou have **{t} shares** (`{pre}{locale.format_string("%d", t * tca, grouping=True)}`)'
                footer4 = "Your professional investor advises you not to sell"
            else:
                tc = f':chart_with_downwards_trend: [{pre}{locale.format_string("%d", tca, grouping=True)} / share](https://google.com) ─ **▼ {pre}{locale.format_string("%d", tpa - tca, grouping=True)} `(▼ {(tpa - tca) / tpa * 100:.2f}%)`**\n\nYou have **{t} shares** (`{pre}{locale.format_string("%d", t * tca, grouping=True)}`)'
                footer4 = "Your professional investor advises you not to sell"
            embed.add_field(name="The Revolutionary <:therevolutionary:865728876546097174>", value=f"{tc}\n```yaml\n{footer4}```", inline=False)
    await ctx.send(embed=embed)

"""FISHING"""
@commands.command()
@commands.is_owner()
@commands.cooldown(1, 4, commands.BucketType.user)
async def fish(ctx):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Fish": 1})["Fish"]
    colc.update_one({"Fish": tc}, {"$set": {"Fish": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Fish": 1})["Fish"]
    cold.update_one({"Fish": tcd}, {"$set": {"Fish": tcd + 1}})

    coli = indb["inventory"]
    a = []
    for x in coli.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: coli.insert_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown": 0, ":star: Star": 0,"<:legendarybox:880229601043963905> Legendary Box": 0, "<:mythicalbox:881252527235018753> Mythical Box": 0,":medal: Medal": 0, ":fog: Air": 0, ":tickets: Ticket": 0, ":fishing_pole_and_fish: Fishing Rod":0,"<:biggerfr:898645851461783594> Platinum Fishing Rod":0,":worm: Worm":0})
    tr = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:therevolutionary:865728876546097174> Crown": 1})["<:therevolutionary:865728876546097174> Crown"]
    st = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":star: Star": 1})[":star: Star"]
    fog = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":fog: Air":1})[":fog: Air"]
    medal = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":medal: Medal":1})[":medal: Medal"]
    ticket = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":tickets: Ticket": 1})[":tickets: Ticket"]
    lbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:legendarybox:880229601043963905> Legendary Box": 1})["<:legendarybox:880229601043963905> Legendary Box"]
    mbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:mythicalbox:881252527235018753> Mythical Box": 1})["<:mythicalbox:881252527235018753> Mythical Box"]
    frod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":fishing_pole_and_fish: Fishing Rod": 1})[":fishing_pole_and_fish: Fishing Rod"]
    pfrod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:biggerfr:898645851461783594> Platinum Fishing Rod": 1})["<:biggerfr:898645851461783594> Platinum Fishing Rod"]
    worm = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":worm: Worm": 1})[":worm: Worm"]

    colt = leaugesdb["leagues"]
    b = []
    for x in colt.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colt.insert_one({"USER ID": ctx.author.id, "USER":str(ctx.author),"League": "🔰 Challenger 🔰", "Trophies": 0})
    trophye = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Trophies": 1})["Trophies"]
    league = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "League": 1})["League"]

    rare = random.randint(1, 10000) if worm == 0 else random.randint(500, 10000)
    trophy = random.randint(10, 100)
    rt = random.randint(1, 5)
    afish = 1 if pfrod == 0 else random.randint(2, 5)

    coli.update_one({"USER ID": ctx.author.id, ":worm: Worm": worm}, {"$set": {":worm: Worm": worm - 1}})

    if frod == 0 and pfrod == 0:
        embed = discord.Embed(description=f"You have no **Fishing Rods :fishing_pole_and_fish:**. Go buy one, `r!shop`",color=color)
        embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
        await ctx.send(embed=embed)
    else:
        msg = await ctx.reply("Fishing...")
        time.sleep(1)
        bonus = None
        if rare <= 1000:
            embed = discord.Embed(description=f"You caught **nothing**. Better luck next time.", color=color)
        elif rare > 1000 and rare <= 2000:
            embed = discord.Embed(description="Your **Fishing Rod :fishing_pole_and_fish:** broke from bad manufacturing.", color=color)
        else:
            if rare > 2000 and rare <= 6500:
                afish = random.randint(1, 5) if pfrod == 0 else random.randint(6, 10)
                type = random.choice(["Fish", "Shrimp"])
                emoji = f":{type.lower()}:"
            elif rare > 6500 and rare <= 9000:
                type = random.choice(["Rare Fish", "Crab", "Squid", "Lobster"])
                if rt == 1:
                    if type =="Rare Fish":
                        emoji = ":tropical_fish:"
                    else:
                        emoji = f":{type.lower()}:"
                    colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye}, {"$set": {"Trophies": trophye+trophy}})
                    if trophy > 1:
                        bonus = f"**YOU LUCKY DUCKY!** You also found **`{trophy}` Trophies** <:leaguetrophy:891844638380556319>!"
                    else:
                        bonus = f"**YOU LUCKY DUCKY!** You also found **a Trophy** <:leaguetrophy:891844638380556319>!"
                else:
                    if type =="Rare Fish":
                        emoji = ":tropical_fish:"
                    else:
                        emoji = f":{type.lower()}:"
            elif rare > 9000 and rare <= 9850:
                type = random.choice(["Octopus", "Dolphin", "Blowfish"])
                emoji = f":{type.lower()}:"
            elif rare > 9850 and rare <= 9950:
                type = random.choice(["Whale", "Shark", "Crocodile"])
                if type =="Whale":
                    emoji = ":whale2:"
                else:
                    emoji = f":{type.lower()}:"
            else:
                type = random.choice(["FRICKING SEA DRAGON! WOW", "STAR! LUCKY!", "MYTHICAL FISH!?!", "CROWN!"])
                if type =="FRICKING SEA DRAGON! WOW":
                    emoji = ":dragon:"
                elif type == "MYTHICAL FISH!?!":
                    emoji = "<:MythicalFish:892182628717953024>"
                elif type == "CROWN!":
                    emoji = "<:therevolutionary:865728876546097174>"
                else:
                    emoji = ":star:"
            col = fishdb["fish"]
            a = []
            for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
            if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Fish :fish:": 0,"Shrimp :shrimp:": 0,"Rare Fish :tropical_fish:": 0,"Crab :crab:": 0,"Squid :squid:": 0,"Octopus :octopus:": 0,"Dolphin :dolphin:": 0,"Blowfish :blowfish:": 0,"Lobster :lobster:": 0,"Whale :whale2:": 0,"Shark :shark:": 0,"Crocodile :crocodile:": 0,"Sea Dragon :dragon:": 0,"Mythical Fish <:MythicalFish:892182628717953024>": 0,"Prized Fish": None})
            if rare <= 9950:
                tf = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, f"{type} {emoji}": 1})[f"{type} {emoji}"]
                col.update_one({"USER ID": ctx.author.id, f"{type} {emoji}": tf}, {"$set": {f"{type} {emoji}": tf + afish}})
            else:
                if type =="FRICKING SEA DRAGON! WOW":
                    tf = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Sea Dragon :dragon:": 1})["Sea Dragon :dragon:"]
                    col.update_one({"USER ID": ctx.author.id,"Sea Dragon :dragon:": tf},{"$set": {"Sea Dragon :dragon:": tf + afish}})
                elif type == "MYTHICAL FISH!?!":
                    tf = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Mythical Fish <:MythicalFish:892182628717953024>": 1})["Mythical Fish <:MythicalFish:892182628717953024>"]
                    col.update_one({"USER ID": ctx.author.id, "Mythical Fish <:MythicalFish:892182628717953024>": tf},{"$set": {"Mythical Fish <:MythicalFish:892182628717953024>": tf + afish}})
                elif type == "CROWN!":
                    coli.update_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown":tr},{"$set": {"<:therevolutionary:865728876546097174> Crown": tr + 1}})
                else:
                    coli.update_one({"USER ID": ctx.author.id, ":star: Star": st},{"$set": {":star: Star": st + 1}})

            embed=discord.Embed(description=f"You caught **{afish} {type}** {emoji}!", color=color)
            if type == "FRICKING SEA DRAGON! WOW":
                embed.set_footer(text="pretend its one ok")

            if bonus is not None:
                await ctx.send(bonus)

                if trophye+trophy >= 250 and trophye+trophy < 500 and "Novice" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🛡️ Novice Tier 🛡️"}})
                elif trophye+trophy >= 500 and trophye+trophy < 1000 and "Gold" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🔱 Gold Tier 🔱"}})
                elif trophye+trophy >= 1000 and trophye+trophy < 2000 and "Purple Dragon" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "⚜️Purple Dragon Tier ⚜️"}})
                elif trophye+trophy >= 2000 and trophye+trophy < 3000 and "Diamond" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "💎 Diamond Tier 💎"}})
                elif trophye+trophy >= 3000 and trophye+trophy < 4500 and "Master" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "⚔️ Master Tier ⚔️"}})
                elif trophye+trophy >= 4500 and trophye+trophy < 5000 and "Legendary" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🃏 Legendary Tier 🃏"}})
                elif trophye+trophy >= 5000 and "The Best of the Best" not in league:
                    await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
                    colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🏴‍☠️ The Best of the Best 🏴‍☠️"}})

        await msg.edit(content=None, embed=embed)
@fish.error
async def fish_e(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if int(s) == 1:
            suffix = "second"
        else:
            suffix = "seconds"
        if int(h) == 0 and int(m) == 0:
            embed = discord.Embed(description=f"Your on cooldown. **{int(s)+1} {suffix}** left",color=color)
            embed.set_author(icon_url='https://cdn.discordapp.com/emojis/842221924997791755.png?size=32', name="Slow it down")
            await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def fsell(ctx, fishe, amount=None):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Fishsell": 1})["Fishsell"]
    colc.update_one({"Fishsell": tc}, {"$set": {"Fishsell": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Fishsell": 1})["Fishsell"]
    cold.update_one({"Fishsell": tcd}, {"$set": {"Fishsell": tcd + 1}})

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

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

    col2 = fishdb["fish"]
    b = []
    for x in col2.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in a: col2.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Fish :fish:": 0, "Shrimp :shrimp:": 0,"Rare Fish :tropical_fish:": 0, "Crab :crab:": 0, "Squid :squid:": 0, "Octopus :octopus:": 0,"Dolphin :dolphin:": 0, "Blowfish :blowfish:": 0, "Lobster :lobster:": 0, "Whale :whale2:": 0,"Shark :shark:": 0, "Crocodile :crocodile:": 0, "Sea Dragon :dragon:": 0,"Mythical Fish <:MythicalFish:892182628717953024>": 0, "Prized Fish": None})

    if fishe.lower() == "whale":
        name = "Whale"
        emoji = ":whale2:"
    elif fishe.lower() == "rarefish" or fishe.lower() == "rare":
        name = "Rare Fish"
        emoji = ":tropical_fish:"
    elif fishe.lower() == "seadragon" or fishe.lower() == "dragon":
        name = "Sea Dragon"
        emoji = ":dragon:"
    elif fishe.lower() == "mythicalfish" or fishe.lower() == "mythical":
        name = "Mythical Fish"
        emoji = "<:MythicalFish:892182628717953024>"
    else:
        name = fishe.title()
        emoji = f":{fishe.lower()}:"

    tf = col2.find_one({"USER ID": ctx.author.id}, {"_id": 0, f"{name} {emoji}": 1})[f"{name} {emoji}"]

    if amount is None:
        if tf == 0:
            embed = discord.Embed(
                description=f"You haven't caught a **{name} {emoji}**",
                color=discord.Color.red())
            embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
        else:
            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + int(chart.get(f'{name} {emoji}'))}})
            col2.update_one({"USER ID": ctx.author.id, f"{name} {emoji}": tf},{"$set": {f"{name} {emoji}": tf - 1}})
            embed = discord.Embed(
                description=f"You sold a **{name} {emoji}** for `{pre}{chart.get(f'{name} {emoji}')}`",
                color=discord.Color.green())
            embed.set_author(name="Successful Transaction", icon_url=micon)
    else:
        if amount.isnumeric():

            if tf < int(amount):
                embed = discord.Embed(
                    description=f"You don't have `{locale.format_string('%d', int(amount), grouping=True)}` **{name} {emoji}**",
                    color=discord.Color.red())
                embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
            else:
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + int(chart.get(f'{name} {emoji}'))*int(amount)}})
                col2.update_one({"USER ID": ctx.author.id, f"{name} {emoji}": tf},{"$set": {f"{name} {emoji}": tf - int(amount)}})
                embed = discord.Embed(
                    description=f"You sold `{locale.format_string('%d', int(amount), grouping=True)}` **{name} {emoji}** for `{pre}{locale.format_string('%d', chart.get(f'{name} {emoji}')*int(amount), grouping=True)}`",
                    color=discord.Color.green())
                embed.set_author(name="Successful Transaction", icon_url=micon)
        else:
            if amount.lower() == "max" or amount.lower() == "all":
                if tf == 0:
                    embed = discord.Embed(
                        description=f"You haven't caught a **{name} {emoji}**",
                        color=discord.Color.red())
                    embed.set_author(name='Error',
                                     icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
                else:
                    col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet + int(chart.get(f'{name} {emoji}')) * tf}})
                    col2.update_one({"USER ID": ctx.author.id, f"{name} {emoji}": tf},{"$set": {f"{name} {emoji}": tf - tf}})
                    embed = discord.Embed(
                        description=f"You sold `{locale.format_string('%d', tf, grouping=True)}` **{name} {emoji}** for `{pre}{locale.format_string('%d', chart.get(f'{name} {emoji}') * tf, grouping=True)}`",
                        color=discord.Color.green())
                    embed.set_author(name="Successful Transaction", icon_url=micon)
            else:
                embed=discord.Embed(description="Please provide a valid input", color=discord.Color.red())
                embed.set_author(name='Error',icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
    await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def setprized(ctx, fishe=None):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Setprized": 1})["Setprized"]
    colc.update_one({"Setprized": tc}, {"$set": {"Setprized": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Setprized": 1})["Setprized"]
    cold.update_one({"Setprized": tcd}, {"$set": {"Setprized": tcd + 1}})

    with open('serverdb.json', "r") as f:prefix = json.load(f)

    if str(ctx.author.guild.id) not in prefix:sp = default_prefix
    else:
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None:sp = default_prefix
        else:sp = prefix[str(ctx.author.guild.id)]["Prefix"]

    col = fishdb["fish"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Fish :fish:": 0, "Shrimp :shrimp:": 0,"Rare Fish :tropical_fish:": 0, "Crab :crab:": 0, "Squid :squid:": 0, "Octopus :octopus:": 0,"Dolphin :dolphin:": 0, "Blowfish :blowfish:": 0, "Lobster :lobster:": 0, "Whale :whale2:": 0,"Shark :shark:": 0, "Crocodile :crocodile:": 0, "Sea Dragon :dragon:": 0,"Mythical Fish <:MythicalFish:892182628717953024>": 0, "Prized Fish": None})

    tf = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Prized Fish": 1})["Prized Fish"]

    if fishe is None:
        if tf is None:
            embed=discord.Embed(description=f"You do not have a current prized fish. Set one by doing `{sp}setprized [fish]`", color=color)
        else:
            embed=discord.Embed(description=f"Your current set prized fish is: **{tf}**", color=color)
    else:
        if fishe.lower() == "whale":
            name = "Whale"
            emoji = ":whale2:"
        elif fishe.lower() == "rarefish" or fishe.lower() == "rare":
            name = "Rare Fish"
            emoji = ":tropical_fish:"
        elif fishe.lower() == "seadragon" or fishe.lower() == "dragon":
            name = "Sea Dragon"
            emoji = ":dragon:"
        elif fishe.lower() == "mythicalfish" or fishe.lower() == "mythical":
            name = "Mythical Fish"
            emoji = "<:MythicalFish:892182628717953024>"
        else:
            name = fishe.title()
            emoji = f":{fishe.lower()}:"

        tf2 = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, f"{name} {emoji}": 1})[f"{name} {emoji}"]

        if tf2 == 0:
            embed=discord.Embed(description=f"You never caught a **{name} {emoji}**.", color=discord.Color.red())
            embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
        else:
            col.update_one({"USER ID": ctx.author.id, "Prized Fish": tf},{"$set": {"Prized Fish": f"{name} {emoji}"}})

            embed = discord.Embed(
                description=f"Your new prized fish: **{name} {emoji}**",
                color=discord.Color.green())
            embed.set_author(name="Successful Action", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

"""FARMING"""
@commands.command()
@commands.is_owner()
async def farm(ctx):
    coli = indb["inventory"]
    a = []
    for x in coli.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: coli.insert_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown": 0, ":star: Star": 0,"<:legendarybox:880229601043963905> Legendary Box": 0, "<:mythicalbox:881252527235018753> Mythical Box": 0,":medal: Medal": 0, ":fog: Air": 0, ":tickets: Ticket": 0, ":fishing_pole_and_fish: Fishing Rod":0,"<:biggerfr:898645851461783594> Platinum Fishing Rod":0,":worm: Worm":0})
    tr = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:therevolutionary:865728876546097174> Crown": 1})["<:therevolutionary:865728876546097174> Crown"]
    st = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":star: Star": 1})[":star: Star"]
    fog = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":fog: Air":1})[":fog: Air"]
    medal = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":medal: Medal":1})[":medal: Medal"]
    ticket = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":tickets: Ticket": 1})[":tickets: Ticket"]
    lbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:legendarybox:880229601043963905> Legendary Box": 1})["<:legendarybox:880229601043963905> Legendary Box"]
    mbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:mythicalbox:881252527235018753> Mythical Box": 1})["<:mythicalbox:881252527235018753> Mythical Box"]
    frod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":fishing_pole_and_fish: Fishing Rod": 1})[":fishing_pole_and_fish: Fishing Rod"]
    pfrod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:biggerfr:898645851461783594> Platinum Fishing Rod": 1})["<:biggerfr:898645851461783594> Platinum Fishing Rod"]
    worm = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":worm: Worm": 1})[":worm: Worm"]
    bee = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":bee: Bee": 1})[":bee: Bee"]
    honeypot = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":honey_pot: Honey Pot": 1})[":honey_pot: Honey Pot"]
    seedling = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":seedling: Seedling": 1})[":seedling: Seedling"]
    apple = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":apple: Apple": 1})[":apple: Apple"]

    colff = farmdb["farm"]
    b = []
    for x in colff.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colff.insert_one({"USER ID": ctx.author.id, "Seed 1": None, "Planted":False,"Last Collected":None})
    seed1 = colff.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Seed 1": 1})["Seed 1"]
    plantedt = colff.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Planted": 1})["Planted"]
    lastcolf = colff.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Last Collected": 1})["Last Collected"]

    colfb = farmdb["bee"]
    d = []
    for x in colfb.find({}, {"_id": 0, "USER ID": 1}): d.append(x)
    if {"USER ID": ctx.author.id} not in d: colfb.insert_one({"USER ID": ctx.author.id, "Last Collected":None})
    lastcol = colfb.find_one({"USER ID": ctx.author.id}, {"_id":0, "Last Collected":1})["Last Collected"]

    planted = []

    if plantedt is True:
        planted.append("1")

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

    if seedling == 0 and bee == 0:
        embed = discord.Embed(description=f"You have no bees or seedlings currently\nGo buy some: **`r!shop`**", color=color)
    else:
        embed = discord.Embed(color=color)
        embed.set_author(name=f"{ctx.author.name}'s Farm", icon_url=micon)
        if seedling > 0:
            embed.add_field(name="Plants", value=f"Your seedlings: **{seedling} :seedling:**\nPlanted: **{len(planted)}/1**\nLast Collected: {discord.utils.format_dt(lastcolf, style='R')}")
        if bee > 0:
            embed.add_field(name="Honey",value=f"Your bees: **{bee} :bee:**\nLast Collected: wip")
    await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def grow(ctx, arg):
    coli = indb["inventory"]
    a = []
    for x in coli.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: coli.insert_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown": 0, ":star: Star": 0,"<:legendarybox:880229601043963905> Legendary Box": 0, "<:mythicalbox:881252527235018753> Mythical Box": 0,":medal: Medal": 0, ":fog: Air": 0, ":tickets: Ticket": 0, ":fishing_pole_and_fish: Fishing Rod":0,"<:biggerfr:898645851461783594> Platinum Fishing Rod":0,":worm: Worm":0})
    tr = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:therevolutionary:865728876546097174> Crown": 1})["<:therevolutionary:865728876546097174> Crown"]
    st = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":star: Star": 1})[":star: Star"]
    fog = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":fog: Air":1})[":fog: Air"]
    medal = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":medal: Medal":1})[":medal: Medal"]
    ticket = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":tickets: Ticket": 1})[":tickets: Ticket"]
    lbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:legendarybox:880229601043963905> Legendary Box": 1})["<:legendarybox:880229601043963905> Legendary Box"]
    mbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:mythicalbox:881252527235018753> Mythical Box": 1})["<:mythicalbox:881252527235018753> Mythical Box"]
    frod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":fishing_pole_and_fish: Fishing Rod": 1})[":fishing_pole_and_fish: Fishing Rod"]
    pfrod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:biggerfr:898645851461783594> Platinum Fishing Rod": 1})["<:biggerfr:898645851461783594> Platinum Fishing Rod"]
    worm = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":worm: Worm": 1})[":worm: Worm"]
    bee = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":bee: Bee": 1})[":bee: Bee"]
    honeypot = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":honey_pot: Honey Pot": 1})[":honey_pot: Honey Pot"]
    seedling = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":seedling: Seedling": 1})[":seedling: Seedling"]
    apple = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":apple: Apple": 1})[":apple: Apple"]

    colff = farmdb["farm"]
    b = []
    for x in colff.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colff.insert_one({"USER ID": ctx.author.id, "Seed 1": None, "Planted": False, "Last Collected": None})
    seed1 = colff.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Seed 1": 1})["Seed 1"]
    plantedt = colff.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Planted": 1})["Planted"]
    lastcolf = colff.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Last Collected": 1})["Last Collected"]

    colfb = farmdb["bee"]
    d = []
    for x in colfb.find({}, {"_id": 0, "USER ID": 1}): d.append(x)
    if {"USER ID": ctx.author.id} not in d: colfb.insert_one({"USER ID": ctx.author.id, "Last Collected": None})
    lastcol = colfb.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Last Collected": 1})["Last Collected"]
    if arg == "seed":
        if seedling is None:
            embed=discord.Embed(description="You have no seeds")
        else:
            if plantedt is True:
                embed=discord.Embed(description="You already have planted a seed.")
            else:
                embed=discord.Embed(description="You planted a **Seed** :seedling:!")
                coli.update_one({"USER ID":ctx.author.id, ":seedling: Seedling":seedling}, {"$set":{":seedling: Seedling":seedling-1}})
                colff.update_one({"USER ID": ctx.author.id, "Planted": plantedt},{"$set": {"Planted": True}})
                colff.update_one({"USER ID": ctx.author.id, "Seed 1": seed1}, {"$set": {"Seed 1": "Apple Tree"}})
                colff.update_one({"USER ID": ctx.author.id, "Last Collected": lastcolf},{"$set": {"Last Collected": datetime.utcnow()}})
        await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def collect(ctx):
    coli = indb["inventory"]
    a = []
    for x in coli.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: coli.insert_one({"USER ID": ctx.author.id, "<:therevolutionary:865728876546097174> Crown": 0, ":star: Star": 0,"<:legendarybox:880229601043963905> Legendary Box": 0, "<:mythicalbox:881252527235018753> Mythical Box": 0,":medal: Medal": 0, ":fog: Air": 0, ":tickets: Ticket": 0, ":fishing_pole_and_fish: Fishing Rod":0,"<:biggerfr:898645851461783594> Platinum Fishing Rod":0,":worm: Worm":0})
    tr = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:therevolutionary:865728876546097174> Crown": 1})["<:therevolutionary:865728876546097174> Crown"]
    st = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":star: Star": 1})[":star: Star"]
    fog = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":fog: Air":1})[":fog: Air"]
    medal = coli.find_one({"USER ID": ctx.author.id}, {"_id":0, ":medal: Medal":1})[":medal: Medal"]
    ticket = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":tickets: Ticket": 1})[":tickets: Ticket"]
    lbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:legendarybox:880229601043963905> Legendary Box": 1})["<:legendarybox:880229601043963905> Legendary Box"]
    mbox = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:mythicalbox:881252527235018753> Mythical Box": 1})["<:mythicalbox:881252527235018753> Mythical Box"]
    frod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":fishing_pole_and_fish: Fishing Rod": 1})[":fishing_pole_and_fish: Fishing Rod"]
    pfrod = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, "<:biggerfr:898645851461783594> Platinum Fishing Rod": 1})["<:biggerfr:898645851461783594> Platinum Fishing Rod"]
    worm = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":worm: Worm": 1})[":worm: Worm"]
    bee = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":bee: Bee": 1})[":bee: Bee"]
    honeypot = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":honey_pot: Honey Pot": 1})[":honey_pot: Honey Pot"]
    seedling = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":seedling: Seedling": 1})[":seedling: Seedling"]
    apple = coli.find_one({"USER ID": ctx.author.id}, {"_id": 0, ":apple: Apple": 1})[":apple: Apple"]

    colff = farmdb["farm"]
    b = []
    for x in colff.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colff.insert_one({"USER ID": ctx.author.id, "Seed 1": None, "Planted": False, "Last Collected": None})
    seed1 = colff.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Seed 1": 1})["Seed 1"]
    plantedt = colff.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Planted": 1})["Planted"]
    lastcolf = colff.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Last Collected": 1})["Last Collected"]

    colfb = farmdb["bee"]
    d = []
    for x in colfb.find({}, {"_id": 0, "USER ID": 1}): d.append(x)
    if {"USER ID": ctx.author.id} not in d: colfb.insert_one({"USER ID": ctx.author.id, "Last Collected": None})
    lastcol = colfb.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Last Collected": 1})["Last Collected"]

    past = lastcolf

    duration = past - datetime.utcnow()
    duration2 = datetime.utcnow() - past
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s, 86400)  # Get days (without [0]!)
    hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
    minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
    seconds = divmod(minutes[1], 1)
    if int(hours[0]) >= 1:
        embed=discord.Embed(description="you collected seed")
    else:
        embed=discord.Embed(description="wait")
    await ctx.send(embed=embed)

"""GAMBLING"""
@commands.command()
@commands.is_owner()
async def flipcoin(ctx, choice=None):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Flipcoin": 1})["Flipcoin"]
    colc.update_one({"Flipcoin": tc}, {"$set": {"Flipcoin": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Deposit": 1})["Deposit"]
    cold.update_one({"Deposit": tcd}, {"$set": {"Deposit": tcd + 1}})
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
            coins = random.randint(10000, 100000)
            if choice.lower() == true:
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet+coins}})
                await message.edit(f"**You won {pre}{coins}!** The coin landed on **`{true}`**")
            else: await message.edit(f"You lost. The coin landed on **`{true}`**")
        else: await ctx.send("Your choices are: **`Heads`** or **`Tails`**")
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.command()
@commands.is_owner()
async def gamble(ctx, amount):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Gamble": 1})["Gamble"]
    colc.update_one({"Gamble": tc}, {"$set": {"Gamble": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Gamble": 1})["Gamble"]
    cold.update_one({"Gamble": tcd}, {"$set": {"Gamble": tcd + 1}})
    col = db["currency"]

    colt = leaugesdb["leagues"]
    b = []
    for x in colt.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colt.insert_one({"USER ID": ctx.author.id, "USER":str(ctx.author),"League": "🔰 Challenger 🔰", "Trophies": 0})
    trophye = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Trophies": 1})["Trophies"]
    league = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "League": 1})["League"]

    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    gbot = random.randrange(1, 12)
    user = random.randrange(1, 12)

    multiplier = round(random.uniform(0.5, 2), 4)

    bonus = None
    trophy = random.randint(10, 100)
    rt = random.randint(1, 5)

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

    if amount == "all" or amount == "max":
        total_amount = 500000 if wallet > 500000 else wallet

        if wallet == 0:
            embed = discord.Embed(description=f"You don't have enough. You have **{pre}0**", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
        else:
            if gbot > user:
                embed = discord.Embed(description=f"You lost **{pre}{locale.format_string('%d', total_amount, grouping=True)}** coins.\nYou now have **{pre}{locale.format_string('%d', wallet - total_amount, grouping=True)}** coins.",color=discord.Color.red())
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - total_amount}})
            elif gbot == user:
                embed = discord.Embed(description=f"You tied!! Your wallet hasn't changed!\nYou still have **{pre}{locale.format_string('%d', wallet, grouping=True)}** coins.",color=color)
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
            else:
<<<<<<< HEAD
                embed = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', int(total_amount*multiplier), grouping=True)}** coins.\n**Multiplier:** `{round(multiplier,2)*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet + int(total_amount*multiplier), grouping=True)}** coins.",color=discord.Color.green())
=======
                embed = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', int(total_amount*multiplier), grouping=True)}** coins.\n**Multiplier:** `{int(multiplier)*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet + int(total_amount*multiplier), grouping=True)}** coins.",color=discord.Color.green())
>>>>>>> 3cf15a2960ea0efc240f02247cd206762185c240
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet + int(total_amount*multiplier)}})
    else:
        if int(amount) > 500000:
            embed = discord.Embed(description=f"You can only gamble under **`{pre}500,000`**", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
        elif int(amount) <= 0:
            embed = discord.Embed(description=f"You don't have enough. You have **`{pre}{wallet}`**", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
        else:
            if gbot > user:
                embed = discord.Embed(description=f"You lost **{pre}{locale.format_string('%d', int(amount), grouping=True)}** coins.\nYou now have **{pre}{locale.format_string('%d', wallet - int(amount), grouping=True)}** coins.",color=discord.Color.red())
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")

                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - int(amount)}})
            elif gbot == user:
                embed = discord.Embed(description=f"You tied!! Your wallet hasn't changed!\nYou still have **{pre}{locale.format_string('%d', wallet, grouping=True)}** coins.",color=discord.Color.yellow())
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
            else:
<<<<<<< HEAD
                embed = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', int(int(amount)*multiplier), grouping=True)}** coins.\n**Multiplier:** `{round(multiplier,2)*100}%`\nYou now have **{pre}{locale.format_string('%d', int(int(amount)*multiplier + wallet), grouping=True)}** coins.",color=discord.Color.green())
=======
                embed = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', int(int(amount)*multiplier), grouping=True)}** coins.\n**Multiplier:** `{int(multiplier)*100}%`\nYou now have **{pre}{locale.format_string('%d', int(int(amount)*multiplier + wallet), grouping=True)}** coins.",color=discord.Color.green())
>>>>>>> 3cf15a2960ea0efc240f02247cd206762185c240
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")

                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + int(int(amount)*multiplier)}})

    if rt == 1:
        colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye}, {"$set": {"Trophies": trophye + trophy}})
        bonus = f"**YOU LUCKY DUCKY!** You also found **`{trophy}` Trophies** <:leaguetrophy:891844638380556319>!"

    if bonus is not None:
        await ctx.send(bonus)

        if trophye + trophy >= 250 and trophye + trophy < 500 and "Novice" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🛡️ Novice Tier 🛡️"}})
        elif trophye + trophy >= 500 and trophye + trophy < 1000 and "Gold" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🔱 Gold Tier 🔱"}})
        elif trophye + trophy >= 1000 and trophye + trophy < 2000 and "Purple Dragon" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "⚜️Purple Dragon Tier ⚜️"}})
        elif trophye + trophy >= 2000 and trophye + trophy < 3000 and "Diamond" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "💎 Diamond Tier 💎"}})
        elif trophye + trophy >= 3000 and trophye + trophy < 4500 and "Master" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "⚔️ Master Tier ⚔️"}})
        elif trophye + trophy >= 4500 and trophye + trophy < 5000 and "Legendary" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🃏 Legendary Tier 🃏"}})
        elif trophye + trophy >= 5000 and "The Best of the Best" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🏴‍☠️ The Best of the Best 🏴‍☠️"}})
    await ctx.send(embed=embed)
@gamble.error
async def gamble_e(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        embed = discord.Embed(description=f"Your on cooldown. **{int(s)} seconds** left\nCheck out the official server, **[The Revolutionary Support](https://discord.gg/cwFU3zRB)**",color=color)
        embed.set_author(icon_url='https://cdn.discordapp.com/emojis/842221924997791755.png?size=32',name="Slow it down")
        await ctx.send(embed=embed)
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.command()
@commands.is_owner()
async def gambletrophy(ctx, amount):
    colt = leaugesdb["leagues"]
    b = []
    for x in colt.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colt.insert_one({"USER ID": ctx.author.id, "USER":str(ctx.author),"League": "🔰 Challenger 🔰", "Trophies": 0})
    trophye = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Trophies": 1})["Trophies"]
    league = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "League": 1})["League"]

    gbot = random.randrange(1, 12)
    user = random.randrange(1, 12)

    multiplier = 1

    bonus = None
    trophy = random.randint(10, 100)
    rt = random.randint(1, 5)

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

    amount3 = 0

    if amount == "all" or amount == "max":
        total_amount = 100 if trophye > 100 else trophye

        if total_amount > trophye:
            embed = discord.Embed(description="You don't have enough <:leaguetrophy:891844638380556319>", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
        else:
            if gbot > user:
                embed = discord.Embed(description=f"You lost **{locale.format_string('%d', total_amount, grouping=True)}** <:leaguetrophy:891844638380556319>\n\nYou now have **{locale.format_string('%d', trophye - total_amount, grouping=True)}** <:leaguetrophy:891844638380556319>",color=discord.Color.red())
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
                colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye},{"$set": {"Trophies": trophye - total_amount}})
            elif gbot == user:
                embed = discord.Embed(description=f"You tied!! Your trophies haven't changed!\n\nYou still have **{locale.format_string('%d', trophye, grouping=True)}** <:leaguetrophy:891844638380556319>",color=color)
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
            else:
                embed = discord.Embed(description=f"You won **{locale.format_string('%d', total_amount*multiplier, grouping=True)}** <:leaguetrophy:891844638380556319>\n\nYou now have **{locale.format_string('%d', trophye + total_amount*multiplier, grouping=True)}** <:leaguetrophy:891844638380556319>",color=discord.Color.green())
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
                colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye},{"$set": {"Trophies": trophye + total_amount*multiplier}})
                amount3 = total_amount*multiplier
    else:
        if int(amount) > 500000:
            embed = discord.Embed(description=f"You can only gamble under `100` <:leaguetrophy:891844638380556319>", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
        elif int(amount) <= 0:
            embed = discord.Embed(description="Needs to be greater than 0 <:leaguetrophy:891844638380556319>", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
        elif int(amount) > trophye:
            embed = discord.Embed(description="You don't have enough <:leaguetrophy:891844638380556319>", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
        else:
            if gbot > user:
                embed = discord.Embed(description=f"You lost **{locale.format_string('%d', int(amount), grouping=True)}** <:leaguetrophy:891844638380556319>\n\nYou now have **{locale.format_string('%d', trophye - int(amount), grouping=True)}** <:leaguetrophy:891844638380556319>",color=discord.Color.red())
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
                colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye},{"$set": {"Trophies": trophye - int(amount)}})
            elif gbot == user:
                embed = discord.Embed(description=f"You tied!! Your trophies haven't changed!\n\nYou still have **{locale.format_string('%d', trophye, grouping=True)}** <:leaguetrophy:891844638380556319>",color=discord.Color.yellow())
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
            else:
                embed = discord.Embed(description=f"You won **{locale.format_string('%d', int(amount)*multiplier, grouping=True)}** <:leaguetrophy:891844638380556319>\n\nYou now have **{locale.format_string('%d', int(amount)*multiplier + trophye, grouping=True)}** <:leaguetrophy:891844638380556319>",color=discord.Color.green())
                embed.set_author(name=f"{ctx.author.name}'s gambling game",icon_url=micon)
                embed.add_field(name=f"{ctx.author.name}", value=f"Rolled a `{user}`")
                embed.add_field(name=f"Bot", value=f"Rolled a `{gbot}`")
                colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye},{"$set": {"Trophies": trophye + int(amount)}})
                amount3 = int(amount)*multiplier


    if trophye + amount3 +trophy >= 250 and trophye + amount3 +trophy < 500 and "Novice" not in league:
        await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
        colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🛡️ Novice Tier 🛡️"}})
    elif trophye + amount3 +trophy >= 500 and trophye + amount3 +trophy < 1000 and "Gold" not in league:
        await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
        colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🔱 Gold Tier 🔱"}})
    elif trophye + amount3 +trophy >= 1000 and trophye + amount3 +trophy < 2000 and "Purple Dragon" not in league:
        await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
        colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "⚜️Purple Dragon Tier ⚜️"}})
    elif trophye + amount3 +trophy >= 2000 and trophye + amount3 +trophy < 3000 and "Diamond" not in league:
        await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
        colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "💎 Diamond Tier 💎"}})
    elif trophye + amount3 +trophy >= 3000 and trophye + amount3 +trophy < 4500 and "Master" not in league:
        await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
        colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "⚔️ Master Tier ⚔️"}})
    elif trophye + amount3 +trophy >= 4500 and trophye + amount3 +trophy < 5000 and "Legendary" not in league:
        await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
        colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🃏 Legendary Tier 🃏"}})
    elif trophye + amount3 +trophy >= 5000 and "The Best of the Best" not in league:
        await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
        colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🏴‍☠️ The Best of the Best 🏴‍☠️"}})
    await ctx.send(embed=embed)
@gambletrophy.error
async def gamblet_e(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        embed = discord.Embed(
            description=f"Your on cooldown. **{int(s)} seconds** left\nCheck out the official server, https://discord.gg/cwFU3zRB",
            color=color)
        embed.set_author(icon_url='https://cdn.discordapp.com/emojis/842221924997791755.png?size=32',
                         name="Slow it down")
        await ctx.send(embed=embed)
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.command()
@commands.is_owner()
async def slots(ctx, amount):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Slots": 1})["Slots"]
    colc.update_one({"Slots": tc}, {"$set": {"Slots": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Slots": 1})["Slots"]
    cold.update_one({"Slots": tcd}, {"$set": {"Slots": tcd + 1}})

    slot_random_1 = random.choice(slot_machine_1)
    slot_random_2 = random.choice(slot_machine_2)
    slot_random_3 = random.choice(slot_machine_3)

    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": ctx.author.id} not in a: col.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    colt = leaugesdb["leagues"]
    b = []
    for x in colt.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: colt.insert_one({"USER ID": ctx.author.id, "USER":str(ctx.author),"League": "🔰 Challenger 🔰", "Trophies": 0})
    trophye = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Trophies": 1})["Trophies"]
    league = colt.find_one({"USER ID": ctx.author.id}, {"_id": 0, "League": 1})["League"]

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

    bonus = None
    trophy = random.randint(10, 100)
    rt = random.randint(1, 5)

    if amount == "all" or amount == "max":
        total_amount = 500000 if wallet > 500000 else wallet

        if wallet == 0:
            embed = discord.Embed(description=f"You don't have enough. You have **{pre}0**", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
            await ctx.send(embed=embed)
        else:
            if slot_random_1 == slot_random_2 or slot_random_1 == slot_random_3 or slot_random_2 == slot_random_3:
                if slot_random_1 == slot_random_2:win = int(slot_rate.get(f'{slot_random_1}')*total_amount)
                elif slot_random_1 == slot_random_3:win = int(slot_rate.get(f'{slot_random_1}') * total_amount)
                else:win = int(slot_rate.get(f'{slot_random_2}') * total_amount)

                embed = discord.Embed(title=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
<<<<<<< HEAD
                embed2 = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', win, grouping=True)}** coins.\n**Multiplier:** `{(round(win/total_amount,2))*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet+win, grouping=True)}** coins.",color=discord.Color.green())
=======
                embed2 = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', win, grouping=True)}** coins.\n**Multiplier:** `{(int(win/total_amount))*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet+win, grouping=True)}** coins.",color=discord.Color.green())
>>>>>>> 3cf15a2960ea0efc240f02247cd206762185c240
                embed2.add_field(name="Outcome", value=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
                embed2.set_author(name=f"{ctx.author.name}'s slot machine game", icon_url=micon)
                embed2.set_footer(text="winner winner chicken dinner")

                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet + win}})
            elif slot_random_1 == slot_random_2 == slot_random_3:
                if slot_random_1 == slot_random_2:win = int(slot_rate.get(f'{slot_random_1}')*total_amount*2)
                elif slot_random_1 == slot_random_3:win = int(slot_rate.get(f'{slot_random_1}') * total_amount*2)
                else:win = int(slot_rate.get(f'{slot_random_2}') * total_amount*2)

                embed = discord.Embed(title=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
<<<<<<< HEAD
                embed2 = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', win, grouping=True)}** coins.\n**Multiplier:** `{(round(win/total_amount,2))*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet + win, grouping=True)}** coins.",color=discord.Color.green())
=======
                embed2 = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', win, grouping=True)}** coins.\n**Multiplier:** `{(int(win/total_amount))*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet + win, grouping=True)}** coins.",color=discord.Color.green())
>>>>>>> 3cf15a2960ea0efc240f02247cd206762185c240
                embed2.add_field(name="Outcome", value=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
                embed2.set_author(name=f"{ctx.author.name}'s slot machine game", icon_url=micon)
                embed2.set_footer(text="winner winner chicken dinner")

                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet + win}})
            else:
                embed = discord.Embed(title=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
                embed2 = discord.Embed(description=f"You lost **{pre}{locale.format_string('%d', total_amount, grouping=True)}** coins.\nYou now have **{pre}{locale.format_string('%d', wallet - total_amount, grouping=True)}** coins.",color=discord.Color.red())
                embed2.add_field(name="Outcome", value=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
                embed2.set_author(name=f"{ctx.author.name}'s slot machine game", icon_url=micon)
                embed2.set_footer(text="lose to lose no chicken")

                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - total_amount}})
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(1)
            await msg.edit(embed=embed2)
    else:
        if int(amount) > 500000:
            embed = discord.Embed(description=f"You can only gamble under **`{pre}500,000`**", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
            await ctx.send(embed=embed)
        elif int(amount) > wallet:
            embed = discord.Embed(description=f"You don't have enough. You have **`{pre}{wallet}`**", color=color)
            embed.set_author(name='Warning',icon_url='https://cdn.discordapp.com/emojis/895068510722601021.png?size=32')
            await ctx.send(embed=embed)
        else:
            if slot_random_1 == slot_random_2 or slot_random_1 == slot_random_3 or slot_random_2 == slot_random_3:
                if slot_random_1 == slot_random_2:win = int(slot_rate.get(f'{slot_random_1}')*int(amount))
                elif slot_random_1 == slot_random_3:win = int(slot_rate.get(f'{slot_random_1}') * int(amount))
                else:win = int(slot_rate.get(f'{slot_random_2}') * int(amount))

                embed = discord.Embed(title=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
<<<<<<< HEAD
                embed2 = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', win, grouping=True)}** coins.\n**Mutliplier:** `{(round(win/int(amount),2))*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet + win, grouping=True)}** coins.",color=discord.Color.green())
=======
                embed2 = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', win, grouping=True)}** coins.\n**Mutliplier:** `{(int(win/int(amount)))*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet + win, grouping=True)}** coins.",color=discord.Color.green())
>>>>>>> 3cf15a2960ea0efc240f02247cd206762185c240
                embed2.add_field(name="Outcome",value=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
                embed2.set_author(name=f"{ctx.author.name}'s slot machine game", icon_url=micon)
                embed2.set_footer(text="winner winner chicken dinner")

                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet + win}})
            elif slot_random_1 == slot_random_2 == slot_random_3:
                if slot_random_1 == slot_random_2:win = int(slot_rate.get(f'{slot_random_1}')*int(amount)*2)
                elif slot_random_1 == slot_random_3:win = int(slot_rate.get(f'{slot_random_1}') * int(amount)*2)
                else:win = int(slot_rate.get(f'{slot_random_2}') * int(amount)*2)

                embed = discord.Embed(title=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
<<<<<<< HEAD
                embed2 = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', win, grouping=True)}** coins.\n**Multiplier:** `{(round(win/int(amount),2))*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet + win, grouping=True)}** coins.",color=discord.Color.green())
=======
                embed2 = discord.Embed(description=f"You won **{pre}{locale.format_string('%d', win, grouping=True)}** coins.\n**Multiplier:** `{(int(win/int(amount)))*100}%`\nYou now have **{pre}{locale.format_string('%d', wallet + win, grouping=True)}** coins.",color=discord.Color.green())
>>>>>>> 3cf15a2960ea0efc240f02247cd206762185c240
                embed2.add_field(name="Outcome", value=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
                embed2.set_author(name=f"{ctx.author.name}'s slot machine game", icon_url=micon)
                embed2.set_footer(text="winner winner chicken dinner")

                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + win}})
            else:
                embed = discord.Embed(title=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
                embed2 = discord.Embed(description=f"You lost **{pre}{locale.format_string('%d',int(amount), grouping=True)}** coins.\nYou now have **{pre}{locale.format_string('%d', wallet-int(amount), grouping=True)}** coins.",color=discord.Color.red())
                embed2.add_field(name="Outcome", value=f"**`>` {slot_random_1} {slot_random_2} {slot_random_3} `<`**")
                embed2.set_author(name=f"{ctx.author.name}'s slot machine game", icon_url=micon)
                embed2.set_footer(text="lose to lose no chicken")

                col.update_one({"USER ID": ctx.author.id, "Wallet": wallet},{"$set": {"Wallet": wallet - int(amount)}})
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(1)
            await msg.edit(embed=embed2)

    if rt == 1:
        colt.update_one({"USER ID": ctx.author.id, "Trophies": trophye}, {"$set": {"Trophies": trophye + trophy}})
        bonus = f"{ctx.author.mention} **YOU LUCKY DUCKY!** You also found **`{trophy}` Trophies** <:leaguetrophy:891844638380556319>!"

    if bonus is not None:
        await ctx.send(bonus)

        if trophye + trophy >= 250 and trophye + trophy < 500 and "Novice" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:shield: Novice Tier :shield:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🛡️ Novice Tier 🛡️"}})
        elif trophye + trophy >= 500 and trophye + trophy < 1000 and "Gold" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:trident: Gold Tier :trident:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🔱 Gold Tier 🔱"}})
        elif trophye + trophy >= 1000 and trophye + trophy < 2000 and "Purple Dragon" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:fleur_de_lis: Purple Dragon Tier :fleur_de_lis:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "⚜️Purple Dragon Tier ⚜️"}})
        elif trophye + trophy >= 2000 and trophye + trophy < 3000 and "Diamond" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:gem: Diamond Tier :gem:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "💎 Diamond Tier 💎"}})
        elif trophye + trophy >= 3000 and trophye + trophy < 4500 and "Master" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:crossed_swords: Master Tier :crossed_swords:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "⚔️ Master Tier ⚔️"}})
        elif trophye + trophy >= 4500 and trophye + trophy < 5000 and "Legendary" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:black_joker: Legendary Tier :black_joker:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league}, {"$set": {"League": "🃏 Legendary Tier 🃏"}})
        elif trophye + trophy >= 5000 and "The Best of the Best" not in league:
            await ctx.send(f"{ctx.author.mention} You are now **:pirate_flag: The Best of the Best :pirate_flag:**!!")
            colt.update_one({"USER ID": ctx.author.id, "League": league},{"$set": {"League": "🏴‍☠️ The Best of the Best 🏴‍☠️"}})
@slots.error
async def slots_e(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        embed = discord.Embed(description=f"Your on cooldown. **{int(s)} seconds** left\nCheck out the official server, **[The Revolutionary Support](https://discord.gg/cwFU3zRB)**",color=color)
        embed.set_author(icon_url='https://cdn.discordapp.com/emojis/842221924997791755.png?size=32',name="Slow it down")
        await ctx.send(embed=embed)

"""DAILY COINS"""
@commands.command()
@commands.is_owner()
async def feelinglucky(ctx):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Feelinglucky": 1})["Feelinglucky"]
    colc.update_one({"Feelinglucky": tc}, {"$set": {"Feelinglucky": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Feelinglucky": 1})["Feelinglucky"]
    cold.update_one({"Feelinglucky": tcd}, {"$set": {"Feelinglucky": tcd + 1}})

    col2 = dailydb["daily"]
    b = []
    for x in col2.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: col2.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Daily": None, "Feeling Lucky": None, "Weekly": None, "Monthly":None})
    tf = col2.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Feeling Lucky": 1})["Feeling Lucky"]

    if tf is None:
        cool = True
    else:
        cool = False

    if cool == True:
        col2.update_one({"USER ID": ctx.author.id, "Feeling Lucky": tf}, {"$set": {"Feeling Lucky": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}})

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
        await ctx.send(f"You got your lucky **{pre}{locale.format_string('%d',coins, grouping=True)}!**. Check in again in `24 hours`.")
    else:
        past = datetime(int(tf[0:4]), int(tf[5:7]),
                        int(tf[8:10]), int(tf[11:13]),
                        int(tf[14:16]), int(tf[17:19]))
        duration = past - datetime.utcnow()
        duration2 = datetime.utcnow() - past
        duration_in_s = duration.total_seconds()
        days = divmod(duration_in_s, 86400)  # Get days (without [0]!)
        hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
        minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
        seconds = divmod(minutes[1], 1)
        if duration2.days >= 1:
            col2.update_one({"USER ID": ctx.author.id, "Feeling Lucky": tf}, {"$set": {"Feeling Lucky": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}})

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
            await ctx.send(f"You got your lucky **{pre}{locale.format_string('%d',coins, grouping=True)}!**. Check in again in `24 hours`.")
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

            if int(hours[0]) == 0:
                settime = f"{int(minutes[0])} {suffixm}"
            elif int(minutes[0]) == 0:
                settime = f"{int(hours[0])} {suffixh}"
            else:
                settime = f"{int(hours[0])} {suffixh} and {int(minutes[0])} {suffixm}"
            embed = discord.Embed(description=f"Your on cooldown. **{settime}** left.",
                                  color=color)
            embed.set_author(icon_url='https://cdn.discordapp.com/emojis/842221924997791755.png?size=32',
                             name="Slow it down")
            await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def daily(ctx):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Daily": 1})["Daily"]
    colc.update_one({"Daily": tc}, {"$set": {"Daily": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Daily": 1})["Daily"]
    cold.update_one({"Daily": tcd}, {"$set": {"Daily": tcd + 1}})

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

    col2 = dailydb["daily"]
    b = []
    for x in col2.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: col2.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Daily": None, "Feeling Lucky": None, "Weekly": None, "Monthly":None})
    tf = col2.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Daily": 1})["Daily"]

    if tf is None:
        cool = True
    else:
        cool = False

    if cool == True:
        col2.update_one({"USER ID": ctx.author.id, "Daily": tf}, {"$set": {"Daily": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}})

        col = db["currency"]
        a = []
        for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
        if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
        userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
        if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
        wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
        bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
        bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

        col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + 100000}})
        embed = discord.Embed(title="Daily Coins!",
                              description=f"You got your daily **[{pre}100,000](https://discord.gg/PqChqEGJx8)**!\nCheck in again in `24 hours`!",
                              color=discord.Color.gold())
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/893267135932031026/896469767911780432/4e70c806a58ff7fa2f3a22eccf2f3cdb__2_-removebg-preview.png')
        embed.set_author(name=f'{ctx.author}', icon_url=micon)
        await ctx.send(embed=embed)
    else:
        past = datetime(int(tf[0:4]), int(tf[5:7]),
                        int(tf[8:10]), int(tf[11:13]),
                        int(tf[14:16]), int(tf[17:19]))
        duration = past - datetime.utcnow()
        duration2 = datetime.utcnow() - past
        duration_in_s = duration.total_seconds()
        days = divmod(duration_in_s, 86400)  # Get days (without [0]!)
        hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
        minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
        seconds = divmod(minutes[1], 1)
        if duration2.days >= 1:
            col2.update_one({"USER ID": ctx.author.id, "Daily": tf}, {"$set": {"Daily": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}})

            col = db["currency"]
            a = []
            for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
            if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
            userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
            if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
            wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
            bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
            bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + 100000}})
            embed = discord.Embed(title="Daily Coins!",
                                  description=f"You got your daily **[{pre}100,000](https://discord.gg/PqChqEGJx8)**!\nCheck in again in `24 hours`!",
                                  color=discord.Color.gold())
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/893267135932031026/896469767911780432/4e70c806a58ff7fa2f3a22eccf2f3cdb__2_-removebg-preview.png')
            embed.set_author(name=f'{ctx.author}', icon_url=micon)
            await ctx.send(embed=embed)
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
            if int(hours[0]) == 0:
                settime = f"{int(minutes[0])} {suffixm}"
            elif int(minutes[0]) == 0:
                settime = f"{int(hours[0])} {suffixh}"
            else:
                settime = f"{int(hours[0])} {suffixh} and {int(minutes[0])} {suffixm}"
            embed = discord.Embed(description=f"Your on cooldown. **{settime}** left.",
                                  color=color)
            embed.set_author(icon_url='https://cdn.discordapp.com/emojis/842221924997791755.png?size=32',
                             name="Slow it down")
            await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def weekly(ctx):
    colc = commandsdb["commands"]
    tc = colc.find_one({}, {"_id": 0, "Weekly": 1})["Weekly"]
    colc.update_one({"Weekly": tc}, {"$set": {"Weekly": tc + 1}})
    cold = commandsdb["daily"]
    tcd = cold.find_one({}, {"_id": 0, "Weekly": 1})["Weekly"]
    cold.update_one({"Weekly": tcd}, {"$set": {"Weekly": tcd + 1}})

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

    col2 = dailydb["daily"]
    b = []
    for x in col2.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: col2.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Daily": None, "Feeling Lucky": None, "Weekly": None, "Monthly":None})
    tf = col2.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Weekly": 1})["Weekly"]

    if tf is None:
        cool = True
    else:
        cool = False

    if cool == True:
        col2.update_one({"USER ID": ctx.author.id, "Weekly": tf}, {"$set": {"Weekly": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}})

        col = db["currency"]
        a = []
        for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
        if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
        userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
        if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
        wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
        bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
        bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

        col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + 1000000}})
        embed = discord.Embed(title="Weekly Coins!",
                              description=f"You got your weekly **[{pre}1,000,000](https://discord.gg/PqChqEGJx8)**!\nCheck in again in `7 days`!",
                              color=discord.Color.gold())
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/893267135932031026/896469767911780432/4e70c806a58ff7fa2f3a22eccf2f3cdb__2_-removebg-preview.png')
        embed.set_author(name=f'{ctx.author}', icon_url=micon)
        await ctx.send(embed=embed)
    else:
        past = datetime(int(tf[0:4]), int(tf[5:7]),
                        int(tf[8:10]), int(tf[11:13]),
                        int(tf[14:16]), int(tf[17:19]))
        duration =timedelta(days=7)-(datetime.now() - past)
        duration2 = datetime.utcnow() - past
        duration_in_s = duration.total_seconds()
        days = divmod(duration_in_s, 86400)  # Get days (without [0]!)
        hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
        minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
        seconds = divmod(minutes[1], 1)
        if duration2.days >= 7:
            col2.update_one({"USER ID": ctx.author.id, "Weekly": tf}, {"$set": {"Weekly": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}})

            col = db["currency"]
            a = []
            for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
            if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
            userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
            if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
            wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
            bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
            bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + 1000000}})
            embed = discord.Embed(title="Weekly Coins!",
                                  description=f"You got your weekly **[{pre}1,000,000](https://discord.gg/PqChqEGJx8)**!\nCheck in again in `7 days`!", color=discord.Color.gold())
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/893267135932031026/896469767911780432/4e70c806a58ff7fa2f3a22eccf2f3cdb__2_-removebg-preview.png')
            embed.set_author(name=f'{ctx.author}', icon_url=micon)
            await ctx.send(embed=embed)
        else:
            suffixh = ""
            suffixm = ""
            suffixs = ""
            suffixd = ""
            if int(days[0]) == 1:
                suffixd = "day"
            else:
                suffixd = "days"
            if int(hours[0]) == 1:
                suffixh = "hour"
            else:
                suffixh = "hours"
            if int(minutes[0]) == 1:
                suffixm = "minute"
            else:
                suffixm = "minutes"

            if int(days[0]) == 0:
                settime=f"{int(hours[0])} {suffixh} and {int(minutes[0])} {suffixm}"
            elif int(hours[0]) == 0:
                settime = f"{int(days[0])} {suffixd} and {int(minutes[0])} {suffixm}"
            elif int(minutes[0]) == 0:
                settime= f"{int(days[0])} {suffixd} and {int(hours[0])} {suffixh}"
            else:
                settime = f"{int(days[0])} {suffixd}, {int(hours[0])} {suffixh} and {int(minutes[0])} {suffixm}"
            embed = discord.Embed(description=f"Your on cooldown. **{settime}** left.",
                                  color=color)
            embed.set_author(icon_url='https://cdn.discordapp.com/emojis/842221924997791755.png?size=32',
                             name="Slow it down")
            await ctx.send(embed=embed)
@commands.command()
@commands.is_owner()
async def monthly(ctx):

    micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

    col2 = dailydb["daily"]
    b = []
    for x in col2.find({}, {"_id": 0, "USER ID": 1}): b.append(x)
    if {"USER ID": ctx.author.id} not in b: col2.insert_one({"USER ID": ctx.author.id, "USER": str(ctx.author), "Daily": None, "Feeling Lucky": None, "Weekly": None, "Monthly":None})

    tf = col2.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Monthly": 1})["Monthly"]

    if tf is None:
        cool = True
    else:
        cool = False

    if cool == True:
        col2.update_one({"USER ID": ctx.author.id, "Monthly": tf}, {"$set": {"Monthly": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}})

        col = db["currency"]
        a = []
        for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
        if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
        userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
        if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
        wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
        bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
        bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

        col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + 5000000}})
        embed = discord.Embed(title="Monthly Coins!",
                              description=f"You got your monthly **[{pre}5,000,000](https://discord.gg/PqChqEGJx8)**!\nCheck in again in `30 days`!",
                              color=discord.Color.gold())
        embed.set_thumbnail(
            url='https://media.discordapp.net/attachments/893267135932031026/896469767911780432/4e70c806a58ff7fa2f3a22eccf2f3cdb__2_-removebg-preview.png')
        embed.set_author(name=f'{ctx.author}', icon_url=micon)
        await ctx.send(embed=embed)
    else:
        past = datetime(int(tf[0:4]), int(tf[5:7]),
                        int(tf[8:10]), int(tf[11:13]),
                        int(tf[14:16]), int(tf[17:19]))
        duration =timedelta(days=30)-(datetime.now() - past)
        duration2 = datetime.utcnow() - past
        duration_in_s = duration.total_seconds()
        days = divmod(duration_in_s, 86400)  # Get days (without [0]!)
        hours = divmod(days[1], 3600)  # Use remainder of days to calc hours
        minutes = divmod(hours[1], 60)  # Use remainder of hours to calc minutes
        seconds = divmod(minutes[1], 1)
        if duration2.days >= 30:
            col2.update_one({"USER ID": ctx.author.id, "Monthly": tf}, {"$set": {"Monthly": f'{datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}'}})

            col = db["currency"]
            a = []
            for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
            if {"USER ID": ctx.author.id} not in a:col.insert_one({"USER ID":ctx.author.id,"USER":str(ctx.author),"Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
            userr = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "USER": 1})["USER"]
            if userr != str(ctx.author): col.update_one({"USER ID": ctx.author.id, "USER": userr},{"$set": {"USER": str(ctx.author)}})
            wallet = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
            bank = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank": 1})["Bank"]
            bankl = col.find_one({"USER ID": ctx.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

            col.update_one({"USER ID": ctx.author.id, "Wallet": wallet}, {"$set": {"Wallet": wallet + 5000000}})
            embed = discord.Embed(title="Monthly Coins!",
                                  description=f"You got your monthly **[{pre}5,000,000](https://discord.gg/PqChqEGJx8)**!\nCheck in again in `30 days`!",
                                  color=discord.Color.gold())
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/893267135932031026/896469767911780432/4e70c806a58ff7fa2f3a22eccf2f3cdb__2_-removebg-preview.png')
            embed.set_author(name=f'{ctx.author}', icon_url=micon)
            await ctx.send(embed=embed)
        else:
            suffixh = ""
            suffixm = ""
            suffixs = ""
            suffixd = ""
            if int(days[0]) == 1:
                suffixd = "day"
            else:
                suffixd = "days"
            if int(hours[0]) == 1:
                suffixh = "hour"
            else:
                suffixh = "hours"
            if int(minutes[0]) == 1:
                suffixm = "minute"
            else:
                suffixm = "minutes"

            if int(days[0]) == 0:
                settime = f"{int(hours[0])} {suffixh} and {int(minutes[0])} {suffixm}"
            elif int(hours[0]) == 0:
                settime = f"{int(days[0])} {suffixd} and {int(minutes[0])} {suffixm}"
            elif int(minutes[0]) == 0:
                settime = f"{int(days[0])} {suffixd} and {int(hours[0])} {suffixh}"
            else:
                settime = f"{int(days[0])} {suffixd}, {int(hours[0])} {suffixh} and {int(minutes[0])} {suffixm}"
            embed = discord.Embed(description=f"Your on cooldown. **{settime}** left.\nIn the mean time, check the official support server! **[The Revolutionary Support](https://discord.gg/PqChqEGJx8)**",
                                  color=color)
            embed.set_author(icon_url='https://cdn.discordapp.com/emojis/842221924997791755.png?size=32',
                             name="Slow it down")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(farm)
    bot.add_command(collect)
    bot.add_command(grow)
    bot.add_command(monthly)
    bot.add_command(gambletrophy)
    bot.add_command(gamble)
    bot.add_command(weekly)
    bot.add_command(fsell)
    bot.add_command(setprized)
    bot.add_command(buy)
    bot.add_command(use)
    bot.add_command(inventory)
    bot.add_command(shop)
    bot.add_command(profile)
    bot.add_command(leagues)
    bot.add_command(fish)
    #bot.add_command(dice)
    bot.add_command(top)
    bot.add_command(daily)
    bot.add_command(feelinglucky)
    bot.add_command(flipcoin)
    bot.add_command(mystocks)
    bot.add_command(stock)
    bot.add_command(slots)
    bot.add_command(dep)
    bot.add_command(withdraw)
    bot.add_command(balance)
    bot.add_command(give)
    bot.add_command(toptrophies)
