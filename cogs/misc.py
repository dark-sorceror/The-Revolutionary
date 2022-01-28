import time
import asyncio
import random
import json
import re
import sys
import typing
import pymongo
import locale
import praw
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus
from pathlib import Path
from num2words import num2words
from collections import Counter

import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot

from variables import (
    default_prefix,
    color,
    cu,
    bot,
    owners,
    cfeedback
)

async def us(guild_id, db):
    if not str(guild_id) in db:
        db[str(guild_id)] = {}
    else:
        return
async def css(guild_id, db, content, author, id):
    db[str(guild_id)][f"{author} | {id}"] = str(content)

# Up to Date
@commands.command(aliases=["Date", "DATE", "Today", "today", "now", "Now"])
@commands.is_owner()
async def date(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Date", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)

    #FORMATTING
    if int(datetime.utcnow().__format__("%d")) >= 10 and int(datetime.utcnow().__format__("%d")) <= 20: snt = "th"
    else:
        if int(datetime.utcnow().__format__("%d")[-1]) == 1:snt = "st"
        elif int(datetime.utcnow().__format__("%d")[-1]) == 2:snt = "nd"
        elif int(datetime.utcnow().__format__("%d")[-1]) == 3:snt = "rd"
        else:snt = "th"
    if int(datetime.utcnow().__format__("%d")[0]) == 0:drd = int(datetime.utcnow().__format__("%d")[1])
    else:drd = int(datetime.utcnow().__format__("%d"))

    embed = discord.Embed(title=f"{datetime.utcnow().strftime('%I:%M %p')} UTC",description=f"{datetime.utcnow().__format__('%A, %B')} {drd}{snt}",color=color)
    embed.set_author(name="The Revolutionary",icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
    embed.set_footer(text="Current Timezone: Universal Coordinated Time")
    await ctx.reply(embed=embed, mention_author=True)

# Up to Date
@commands.command(aliases=["ui", "UI", "Ui", "Userinfo", "USERINFO", "UserInfo"])
@commands.is_owner()
async def userinfo(ctx, member: discord.Member = None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Userinfo", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    if member is None:
        if ctx.author.status is discord.Status.offline:ms = "<:offline:883116572904923138> Offline"
        elif ctx.author.status is discord.Status.online:
            if ctx.author.is_on_mobile() == True:ms = "<:mobile:883116501178122240> Mobile"
            elif ctx.author.activity is not None and ctx.author.activity.type is discord.ActivityType.streaming: ms="<:streaming:883116541531545630>"
            else:ms = "<:online:883116554298990605> Online"
        elif ctx.author.status is discord.Status.idle:ms = "<:idle:883116602332160000> Idle"
        elif ctx.author.status is discord.Status.dnd:ms = "<:dnd:883116589531160576> Do Not Disturb"
        else:ms = "unknown"
        micon = ctx.author.default_avatar if not ctx.author.avatar else ctx.author.avatar.url

        embed = discord.Embed(title=f"{ctx.author.name}'s info.",description=f"This account belongs to {ctx.author.mention}",colour=ctx.author.color)
        embed.set_thumbnail(url=f"{micon}")
        embed.set_author(name=f"{ctx.author}",icon_url=f"{micon}")
        embed.add_field(name='Created at',value=f'{discord.utils.format_dt(discord.utils.snowflake_time(ctx.author.id), style="D")}\n({discord.utils.format_dt(discord.utils.snowflake_time(ctx.author.id), style="R")})',inline=True)
        embed.add_field(name='Joined at',value=f'{discord.utils.format_dt(ctx.author.joined_at, style="D")}\n({discord.utils.format_dt(ctx.author.joined_at, style="R")})',inline=True)
        embed.add_field(name="Status", value=f'{ms}', inline=True)
        embed.add_field(name="Roles", value=f'{len(ctx.author.roles)}', inline=True)
        embed.add_field(name="Highest Role", value=f"{ctx.author.top_role.mention}", inline=True)
        embed.set_footer(text=f"ID: {ctx.author.id}")
        await ctx.send(embed=embed)
    else:
        thelist = []
        if member.status is discord.Status.offline:ms = "<:offline:883116572904923138> Offline"
        elif member.status is discord.Status.online:
            if member.is_on_mobile() == True:ms = "<:mobile:883116501178122240> Mobile"
            elif member.activity is not None and member.activity.type is discord.ActivityType.streaming: ms="<:streaming:883116541531545630> Streaming"
            else:ms = "<:online:883116554298990605> Online"
        elif member.status is discord.Status.idle:ms = "<:idle:883116602332160000> Idle"
        elif member.status is discord.Status.dnd:ms = "<:dnd:883116589531160576> Do Not Disturb"
        else:ms = "unknown"

        #MUTUAL GUILDS
        for a in member.mutual_guilds:
            thelist.append(f"(`{a.id}`) ─ **{a}**")

        micon = member.default_avatar if not member.avatar else member.avatar.url

        embed = discord.Embed(title=f"{member.name}'s info.", description=f"This account belongs to {member.mention}",colour=member.color)
        embed.set_thumbnail(url=f"{micon}")
        embed.set_author(name=f"{member}",icon_url=f"{micon}")
        embed.add_field(name='Created on',value=f'{discord.utils.format_dt(discord.utils.snowflake_time(member.id), style="D")}\n({discord.utils.format_dt(discord.utils.snowflake_time(member.id), style="R")})',inline=True)
        embed.add_field(name='Joined on',value=f'{discord.utils.format_dt(member.joined_at, style="D")}\n({discord.utils.format_dt(member.joined_at, style="R")})',inline=True)
        embed.add_field(name="Status", value=f'{ms}', inline=True)
        embed.add_field(name="Roles", value=f'{len(member.roles)}', inline=True)
        embed.add_field(name="Highest Role", value=f"{member.top_role.mention}", inline=True)
        embed.add_field(name="Mutual Servers", value="\n".join(b for b in thelist), inline=False)
        embed.set_footer(text=f"ID: {member.id}")
        await ctx.send(embed=embed)
@userinfo.error
async def ue(ctx, error):
    if isinstance(error, commands.BadArgument):await ctx.send(f"{error}")

@commands.command()
@commands.is_owner()
async def guserinfo(ctx, member:discord.User):
    thelist = []

    # MUTUAL GUILDS
    for a in member.mutual_guilds: thelist.append(f"(`{a.id}`) ─ **{a}**")

    micon = member.default_avatar if member.avatar is None else member.avatar.url

    word = "\n".join(b for b in thelist)

    if len(word) == 0: word = "None"
    else: word = "\n".join(b for b in thelist)

    embed = discord.Embed(title=f"{member.name}'s Basic Info.", colour=member.color)
    embed.set_thumbnail(url=micon)
    embed.set_author(name=f"{member}", icon_url=micon)
    embed.add_field(name="User",value=f"{member}\n({member.mention})", inline=True)
    embed.add_field(name='Created at',value=f'{discord.utils.format_dt(discord.utils.snowflake_time(member.id), style="D")}\n({discord.utils.format_dt(discord.utils.snowflake_time(member.id), style="R")})',inline=True)
    embed.add_field(name="Mutual Servers", value=f"{word}", inline=False)
    embed.set_footer(text=f"ID: {member.id}")
    await ctx.send(embed=embed)

@commands.command()
@commands.is_owner()
async def snowflake(ctx, arg:int):
    pass

@commands.command()
@commands.is_owner()
async def allroles(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Allroles", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)

    if not ctx.author.guild.icon: guildicon = 'https://cdn.discordapp.com/attachments/865342805107015722/871546487220359229/dd4dbc0016779df1378e7812eabaa04d.png'
    else: guildicon = ctx.author.guild.icon

    roles = [role for role in ctx.author.guild.roles if not role.is_bot_managed() or role.is_default()]
    for a in roles:
        if a.is_default():
            roles.remove(a)
    newroles = []
    embed = discord.Embed(color=discord.Color.from_rgb(47, 49, 54))
    embed.add_field(name=f"Server Roles ({len(roles)})", value=" ".join(role.mention for role in roles),inline=False)
    embed.set_author(name=f"{ctx.author.guild.name} Roles", icon_url=f"{guildicon}")
    embed.add_field(name=f"Your Roles ({len(ctx.author.roles)}/{len((roles))})", value=" ".join(role.mention for role in ctx.author.roles))
    await ctx.send(embed=embed)

@commands.command()
@commands.is_owner()
async def channels(ctx):
    text_channel_list = []
    for channel in ctx.author.guild.channels:
        await ctx.send(f"{channel}")

# Finished
@commands.command(aliases=["av", "AV", "Av", "AVATAR", "Avatar"])
@commands.is_owner()
async def avatar(ctx, *, member: discord.Member = None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Avatar", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    if member is None:
        pfp = ctx.author.avatar.url
        embed = discord.Embed(title="Avatar", color=ctx.author.color)
        embed.set_image(url=pfp)
        embed.set_author(name=f"{ctx.author}", icon_url=pfp)
        await ctx.send(embed=embed)
    else:
        micon = member.default_avatar if not member.avatar else member.avatar.url
        embed = discord.Embed(title="Avatar", colour=member.color)
        embed.set_image(url=micon)
        embed.set_author(name=f"{member}", icon_url=micon)
        await ctx.send(embed=embed)
@avatar.error
async def ae(ctx, error):
    if isinstance(error, commands.BadArgument):await ctx.send(f"{error}")

# Finished
@commands.command(aliases=["Bon", "BON"])
@commands.is_owner()
async def bon(ctx, member: discord.Member = None, reason=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Bon", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    if member is None:await ctx.send(f"Banned **{ctx.author}**.\nReason: **{reason}**")
    else:await ctx.send(f"Banned **{member}**.\nReason: **{reason}**")

# Error
@commands.command(aliases=["Pat", "PAT"])
@commands.is_owner()
async def pat(ctx, member:discord.Member=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Pat", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    if member is None:await ctx.reply("You pat yourself!", mention_author=False)
    else:await ctx.reply(f"**{ctx.message.author.name}** pats **{member.name}** <a:3hearts:865361826723528734>",mention_author=False)

# Finished
@commands.command(aliases=["Help", "HELP"])
@commands.is_owner()
async def help(ctx, arg=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Help", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    with open('serverdb.json', "r") as f:prefix = json.load(f)

    if str(ctx.author.guild.id) not in prefix:sp = default_prefix
    else:
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None:sp = default_prefix
        else:sp = prefix[str(ctx.author.guild.id)]["Prefix"]

    if arg is None:
        embed = discord.Embed(title="Bot Commands",description=f"Use the dropdown menu below\n\n**Weekly Command Spotlight** \n**`{sp}pban`** ─ Vote ban someone in the server! (jk)",color=color, url='https://discord.com/api/oauth2/authorize?client_id=868699834461347880&permissions=8&scope=bot')
        embed.add_field(name=":wrench: | Info/Utility", value="[Hover for Info](https://google.com 'Multi-purpose commands and information')\nSelect `Info/Utilities`", inline=True)
        embed.add_field(name=":tada: | Fun/Misc", value="[Hover for Info](https://google.com 'Fun and entertaining commands for everyone')\nSelect `Fun/Misc`", inline=True)
        embed.add_field(name=":medal: | Activity", value="[Hover for Info](https://google.com 'Interactive mini-games if your bored')\nSelect `Activities`", inline=True)
        embed.add_field(name=":hammer: | Moderation", value="[Hover for Info](https://google.com 'Powerful moderation commands')\nSelect `Moderation`", inline=True)
        embed.add_field(name=":dollar: | Currency", value="[Hover for Info](https://google.com 'Play with a Currency simulation')\nSelect `Currency`", inline=True)
        embed.add_field(name=":gear: | Bot Configuration", value="[Hover for Info](https://google.com 'Configure this bot in your server')\nSelect `Bot Configuration`", inline=True)
        embed.set_footer(text=f"Created by {owners[0]} and {owners[1]}")
        my_view = helpbuttons(timeout=10)
        out = await ctx.reply(embed=embed, view=my_view, mention_author=False)
        my_view.response = out
        my_view.user = ctx.author.id
    else:
        if arg.lower() == "avatar" or arg.lower() == "av":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}avatar [member]```\nReturn a members avatar in a larger view.\n\nWhen `Member` is unfilled, the command returns your avatar. `Member` can either be a mention or ID.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Avatar",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Examples",
                            value=f"```{sp}avatar <@868699834461347880>\n{sp}av 868699834461347880```",inline=False)
            embed.add_field(name="Aliases", value='`avatar`, `av`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "userinfo" or arg.lower() == "ui":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}userinfo [member]```\nReturn a members information such as when they joined ect.\n\nWhen `Member` is unfilled, the command returns your userinfo. `Member` can either be a mention or ID.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Userinfo",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Examples",
                            value=f"```{sp}userinfo <@868699834461347880>\n{sp}ui 868699834461347880```", inline=False)
            embed.add_field(name="Aliases", value='`ui`, `userinfo`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "botinfo" or arg.lower() == "binfo":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}botinfo```\nReturns information about this bot, such as version, uptime ect.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Botinfo",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`botinfo`, `binfo`')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "version" or arg.lower() == "versioninfo" or arg.lower() == "botversion":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}version```\nThe current version of this bot""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Version",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`botversion`, `version`, `versioninfo`')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "uptime":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}uptime```\nThe current uptime of this bot""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Uptime",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`uptime`')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "date" or arg.lower() == "today":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}date```\nGet today's current date and time (UTC)""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Date",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`date`, `today`')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "invite":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}invite```\nGet a link to the official support server of this bot and a link to invite this bot to your favored server""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Invite",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`invite`')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "serverinfo" or arg.lower() == "si":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}serverinfo```\nView information about this current server such as when it was created ect.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Serverinfo",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`serverinfo`, `si`')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "ping" or arg.lower() == "latency":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}ping```\nGet the bot latency and Discord API latency""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Ping",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`ping`, `latency`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "taxcalc" or arg.lower() == "tc":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}taxcalc [amount]```\n**Amount** must be a counting number (1+), so no decimals or negatives ect.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Taxcalc",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`taxcalc`, `tc`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "bon":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}bon [member]```\nBan a member from the server (jk)\n\nWhen `Member` is unfilled, you ban yourself :| `Member` can either be a mention or ID.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Bon",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`bon`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "pat":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}pat [member]```\nPat someone\n\nWhen `Member` is unfilled, you pat yourself :| `Member` can either be a mention or ID.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Pat",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`pat`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "google":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}google```\nGoogle something on the internet quickly... or if your too lazy to open your browser.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Google",icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`google`, `search`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "say":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}say [message...]```\nThe bot will say something you make it say""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Say",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`say`', inline=False)
        elif arg.lower() == "flipcoin":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}flipcoin [coin face]```\nFlip a coin. Coinface can be `Heads` or `Tails`. If you guess the correct landing coin face, you get a some coins!""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Flipcoin",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`flipcoin`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "flipcoin":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}choose [choices...]```\nThe bot will choose from a list of your sort.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Choose",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`choose`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "timer":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}timerstart [time] [message...]```\nStart a timer""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Timer",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Examples",
                            value=f"```{sp}tstart 1m Eat Dinner\n{sp}tstart 55m Zoom Meeting```", inline=False)
            embed.add_field(name="Aliases", value='`choose`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "num2word":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}num2word [number]```\nTurn numbers into words""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Num2Word",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`num2word`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "emojify":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}emojify [message...]```\nEmojify a message of your choice""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Emojify",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`emojify`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "simprate":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}simprate [member]```\nHow simp are you or your friends?\n\nWhen `Member` is unfilled, the command returns your simprate. `Member` can either be a mention or ID.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Simprate",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`simprate`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "hello":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}hello```\nHello!""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Hello",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`hello`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "membercount":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}membercount```\nReturn the servers member count""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: MemberCount",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`membercount`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "allroles":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}allroles```\nDisplay the servers roles including your own.""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Allroles",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`allroles`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
        elif arg.lower() == "guess":
            embed = discord.Embed(description=f"""
```yaml
Syntax: {sp}guess [minimum] [maximum]```\nGet 3 tries to guess number between **minimum** and **maximum**.\n\nWhen **minimum number** and **maximum number** are unfilled, the default is **1-20**""",
                                  color=discord.Color.gold())
            embed.set_author(name="Command Help: Guess",
                             icon_url="https://cdn.discordapp.com/attachments/690681407256789012/867229851735031867/c9c0406416e18421fc203dd3c8a2dba7.png")
            embed.add_field(name="Aliases", value='`guess`', inline=False)
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await ctx.reply(embed=embed, mention_author=False)
class helpbuttons(discord.ui.View):
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

    @discord.ui.select(placeholder="Command Categories", options=[
        discord.SelectOption(label="Info/Utilities", value="Info",description="Multi-purpose commands and information",emoji="🔧"),
        discord.SelectOption(label="Fun/Misc", value="Fun",description="Fun and entertaining commands for everyone", emoji="🎉"),
        discord.SelectOption(label="Activities", value="Activity", description="Interactive mini-games if your bored", emoji="🏅"),
        discord.SelectOption(label="Moderation", value="Moderation", description="Powerful moderation commands", emoji="🔨"),
        discord.SelectOption(label="Currency", value="Currency", description="Play with a Currency simulation", emoji="💵"),
        discord.SelectOption(label="Bot Configuration", value="BC", description="Configure this bot in your server",emoji="⚙️")])
    async def dropdown(self, select: discord.ui.Select, interaction: discord.Interaction):
        with open('serverdb.json', "r") as f:
            prefix = json.load(f)
        if str(interaction.guild_id) in prefix:
            if prefix[str(interaction.guild_id)]["Prefix"] is None:
                sp = default_prefix
            else:
                sp = prefix[str(interaction.guild_id)]["Prefix"]
        else:
            sp = default_prefix
        if select.values[0] == 'Info':
            embed = discord.Embed(title=":wrench: Info/Utility Commands", description=f"""
Make sure to include **`{sp}`** as the prefix for each command below.

<:replystart:895447277622161469>`Date` - View today's date (UTC for now)
<:Reply:882064180251877416>`Userinfo` - Information about a specific user

[**Bot Information**](https://google.com "Information about this bot")
Hover for Info
<:Reply:882064180251877416>`Botinfo`, `Invite`, `Ping`, `Uptime`, `Version`

[**Dank Memer**](https://google.com "Dank Memer Utilities to help you")
Hover for Info
<:Reply:882064180251877416>`Taxcalc`, `Tradeshop`

[**Server Information**](https://google.com "Information and display stats about this server")
Hover for Info
<:Reply:882064180251877416>`Allroles`, `Channels`, `Emojilist`, `MemberCount`, `Serverinfo`
""", color=color, url='https://discord.com/api/oauth2/authorize?client_id=868699834461347880&permissions=8&scope=bot')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await interaction.response.edit_message(embed=embed, view=self)
        elif select.values[0] == "Fun":
            embed = discord.Embed(title=":tada: Fun/Miscellaneous Commands",
                                  description=f"""
Make sure to include **`{sp}`** as the prefix for each command below.

<:replystart:895447277622161469>`Avatar` - View someone's avatar
<:ReplyContinue:882064049850961981>`Choose` - The bot will choose from a list of your sort
<:Reply:882064180251877416>`Commandlb` - Shows the top 10 most used commands

[**Google**](https://google.com "Google something quickly in Discord")
Hover for Info
<:Reply:882064180251877416>`Google`

[**Output**](https://google.com "Input and Output")
Hover for Info
<:Reply:882064180251877416>`Emojify`, `Num2Word`

[**Rates**](https://google.com "Rates in percentage or just numbers")
Hover for Info
<:Reply:882064180251877416>`IQrate`, `Luck`, `Simprate`

[**Roleplay**](https://google.com "Roleplay with your friends")
Hover for Info
<:Reply:882064180251877416>`Bon`, `Hello`, `Pat`, ~~`Pban`~~, `Say`

[**Timer**](https://google.com "Start a timer")
Hover for Info
<:Reply:882064180251877416>`Timerstart`
""", color=color, url='https://discord.com/api/oauth2/authorize?client_id=868699834461347880&permissions=8&scope=bot')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await interaction.response.edit_message(embed=embed, view=self)
        elif select.values[0] == "Activity":
            embed = discord.Embed(title=":medal: Activity Commands",
                                  description=f"""
Make sure to include **`{sp}`** as the prefix for each command below.

<:replystart:895447277622161469>`Guess` - Guess a number from your choice **(default: 1-20)**
<:ReplyContinue:882064049850961981>`TicTacToe` - Play tictactoe with your friend
<:Reply:882064180251877416>`Revolution` - Play war with your friend
""",
                                  color=discord.Color.gold(), url='https://discord.com/api/oauth2/authorize?client_id=868699834461347880&permissions=8&scope=bot')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await interaction.response.edit_message(embed=embed, view=self)
        elif select.values[0] == "Moderation":
            embed = discord.Embed(title=":hammer: Moderation Commands",
                                  description=f"""
Make sure to include **`{sp}`** as the prefix for each command below.

[**Actions**](https://google.com "Powerful and quick actions ready anytime")
Hover for Info
<:Reply:882064180251877416>`Ban`, `Kick`, `Mute`, `Unban`, `Unmute`

[**Delete Messages**](https://google.com "Delete/purge a set amount of messages")
Hover for Info
<:Reply:882064180251877416>`Purge`

[**Utilities**](https://google.com "Quick utilities to use")
Hover for Info
<:Reply:882064180251877416>`Dump`
""", color=color, url='https://discord.com/api/oauth2/authorize?client_id=868699834461347880&permissions=8&scope=bot')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await interaction.response.edit_message(embed=embed, view=self)
        elif select.values[0] == "Currency":
            #add currency help
            embed = discord.Embed(title=":dollar: Currency Commands",
                                  description=f"""
Make sure to include **`{sp}`** as the prefix for each command below.

[**Economy**](https://google.com "Basic currency commands")
Hover for Info
<:Reply:882064180251877416>`Balance`, `Daily`, `Deposit`, `Feelinglucky`, `Give`, `Profile`, `Top`, `Withdraw`

[**Fishing**](https://google.com "Fishy fish fish")
Hover for Info
<:Reply:882064180251877416>`Fish`, `Fsell`, `Myfish`

[**Gambling**](https://google.com "Gamble some coins")
Hover for Info
<:Reply:882064180251877416>`Flipcoin`, `Gamble`

[**Leaderboards**](https://google.com "List of top 10 users")
Hover for Info
<:Reply:882064180251877416>`Top`, `Toptrophy`

[**Leagues**](https://google.com "The Leagues")
Hover for Info
<:Reply:882064180251877416>`Leagues`

[**Stocks**](https://google.com "Stonks stonks stonks")
Hover for Info
<:Reply:882064180251877416>`Stocks`, `Mystocks`
""", color=color, url='https://discord.com/api/oauth2/authorize?client_id=868699834461347880&permissions=8&scope=bot')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await interaction.response.edit_message(embed=embed, view=self)
        elif select.values[0] == "BC":
            embed = discord.Embed(title=":gear: Bot Configuration Commands",
                                  description=f"""
Make sure to include **`{sp}`** as the prefix for each command below.

[**Moderation**](https://google.com "Configure Moderation Commands")
Hover for Info
<:Reply:882064180251877416>`Setmuterole`

[**Settings**](https://google.com "Make this bot suitable in your server")
Hover for Info
<:Reply:882064180251877416>`Setembedcolor`, `Setprefix`
""", color=color, url='https://discord.com/api/oauth2/authorize?client_id=868699834461347880&permissions=8&scope=bot')
            embed.set_footer(text=f"Type {sp}help <command> for more information on a command.")
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='', style=discord.ButtonStyle.grey, emoji="❌")
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        await discord.InteractionMessage.delete(self)

# Verified
@commands.command()
@commands.is_owner()
async def choose(ctx, *, cl=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Choose", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    if cl is None:await ctx.send("You want me to choose something...")
    else:
        c = re.compile('^[\x20-\x7F]*$')
        a = re.sub(f"{c}", " ", cl).split()
        b = random.choice(a)

        if "@everyone" in cl:await ctx.reply(f'I choose **`{b.replace("@everyone", "@Everyone")}`**')
        elif "@here" in cl:await ctx.reply(f'I choose **`{b.replace("@here", "@Here")}`**')
        else:await ctx.reply(f'I choose **`{b}`**')

@commands.command()
@commands.is_owner()
async def war(ctx, member: discord.Member):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("War", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    embed = discord.Embed(color=discord.Color.gold())
    embed.add_field(name=f"{member.name}",value=":blue_circle: :blue_circle: :blue_circle: :blue_circle: :blue_circle: ")
    embed.add_field(name=f"{ctx.author.name}",value=":red_circle: :red_circle: :red_circle: :red_circle: :red_circle: ", inline=True)
    mview =warbuttons(timeout=20)
    out = await ctx.send(embed=embed, view=mview)
    mview.response = out
    mview.user.append(member.id)
    mview.user.append(ctx.author.id)
class warbuttons(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.response = None
        self.user = []
        self.mhealth = 100
        self.uhealth = 100

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.response.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id not in self.user:
            self.au
            await interaction.response.send_message("You are not participating in this fight.", ephemeral=True)
            return False
        else:
            return True
    @discord.ui.button(label="Attack!", emoji="⚔️")
    async def attack(self, button: discord.ui.Button, interaction: discord.Interaction):
        success = random.randint(1,3)
        if success == 1:
            self.mhealth - 100

@commands.command()
@commands.is_owner()
async def tictactoe(ctx, member: discord.Member):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Tictactoe", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)

# Verified
@commands.command()
@commands.is_owner()
async def say(ctx, *, s=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Say", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)

    if s is None:await ctx.send("You want me to say something...")
    else:
        if "@everyone" in s:await ctx.send(f"{s.replace('@everyone', '@Everyone')}")
        elif "@here" in s:await ctx.send(f"{s.replace('@here', '@Here')}")
        else:await ctx.send(f"{s}\n\nSincerely,\n**{ctx.author}**")

@commands.command()
@commands.is_owner()
async def commandlb(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Commandlb", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    k = Counter(db["Total"])
    high, place, thelist = k.most_common(10), 1, []
    for i in high:
        if place == 10:
            thelist.append(f"{place}. {locale.format_string('%d', i[1], grouping=True).ljust(10)}{i[0].ljust(5)}")
        else:
            thelist.append(f"{place}.  {locale.format_string('%d', i[1], grouping=True).ljust(10)}{i[0].ljust(5)}")
        place += 1
    embed= discord.Embed(title="Top 10 Commands", description=f"```md\n#   {'Amount'.ljust(10)}{'Command'.ljust(5)}\n" + "\n".join(a for a in thelist) + "```", color=color)
    embed.set_author(name="The Revolutionary",icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
    embed.set_footer(text="The currency commands on the rise...")
    await ctx.send(embed=embed)

@commands.command()
@commands.is_owner()
async def test2(ctx):
    b = discord.utils.snowflake_time(497903117241810945)
    await ctx.send(f"{discord.utils.format_dt(b)}")
    d = 497903117241810945
    c = ((d >> 22) + 1420070400000)/1000
    await ctx.send(f"<t:{c}>")


@commands.command()
@commands.is_owner()
async def google(ctx, *, query: str):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Google", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    mview = Google(query)
    out = await ctx.send(f"Search for: **`{query}`**", view=mview)
    mview.response = out
class Google(discord.ui.View):
    def __init__(self, query: str):
        super().__init__(timeout=15)
        self.response = None
        query = quote_plus(query)
        url = f'https://www.google.com/search?q={query}'
        self.add_item(discord.ui.Button(label='Search', url=url))

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.response.edit(view=self)

# Semi Finished
@commands.command(aliases=["pollban", "PollBan", "Pollban", "voteban", "Voteban", "VoteBan"])
@commands.is_owner()
async def pban(ctx, member: discord.Member = None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Pban", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    view = pbanbuttons()
    out = await ctx.reply(f"Should we ban **{member}**? (Majority wins)", view=view, mention_author=False)
    view.user = member.id
    view.response = out
class pbanbuttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=10)
        self.response = None
        self.game = []
        self.yes = []
        self.no = []
        self.user = None

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        if len(self.yes) > len(self.no):
            await self.response.edit(f"**TIME'S UP!**\n<@{self.user}> **will be banned!! (`{len(self.yes)}: YES | {len(self.no)}: NO`)**", view=self)
        elif len(self.yes) < len(self.no):
            await self.response.edit(f"**TIME'S UP!**\n<@{self.user}> **will not be banned!! (`{len(self.yes)}: YES | {len(self.no)}: NO`)**\n\nCaring for each other is important :thumbsup:", view=self)
        else:
            await self.response.edit(f"**TIME'S UP!**\n<@{self.user}> **will not be banned!! (`It was a TIE`)**\n\nCaring for each other is important :thumbsup:", view=self)


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id in self.game:
            await interaction.response.send_message("You already voted.", ephemeral=True)
            return False
        else:
            return True

    @discord.ui.button(label='0', style=discord.ButtonStyle.grey, emoji="<:checkmark:865377261896466442>",custom_id="yes")
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        number = int(button.label) if button.label else 0

        button.label = str(number + 1)
        self.game.append(interaction.user.id)
        self.yes.append(interaction.user.id)
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='0', style=discord.ButtonStyle.grey, emoji="<:block:864236511612239873>", custom_id="no")
    async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
        number = int(button.label) if button.label else 0

        button.label = str(number + 1)
        self.game.append(interaction.user.id)
        self.no.append(interaction.user.id)
        await interaction.response.edit_message(view=self)

