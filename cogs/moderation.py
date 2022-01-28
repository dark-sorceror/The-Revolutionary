import discord
import time
import asyncio
import random
import json
import re
import sys
import locale
import typing
import pymongo
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus
from pathlib import Path
from num2words import num2words

import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot

from variables import (
    color,
    cu,
    determine_prefix,
    bot
)

membed=discord.Embed(
    description="```yaml\nSyntax: r!ban <user> [days] [reason]```\nBan a user from this server and optionally delete days of messages.\n`[days]` is the amoutn of days of messages to cleanup on ban.", color=discord.Color.red())
membed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
membed.add_field(
    name="Examples",
    value="<:replystart:895447277622161469> `r!ban 567487802900480000 7 Rude to other members`\n<:ReplyContinue:882064049850961981> `r!ban` <@567487802900480000> `2 Making rumours`\n<:Reply:882064180251877416> `r!ban Fantom#1258 7 Starting drama`")
membed.add_field(name="**Permissions**",value="`USER` ─ `Administrator` | `Ban Members`\n`BOT` ─ `Ban Members`")

kembed=discord.Embed(
    description="```yaml\nSyntax: r!kick <user> [reason]```\nKick a user from this server", color=discord.Color.red())
kembed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
kembed.add_field(
    name="Examples",
    value="<:replystart:895447277622161469> `r!kick 567487802900480000 Rude to other members`\n<:ReplyContinue:882064049850961981> `r!kick` <@567487802900480000> `Making rumours`\n<:Reply:882064180251877416> `r!kick Fantom#1258 Starting drama`")
kembed.add_field(name="**Permissions**",value="`USER` ─ `Administrator` | `Kick Members`\n`BOT` ─ `Kick Members`")

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
        await ctx.reply(embed=membed, mention_author=False)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(content="```yaml\nr!ban <user> [days] [reason]\n    ^^^^\n<user> is a required argument that is missing.```",embed=membed, mention_author=False)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="Your missing `BAN_MEMBERS` permission", color=discord.Color.red())
        embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description="Bot is missing `BAN_MEMBERS` permission", color=discord.Color.red())
        embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
        await ctx.reply(embed=embed, mention_author=False)

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
        await ctx.reply(embed=kembed, mention_author=False)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(
            content="```yaml\nr!kick <user> [reason]\n    ^^^^\n<user> is a required argument that is missing.```",
            embed=kembed, mention_author=False)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="Your missing `KICK_MEMBERS` permission", color=discord.Color.red())
        embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(description="Bot is missing `KICK_MEMBERS` permission", color=discord.Color.red())
        embed.set_author(name='Error', icon_url='https://cdn.discordapp.com/emojis/895068499175682098.png?size=32')
        await ctx.reply(embed=embed, mention_author=False)

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
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None: theprefix = default_prefix
        else: theprefix = prefix[str(ctx.author.guild.id)]["Prefix"]
    else: theprefix = default_prefix
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
            theprefix = default_prefix
        else:
            theprefix = prefix[str(ctx.author.guild.id)]["Prefix"]
    else:
        theprefix = default_prefix
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
