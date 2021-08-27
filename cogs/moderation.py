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
# import fuzzywuzzy (NEXT UPDATE)

cwd = Path(__file__).parents[0]
cwd = str(cwd)
default = "+"
status = [False, False, False, False]
statusdetails = [True, False, False, False]
efile = 'C:/Users/Hao/PycharmProjects/master/error logs'
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

async def cu(command, db):
    db["Total"][f"{command}"] += 1
    db["Daily"][f"{command}"] += 1
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

bot = Bot(command_prefix=determine_prefix, intents=discord.Intents().all(), owner_ids=[497903117241810945, 567487802900480000])
bot.blacklisted_users = []
bot.remove_command('help')

@commands.command(aliases=["Ban", "BAN"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Ban", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    await member.ban(reason=reason)
    await ctx.send(f"**{member}** has been banned by {ctx.author}")
@ban.error
async def be(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(description=f"{error}", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description="**Missing Required Argument:** `Member`", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="Your missing `BAN_MEMBERS` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description="Bot is missing `BAN_MEMBERS` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)

@commands.command(aliases=["Kick", "KICK"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Kick", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    await member.kick(reason=reason)
    await ctx.send(f"**{member}** has been kicked by {ctx.author}")
@kick.error
async def ke(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(description="Member Not Found", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description="Missing Required Argument: Member", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="Your missing `KICK MEMBERS` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description="Bot is missing `KICK MEMBERS` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)

@commands.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, member: discord.Member, *, reason=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Unban", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    await member.unban(reason=reason)
    await ctx.send(f"**{member}** has been unbanned by {ctx.author}")
@unban.error
async def ue(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(description="Member Not Found", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description="Missing Required Argument: Member", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="Your missing `BAN MEMBERS` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description="Bot is missing `BAN MEMBERS` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)

@commands.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason= None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Mute", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    with open('serverdb.json', "r") as f:
        prefix = json.load(f)

    if str(ctx.author.guild.id) in prefix:
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None: theprefix = default
        else: theprefix = prefix[str(ctx.author.guild.id)]["Prefix"]
    else: theprefix = default
    if str(ctx.author.guild.id) in prefix:
        if prefix[str(ctx.author.guild.id)]["Mute Role"] is None:
            cool = False
        else:
            cool = True
    else:
        cool = False

    if cool == False:
        embed = discord.Embed(description=f"Mute role is not set\n**`{theprefix}setmuterole [Role]`**", color=color)
    else:
        guild = ctx.author.guild
        role_id = prefix[str(ctx.author.guild.id)]["Mute Role"]
        role = discord.utils.get(guild.roles, id=role_id)
        await member.add_roles(role)
        embed = discord.Embed(description=f"`{member}` | {member.mention} is **MUTED**.\n**Reason:** {reason}", color=color)
    await ctx.send(embed=embed)
@mute.error
async def me(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(description="Member Not Found", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description="Missing Required Argument: Member", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="Your missing `MANAGE ROLES` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description="Bot is missing `MANAGE ROLES` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)

@commands.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Unmute", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    with open('serverdb.json', "r") as f:
        prefix = json.load(f)

    if str(ctx.author.guild.id) in prefix:
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None:
            theprefix = default
        else:
            theprefix = prefix[str(ctx.author.guild.id)]["Prefix"]
    else:
        theprefix = default
    if str(ctx.author.guild.id) in prefix:
        if prefix[str(ctx.author.guild.id)]["Mute Role"] is None:
            cool = False
        else:
            cool = True
    else:
        cool = False

    if cool == False:
        embed = discord.Embed(description=f"Mute role is not set\n**`{theprefix}setmuterole [Role]`**", color=color)
    else:
        guild = ctx.author.guild
        role_id = prefix[str(ctx.author.guild.id)]["Mute Role"]
        role = discord.utils.get(guild.roles, id=role_id)
        await member.remove_roles(role)
        embed = discord.Embed(description=f"`{member}` | {member.mention} is **UNMUTED**.\n**Reason:** {reason}", color=color)
    await ctx.send(embed=embed)
@unmute.error
async def une(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(description="Member Not Found", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description="Missing Required Argument: Member", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="Your missing `MANAGE ROLES` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description="Bot is missing `MANAGE ROLES` permission`", color=discord.Color.gold())
        await ctx.send(embed=embed)

@commands.command(aliases=["Clear", "Purge", "purge", "PURGE", "CLEAR", "P", "p"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=int(amount))
    if int(amount) == 1:
        suffix = "message"
    else:
        suffix = "messages"
    message = await ctx.send(f"**`{int(amount)}`** {suffix} were deleted.")
    time.sleep(2)
    await message.delete()

def setup(bot):
    bot.add_command(clear)
    bot.add_command(ban)
    bot.add_command(kick)
    bot.add_command(unban)
    bot.add_command(mute)
    bot.add_command(unmute)