# Semi Finished
@commands.command(aliases=["Invite", "inv", "Inv", "INV", "INVITE"])
async def invite(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Invite", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    embed = discord.Embed(title="Invite Links!", color=discord.Color.gold())
    embed.set_author(name="The Revolutionary",
                     icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
    await ctx.reply(embed=embed, mention_author=False, view=invitebuttons())
class invitebuttons(discord.ui.View):
    def __init__(self):
        super().__init__()
        url = 'https://discord.com/api/oauth2/authorize?client_id=868699834461347880&permissions=8&scope=bot'
        url2 = 'https://discord.gg/g9NVw9utNk'
        self.add_item(discord.ui.Button(label='Bot Invite', url=url, style=discord.ButtonStyle.url))
        self.add_item(discord.ui.Button(label='Server Invite', url=url2, style=discord.ButtonStyle.url))

# Finished
@commands.command()
@commands.is_owner()
async def nextupdate(ctx):
    embed=discord.Embed(title="v2.2.0 plans", color=color)
    embed.set_author(name="The Revolutionary",
                     icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
    await ctx.reply(embed=embed, mention_author=False, view=updatebuttons())
class updatebuttons(discord.ui.View):
    def __init__(self):
        super().__init__()
        url = 'https://trello.com/b/h4bMZyBV/the-revolutionary-220'
        self.add_item(discord.ui.Button(label='Click Here', url=url, style=discord.ButtonStyle.url))


@commands.command()
@commands.is_owner()
async def hello(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Hello", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    async with ctx.typing():
        await asyncio.sleep(0.5)
    await ctx.reply("Hello")

@commands.command()
@commands.is_owner()
async def emojilist(ctx):
    emoji = [emoji for emoji in ctx.author.guild.emojis]
    final = []
    animated = []
    total = []
    for a in ctx.author.guild.emojis:
        if f"{a}"[1] == "a":
            final.append(f"{a} ─ `{a}`")
        else:
            animated.append(f"{a} ─ `{a}`")
        total.append(f"{a} ─ `{a}`")
    embed=discord.Embed(title=f"Total Emojis: {len(total)}", description=f"**Not Animated Emojis `({len(animated)})`**\n"+"\n".join(b for b in animated), color=color)
    embed.set_author(name=f"{ctx.author.guild}", icon_url=ctx.author.guild.icon)
    embed2 = discord.Embed(description=f"**Animated Emojis `({len(final)})`**\n" + "\n".join(b for b in final), color=color)
    embed2.set_footer(text=f"Total Emojis: {len(total)}")
    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)

@commands.command()
@commands.is_owner()
async def simprate(ctx, member:discord.Member=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Simprate", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    simp = random.randrange(1, 100)
    if member is None:
        await ctx.send(f"{ctx.author.name}'s simprate: **`{str(simp)}%`**")
    else:
        await ctx.send(f"{member.name}'s simprate: **`{str(simp)}%`**")

@commands.command()
@commands.is_owner()
async def iqrate(ctx, member:discord.Member=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("IQrate", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    simp = random.randrange(69, 200)
    if member is None:
        await ctx.send(f"{ctx.author.name}'s iq: **`{str(simp)}`**")
    else:
        await ctx.send(f"{member.name}'s iq: **`{str(simp)}`**")

@commands.command()
@commands.is_owner()
async def luck(ctx, member:discord.Member=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Luck", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    simp = random.randrange(1, 100)
    if member is None:
        if simp == 100:
            await ctx.send(f"{ctx.author.name}'s luck: **`{str(simp)}%`** :four_leaf_clover:")
        else:
            await ctx.send(f"{ctx.author.name}'s luck: **`{str(simp)}%`**")
    else:
        if simp == 100:
            await ctx.send(f"{member.name}'s luck: **`{str(simp)}%`** :four_leaf_clover:")
        else:
            await ctx.send(f"{member.name}'s luck: **`{str(simp)}%`**")

@commands.command()
@commands.is_owner()
async def membercount(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Membercount", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    embed = discord.Embed(description=f"**Total Members:** {ctx.author.guild.member_count}\n**Humans:** {len([m for m in ctx.author.guild.members if not m.bot])}\n**Bots:** {len([m for m in ctx.author.guild.members if m.bot])}", color=discord.Color.from_rgb(47, 49, 54))
    embed.set_author(name=f"{ctx.author.guild.name}", icon_url=ctx.author.guild.icon)
    await ctx.send(embed=embed)

#MODERATION
@commands.command()
@commands.is_owner()
async def dump(ctx, role:discord.Role):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Dump", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    b = []
    for a in role.members:
        b.append(a.mention)
    if role.color == discord.Color.default():
        color = discord.Color.gold()
    else:
        color = role.color
    if role.name == "@everyone":
        name = "Everyone"
    else:
        name = role.name
    embed = discord.Embed(title=f"Users with {name}", color=color)
    embed.add_field(name=f"Users ({len(role.members)})", value="\n".join(c for c in b))
    embed.set_author(name=f"{ctx.author.guild.name}", icon_url=ctx.author.guild.icon)
    await ctx.send(embed=embed)

@commands.command()
@commands.is_owner()
async def taxcalc(ctx, amount):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Taxcalc", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    locale.setlocale(locale.LC_ALL, 'en_US')

    if amount.isnumeric() == False:
        await ctx.send("Must be a number")
    elif amount.isnumeric() == True:
        if int(amount) <= 0:
            await ctx.send("Must be greater than 0...")
        else:
            embed = discord.Embed(title=f"You have to pay {locale.format_string('%d', int(round(int(amount)/0.97)), grouping=True)}", description=f"Amount after tax: **{locale.format_string('%d', int(amount), grouping=True)}**\nAmount lost after tax: **{locale.format_string('%d', int(round(int(amount)/0.97))-int(amount), grouping=True)}**", color=discord.Color.gold())
            embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/270904126974590976/d60c6bd5971f06776ba96497117f7f58.png?size=1024')
            embed.set_footer(text="Tax Rate: 3%")
            embed.set_author(name="The Revolutionary", icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
            await ctx.send(embed=embed)

@commands.command()
@commands.is_owner()
async def emojify(ctx, *,words):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Emojify", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    a = [char for char in words.lower()]
    emoji = ":regional_indicator_"
    string = []
    er = False
    for b in a:
        if b == " ":
            string.append(" ")
        elif b.isnumeric() == True:
            string.append(f":{num2words(b)}:")
        elif b.isalpha() == True:
            string.append(f"{emoji}{b}:")
        else:
            await ctx.send(f"'{b}' cannot be emojified.")
            er = True
            return
    if er == False:
        await ctx.send("".join(c for c in string))

@commands.command()
@commands.is_owner()
async def num2word(ctx, *, num2word):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Num2Word", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)
    dc = num2word.split()
    string = []
    for b in dc:
        if b.isnumeric() == True:
            string.append(num2words(int(b)))
        elif "@everyone" == b:
            string.append("@Everyone")
        elif "@here" == b:
            string.append("@Here")
        else:
            string.append(b)
    await ctx.send(" ".join(string))

@commands.command()
@commands.is_owner()
async def tstart(ctx, time, *, reward):
    last = time[-1]

    multi = 1
    suffix = ""

    if last == "s":
        multi = 1
        if int(time[:-1]) > 1:
            suffix = "seconds"
        else:
            suffix = "minute"
    elif last == "m":
        multi = 60
        if int(time[:-1]) > 1:
            suffix = "minutes"
        else:
            suffix = "minute"
    elif last == "h":
        multi = 3600
        if int(time[:-1]) > 1:
            suffix = "hours"
        else:
            suffix = "hour"

    time2 = int(time[:-1]) * multi
    mins, secs = divmod(time2, 60)
    h, mins = divmod(mins, 60)
    future = datetime.now() + timedelta(seconds=time2)

    real = datetime.now() - timedelta(hours=12)
    a = real + timedelta(minutes=mins, seconds=secs, hours=h)

    if datetime.now().hour >= 12:
        pmam = "PM"
    else:
        pmam = "AM"

    await ctx.channel.purge(limit=1)
    msg = await ctx.send("**:timer: TIMER :timer:**")
    while datetime.now().strftime('%H:%M:%S') < future.strftime('%H:%M:%S'):
        mins, secs = divmod(time2, 60)
        h, mins = divmod(mins, 60)

        new_embed1 = discord.Embed(title=f'{reward}',description=f"Time: **{time[:-1]} {suffix}** (ends {discord.utils.format_dt(discord.utils.snowflake_time(msg.id)+timedelta(seconds=time2), style='R')})\nStarted by: **{ctx.author} | {ctx.author.mention}**",color=discord.Color.gold())
        new_embed1.set_author(name="Timer",icon_url="https://cdn.discordapp.com/attachments/690681407256789012/865432946068422656/c9c0406416e18421fc203dd3c8a2dba7.png")
        new_embed1.set_footer(text=f"Ends at {a.strftime(f'%H:%M {pmam}')}")
        await msg.edit(embed=new_embed1)
        await asyncio.sleep(int(time2)/2)
    new_embed3 = discord.Embed(title=f'{reward}',description=f"Started by: **{ctx.author} | {ctx.author.mention}**",color=discord.Color.from_rgb(47, 49, 54))
    new_embed3.set_author(name="Timer has ended",icon_url="https://cdn.discordapp.com/attachments/690681407256789012/865432946068422656/c9c0406416e18421fc203dd3c8a2dba7.png")
    new_embed3.set_footer(text=f"Ended on {a.strftime(f'%H:%M {pmam}')}")
    await msg.edit(embed=new_embed3)
    await msg.reply(content=f"Timer has ended for **{reward}**!\nhttps://discord.com/channels/{ctx.author.guild.id}/{ctx.channel.id}/{msg.id}")

#V 2.0.0

@commands.command()
@commands.is_owner()
async def afk(ctx):
    pass

@commands.command()
@commands.is_owner()
async def mutualg(ctx, member:discord.Member):
    thelist = []

    # MUTUAL GUILDS
    for a in member.mutual_guilds: thelist.append(f"(`{a.id}`) ─ **{a}**")

    word = "\n".join(b for b in thelist)

    if len(word) == 0:
        word = "None"
    else:
        word = "\n".join(b for b in thelist)

    if member.avatar == None:
        micon = member.default_avatar
    else:
        micon = member.avatar.url

    embed = discord.Embed(title=f"{member.name}'s Mutual Servers With You", description=f"{word}", colour=ctx.author.color)
    embed.set_author(name=f"{ctx.author}", icon_url='https://cdn.discordapp.com/emojis/895068536223985664.png?size=32')
    await ctx.reply(embed=embed, mention_author=False)

@commands.command()
@commands.is_owner()
async def banner(ctx, member:discord.Member=None):
    if member is None:
        if ctx.author.banner == None: bicon = True
        else:bicon = ctx.author.banner

        if ctx.author.avatar == None:micon = ctx.author.default_avatar
        else:micon = ctx.author.avatar

        if bicon == True:
            embed = discord.Embed(title="User Banner", description="User has no banner", colour=ctx.author.color)
            embed.set_author(name=f"{ctx.author}", icon_url='https://cdn.discordapp.com/emojis/895068536223985664.png?size=32')
        else:
            embed = discord.Embed(title="User Banner",colour=ctx.author.color)
            embed.set_image(url=bicon)
            embed.set_author(name=f"{ctx.author}", icon_url='https://cdn.discordapp.com/emojis/895068536223985664.png?size=32')
        await ctx.reply(embed=embed, mention_author=False)
    else:
        if member.banner == None: bicon = True
        else:bicon = member.banner

        if member.avatar == None:micon = member.default_avatar
        else:micon = member.avatar

        if bicon == True:
            embed = discord.Embed(title="User Banner", description="User has no banner", colour=member.color)
            embed.set_author(name=f"{member}", icon_url='https://cdn.discordapp.com/emojis/895068536223985664.png?size=32')
        else:
            embed = discord.Embed(title="User Banner",colour=member.color)
            embed.set_image(url=bicon)
            embed.set_author(name=f"{member}", icon_url='https://cdn.discordapp.com/emojis/895068536223985664.png?size=32')
        await ctx.reply(embed=embed, mention_author=False)

@commands.command()
@commands.is_owner()
async def easy2read(ctx, arg):
    if "```" in arg: await ctx.send(f"` {arg}   <-- Copy if needed!`")
    else: await ctx.reply(f"``` {arg}   <-- Copy if needed!```", mention_author=False)

@commands.command()
@commands.is_owner()
async def gavatar(ctx, member:discord.User):
    if member.avatar == None: micon = member.default_avatar
    else:micon = member.avatar

    embed = discord.Embed(title="Avatar", colour=member.color)
    embed.set_image(url=micon)
    embed.set_author(name=f"{member}", icon_url='https://cdn.discordapp.com/emojis/895068536223985664.png?size=32')
    await ctx.reply(embed=embed, mention_author=False)

@commands.command()
@commands.is_owner()
async def _(ctx):
    await ctx.send("_ (`You found a secret command!`)")

@commands.command()
@commands.is_owner()
async def updatee(ctx):
    embed = discord.Embed(title="**Version 2.2.0 Patch Notes!**", description="""
These notes only cover the most important updates, we did many small changes to almost every existing command. We might've forgot to put an important update on here. This update mainly focused on currency commands and formatting.

> **LEAGUES! <:leaguetrophy:891844638380556319>**
> <:Reply:882064180251877416> Trophy ratings, check `r!leagues` for more info
>
> **Gamble and Slot Machine! :moneybag:**
> <:Reply:882064180251877416> Gamble your money with two new gambling commands!
>
> **New command: `r!profile`**, check user/your balance, league/trophy, fish net, and most prized catch
>
> **You can now shop for items! :shopping_cart: :shopping_bags: `r!shop`**
> <:ReplyContinue:882064049850961981> 4 New First Items listed in the shop
> <:Reply:882064180251877416> Buy/Sell/Use Items! `r!buy`|`r!sell`|`r!use`!
>
> **3 New fish!! 👀 `r!fish`** to try to get the **__three__** new fish :fish:!
> <:ReplyContinue:882064049850961981> There is now also a chance to get nothing!
> <:ReplyContinue:882064049850961981> Lobster downgraded one rarity :chart_with_downwards_trend:
> <:Reply:882064180251877416> You can now sell fish! The fish you catch counts as your fish net
>
> **2 New Stocks!! 👀 `r!stocks`**
> <:ReplyContinue:882064049850961981> Stock custom BUY button! (only for one tho)
> <:Reply:882064180251877416> Formatting changed dramatically! Much more aesthetically pleasing
>
> **New item: Worms :worm:!** They increase your luck in fishing. Can be bought in the shop.
>
> **`r!help` much much MUCH more user-friendly :boy:**, this update's purpose was to be more appealing towards new users
> <:Reply:882064180251877416> Finished the individual sub-commands
>
> **20 New Commands** Check them out!

**Tell us how we did! `r!feedback`**
""", color=color)
    embed.set_footer(text="The Revolutionary Staff",
                     icon_url='https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024')
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024')
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)

#V 2.5.0

@commands.command()
@commands.is_owner()
async def meme(ctx):
    reddit = praw.Reddit(client_id='Pb0283EFt8VAug',
                         client_secret='zsWBP1S1tPJKU__3Xut0s-nYSWuSSA',
                         user_agent='meme-collector')

    memes_submissions = reddit.subreddit('memes').hot(limit=200)
    post_to_pick = random.randint(1, 10)
    submission=None
    for i in range(0, post_to_pick):submission = next(x for x in memes_submissions if not x.stickied)

    embed = discord.Embed(title="Meme Compliation", color=color)
    embed.set_image(url=submission.url)

    #embed.set_footer(text=f"👍 {thumbsup} | 💬 {comments} | r/memes")
    await ctx.send(embed=embed)

def setup(bot):
    bot.add_command(meme)
    bot.add_command(updatee)
    bot.add_command(_)
    bot.add_command(afk)
    bot.add_command(mutualg)
    bot.add_command(banner)
    bot.add_command(easy2read)
    bot.add_command(guserinfo)
    bot.add_command(luck)
    bot.add_command(iqrate)
    bot.add_command(commandlb)
    bot.add_command(tstart)
    bot.add_command(num2word)
    bot.add_command(emojify)
    bot.add_command(taxcalc)
    bot.add_command(dump)
    bot.add_command(membercount)
    bot.add_command(simprate)
    bot.add_command(emojilist)
    bot.add_command(hello)
    bot.add_command(test2)
    bot.add_command(snowflake)
    bot.add_command(channels)
    bot.add_command(allroles)
    bot.add_command(help)
    bot.add_command(google)
    bot.add_command(say)
    bot.add_command(choose)
    bot.add_command(avatar)
    bot.add_command(userinfo)
    bot.add_command(nextupdate)
    bot.add_command(bon)
    bot.add_command(pat)
    bot.add_command(pban)
    bot.add_command(invite)
    bot.add_command(date)
    bot.add_command(war)
    bot.add_command(gavatar)
