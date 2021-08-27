import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
import time
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
import pymongo
# import fuzzywuzzy (NEXT UPDATE)

"""
THE REVOLUTIONARY BOT

A reliable utility bot for your every use. Try sending r!help to see what I can do!

AVATAR: https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024
"""

cwd = str(Path(__file__).parents[0])
default = "+"
efile = 'C:/Users/Hao/PycharmProjects/master/error logs'
color = discord.Color.gold()

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
    online, idle, offline, dnd, streaming, mobile = 0, 0, 0, 0, 0, 0
    for m in guild.members:
        if m.status is discord.Status.online:
            if m.is_on_mobile(): mobile += 1
            elif m.activity is not None and m.activity.type is discord.ActivityType.streaming: streaming += 1
            else: online += 1
        elif m.status is discord.Status.offline: offline += 1
        elif m.status is discord.Status.dnd: dnd += 1
        elif m.status is discord.Status.idle: idle += 1
    return online, idle, offline, dnd, streaming, mobile

async def cu(command, db):
    db["Total"][f"{command}"] += 1
    db["Daily"][f"{command}"] += 1
async def ctm(guild_id, db): db[str(guild_id)]["Total Messages"] += 1
async def ctc(guild_id, db): db[str(guild_id)]["Total Commands"] += 1
async def cs(guild_id, db, prefix): db[str(guild_id)]["Prefix"] = prefix
async def ci(guild_id, db, invite): db[str(guild_id)]["Invite"] = f"{invite}"
async def cmr(guild_id, db, role_id): db[str(guild_id)]["Mute Role"] = role_id
async def determine_prefix(bot, message):
    with open('serverdb.json', "r") as f: prefix = json.load(f)
    if str(message.guild.id) in prefix:
        if prefix[str(message.guild.id)]["Prefix"] is None: return default
        else: return prefix[str(message.guild.id)]["Prefix"]
    else: return default
async def udb(guild_id, db):
    if not str(guild_id) in db: db[str(guild_id)], db[str(guild_id)]["Prefix"], db[str(guild_id)]["Invite"], db[str(guild_id)]["Mute Role"],db[str(guild_id)]["Total Messages"], db[str(guild_id)]["Total Commands"] = {}, None, None, None, 0, 0
    else: return

bot = Bot(command_prefix=determine_prefix, intents=discord.Intents().all(), owner_ids=[497903117241810945, 567487802900480000,707697817082265620])
bot.remove_command('help')

#UP TO DATE
@bot.command(aliases=["Uptime", "UPTIME"])
@commands.is_owner()
async def uptime(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Uptime", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)

    uptime = datetime.utcnow() - start_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(color=color)
    embed.set_author(name="The Revolutionary", icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
    embed.add_field(name="Uptime", value=f"{days}d, {hours}h and {minutes}m")
    await ctx.reply(embed=embed, mention_author=False)

#UP TO DATE
@bot.command(aliases=["Setmuterole", "SetMuteRole","setMuteRole","SETMUTEROLE"])
@commands.is_owner()
async def setmuterole(ctx, role:typing.Union[discord.Role, str]=None):
    with open('serverdb.json', "r") as f: prefix = json.load(f)

    if str(ctx.author.guild.id) in prefix:
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None: theprefix = default
        else: theprefix = prefix[str(ctx.author.guild.id)]["Prefix"]
    else: theprefix = default

    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Setmuterole", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4)

    if role is None:
        if str(ctx.author.guild.id) in prefix:
            if prefix[str(ctx.author.guild.id)]["Mute Role"] is None: therole = "None"
            else: therole = prefix[str(ctx.author.guild.id)]["Mute Role"]
        else: therole = "None"

        if therole == "None": embed = discord.Embed(description="The current mute role is not set.", color=color)
        else: embed = discord.Embed( description=f"The current mute role is <@&{therole}>.\nTo remove it, type **`{theprefix}setmuterole none`**", color=color)
    else:
        if role == "none" or role == "None" or role == "NONE":
            if str(ctx.author.guild.id) not in prefix:
                await udb(str(ctx.author.guild.id), prefix)
                with open('serverdb.json', 'w') as f: json.dump(prefix, f, indent=4)
            if prefix[str(ctx.author.guild.id)]['Mute Role'] is None: embed = discord.Embed(description="The current mute role is not set.", color=color)
            else:
                embed = discord.Embed(description=f"Current mute role <@&{prefix[str(ctx.author.guild.id)]['Mute Role']}> is removed.",color=color)
                await cmr(str(ctx.author.guild.id), prefix, role_id=None)
                with open('serverdb.json', 'w') as f: json.dump(prefix, f, indent=4)
        else:
            if str(ctx.author.guild.id) not in prefix:
                await udb(str(ctx.author.guild.id), prefix)
                with open('serverdb.json', 'w') as f: json.dump(prefix, f, indent=4)
            await cmr(str(ctx.author.guild.id), prefix, role_id=role.id)
            with open('serverdb.json', 'w') as f: json.dump(prefix, f, indent=4)
            embed = discord.Embed(description=f"The current mute role is set to <@&{role.id}>.",color=color)
    await ctx.send(embed=embed)

#UP TO DATE
@bot.command(aliases=["Version", "VERSION", "Versioninfo", "VersionInfo", "versioninfo","VERSIONINFO"])
@commands.is_owner()
async def version(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Version", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)

    embed = discord.Embed(color=color)
    embed.set_author(name="The Revolutionary",icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
    embed.add_field(name="Bot Version", value="<:python:876219458522349569> [`3.8.1`](https://www.python.org/)\n<:discordpy:876219426469478411> [`1.7.3`](https://github.com/Rapptz/discord.py)\n<:therevolutionary:865728876546097174> [`2.0.0 (Master)`](https://google.com)")
    await ctx.reply(embed=embed, mention_author=False)

#UP TO DATE
@bot.command(aliases=["Guess", "GUESS"])
@commands.is_owner()
async def guess(ctx, lr=None, hr=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Guess", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4, sort_keys=True)

    if lr is None and hr is None: lr, hr = 1, 20
    alr, ahr = lr, hr
    if lr > hr: lr, hr = ahr, alr
    message = await ctx.reply(f"Thinking of a number between **`{lr}`** and **`{hr}`**...")
    time.sleep(2)
    number = random.randint(int(lr), int(hr))
    await message.edit(f"OK, I have found a number between **`{lr}`** and **`{hr}`**. Type your guess down below. To end the game, type **`end`**.")

    tries = 3
    while tries != 0:
        def check(m: discord.Message): return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        try: msg = await bot.wait_for(event='message', check=check, timeout=10)
        except asyncio.TimeoutError:
            await ctx.send(f"**Times Up!** The number was **`{number}`**")
            return
        else:
            if str(msg.content.lower()) == "end":
                await ctx.send("You ended the game. Sad.")
                return
            else:
                if int(msg.content) == number:
                    await ctx.send(f"You found my number! It was **`{number}`**!!")
                    return
                else:
                    tries = tries - 1
                    if tries == 0:
                        await ctx.send(f"Rip, you ran out of attempts to guess the number. I was thinking of the number, **`{number}`**")
                        return
                    else:
                        if tries == 1: await ctx.send(f"**`{msg.content}`** is not the number. **{tries}** try left.")
                        else: await ctx.send(f"**`{msg.content}`** is not the number. **{tries}** tries left.")

#UP TO DATE
@bot.command(aliases=["Setprefix","setPrefix","SetPrefix","trprefix","TRPrefix","Trprefix","SETPREFIX"])
@commands.is_owner()
async def setprefix(ctx, arg=None):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Setprefix", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4)
    with open('serverdb.json', "r") as f: prefix = json.load(f)

    if str(ctx.author.guild.id) in prefix:
        if prefix[str(ctx.author.guild.id)]["Prefix"] is None: theprefix = default
        else: theprefix = prefix[str(ctx.author.guild.id)]["Prefix"]
    else: theprefix = default

    if arg is None: embed = discord.Embed(description=f"The current server prefix is: **`{theprefix}`**. \nTo change it, type **`{theprefix}setprefix [Prefix of your choosing]`**", color=color)
    else:
        with open('serverdb.json', 'w') as f:
            if str(ctx.author.guild.id) not in prefix: await udb(str(ctx.author.guild.id), prefix)
            await cs(str(ctx.author.guild.id), prefix, prefix=arg)
            json.dump(prefix, f, indent=4)
            embed = discord.Embed(description=f"Server prefix set to: **`{arg}`**",color=color)
    await ctx.send(embed=embed)

#UP TO DATE
@bot.command(aliases=["Ping", "PING","latency","Latency","LATENCY"])
@commands.is_owner()
async def ping(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Ping", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4)

    start_time = time.time()
    message = await ctx.reply("Loading...", mention_author=True)
    end_time = time.time()
    embed = discord.Embed(title=f"Pong!",description=f"Bot Latency: **{round(bot.latency * 1000)}ms**\nAPI Latency: **{round((end_time - start_time) * 1000)}ms**",color=color)
    embed.set_author(name="The Revolutionary",icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
    await message.edit(content=None, embed=embed)

#UP TO DATE
@bot.command(aliases=["SI", "si", "Si", "SERVERINFO", "Serverinfo"])
@commands.is_owner()
async def serverinfo(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        await cu("Serverinfo", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4)
    with open('serverdb.json', 'r') as f: sdb = json.load(f)

    guild = bot.get_guild(ctx.author.guild.id)
    ae, ar = len(list(guild.emojis)), len(list(guild.roles)) #AMOUNT OF ROLES
    real = guild.created_at - timedelta(hours=12) #12 HOUR CLOCK
    online, idle, offline, dnd, streaming, mobile = community_report(ctx) #STATUS
    link = await ctx.channel.create_invite(max_age=300) #INVITE LINK
    # cfm = real.__format__("%B")[0:3] V2.0.0 REMOVED

    if str(ctx.author.guild.id) in sdb:
        if sdb[str(ctx.author.guild.id)]["Invite"] is None:
            await ci(str(ctx.author.guild.id), sdb, invite=link)
            with open('serverdb.json', 'w') as f: json.dump(sdb, f, indent=4)
    else:
        await udb(str(ctx.author.guild.id), sdb)
        await ci(str(ctx.author.guild.id), sdb, invite=link)
        with open('serverdb.json', 'w') as f: json.dump(sdb, f, indent=4)

    #DATABASE VARIABLES
    thelink, tm, tc = sdb[str(ctx.author.guild.id)]["Invite"],sdb[str(ctx.author.guild.id)]["Total Messages"],sdb[str(ctx.author.guild.id)]["Total Commands"]

    #FORMATTING
    if int(real.__format__("%d")) >= 10 and int(real.__format__("%d")) <= 20: snt = "th"
    else:
        if int(real.__format__("%d")[-1]) == 1:snt = "st"
        elif int(real.__format__("%d")[-1]) == 2:snt = "nd"
        elif int(real.__format__("%d")[-1]) == 3:snt = "rd"
        else:snt = "th"
    if int(real.__format__("%d")[0]) == 0:rd = int(real.__format__("%d")[1])
    else:rd = int(real.__format__("%d"))
    if not guild.icon: guildicon = 'https://cdn.discordapp.com/attachments/865342805107015722/871546487220359229/dd4dbc0016779df1378e7812eabaa04d.png'
    else: guildicon = guild.icon
    vc_regions = {
"eu-west": "EU West " + "\U0001F1EA\U0001F1FA",
"eu-central": "EU Central " + "\U0001F1EA\U0001F1FA",
"europe": "Europe " + "\U0001F1EA\U0001F1FA",
"london": "London " + "\U0001F1EC\U0001F1E7",
"frankfurt": "Frankfurt " + "\U0001F1E9\U0001F1EA",
"amsterdam": "Amsterdam " + "\U0001F1F3\U0001F1F1",
"us-west": "US West " + "\U0001F1FA\U0001F1F8",
"us-east": "US East " + "\U0001F1FA\U0001F1F8",
"us-south": "US South " + "\U0001F1FA\U0001F1F8",
"us-central": "US Central " + "\U0001F1FA\U0001F1F8",
"singapore": "Singapore " + "\U0001F1F8\U0001F1EC",
"sydney": "Sydney " + "\U0001F1E6\U0001F1FA",
"brazil": "Brazil " + "\U0001F1E7\U0001F1F7",
"hongkong": "Hong Kong " + "\U0001F1ED\U0001F1F0",
"russia": "Russia " + "\U0001F1F7\U0001F1FA",
"japan": "Japan " + "\U0001F1EF\U0001F1F5",
"southafrica": "South Africa " + "\U0001F1FF\U0001F1E6",
"india": "India " + "\U0001F1EE\U0001F1F3",
"dubai": "Dubai " + "\U0001F1E6\U0001F1EA",
"south-korea": "South Korea " + "\U0001f1f0\U0001f1f7"}

    #EMBED
    if guild.description == None: embed = discord.Embed(title='Server Information',description=f'**Owner:** {guild.owner} | {guild.owner.mention}\n**Region:** {vc_regions.get(str(guild.region))}\n**Creation:** {discord.utils.format_dt(discord.utils.snowflake_time(ctx.author.guild.id), style="D")} ({discord.utils.format_dt(discord.utils.snowflake_time(ctx.author.guild.id), style="R")})',color=discord.Color.from_rgb(47, 49, 54))
    else:embed = discord.Embed(title='Server Information',description=f'{guild.description}\n\n**Owner:** {guild.owner.mention}\n**Region:** {vc_regions.get(str(guild.region))}\n**Creation:** {discord.utils.format_dt(discord.utils.snowflake_time(ctx.author.guild.id), style="D")} ({discord.utils.format_dt(discord.utils.snowflake_time(ctx.author.guild.id), style="R")})',color=discord.Color.from_rgb(47, 49, 54))
    embed.set_thumbnail(url=f"{guildicon}")
    embed.set_author(name=f"{guild.name}", icon_url=f"{guildicon}", url=thelink)
    embed.add_field(name="Stats",value=f"**Total Members:** {guild.member_count}\n**Bots:** {len([m for m in guild.members if m.bot])}\n**Emotes:** {ae}\n**Roles:** {ar}")
    embed.add_field(name='Server Stats', value=f"**Total Messages:** {tm}\n**Total Commands:** {tc}")
    embed.add_field(name="Member Stats",value=f"<:online:870758878416105523> **Online:** {online}\n<:idle:870758669325860896> **Idle:** {idle}\n<:dnd:870758632306913360> **Dnd:** {dnd}\n<:offline:870758702360191007> **Offline:** {offline}\n<:streaming:870758731674157118> **Streaming:** {streaming}\n<:mobile:868253746155646976> **Mobile:** {mobile}")
    embed.set_footer(text=f"ID: {guild.id}")
    await ctx.reply(embed=embed, mention_author=False)

#UP TO DATE
@bot.command(aliases=["Botinfo", "binfo", "BInfo", "BOTINFO","Binfo"])
@commands.is_owner()
async def botinfo(ctx):
    with open('commandusage.json', "r") as f:
        db = json.load(f)
        a, b = db["Total"].values(), db["Daily"].values()
        amount, amount2 = sum(a), sum(b)
        await cu("Botinfo", db)
        with open('commandusage.json', "w") as f: json.dump(db, f, indent=4)
    with open('serverdb.json', 'r') as f: sdb = json.load(f)

    if str(ctx.author.guild.id) in sdb:
        if sdb[str(ctx.author.guild.id)]["Prefix"] is None: theprefix = default
        else: theprefix = sdb[str(ctx.author.guild.id)]["Prefix"]
    else: theprefix = default

    #memberCount = len(set(bot.get_all_members()))
    uptime = datetime.utcnow() - start_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    embed = discord.Embed(description="A reliable utility bot for your every use. Try sending `r!help` to see what I can do!",color=color)
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024')
    embed.set_author(name="The Revolutionary",icon_url="https://cdn.discordapp.com/avatars/862823231161630740/c9c0406416e18421fc203dd3c8a2dba7.webp?size=1024")
    embed.add_field(name="Owner", value="sheesh#0034 | <@497903117241810945>", inline=True)
    embed.add_field(name="Versions", value="<:python:876219458522349569> [`3.8.1`](https://www.python.org/)\n<:discordpy:876219426469478411> [`1.7.3`](https://github.com/Rapptz/discord.py)\n<:therevolutionary:865728876546097174> [`2.1.0 (Master)`](https://google.com)", inline=True)
    embed.add_field(name="Bot Stats",value=f"Total Commands Used: **{amount}**\nCommands Used Today: **{amount2}**\nMost Used Command Today: **`{theprefix}{max(db['Daily'], key=db['Daily'].get)}`**", inline=False)
    embed.add_field(name="Links",value="[Invite Me](https://discord.com/api/oauth2/authorize?client_id=862823231161630740&permissions=8&scope=bot%20applications.commands)  |  [Support Server](https://discord.gg/g9NVw9utNk)",inline=True)
    embed.set_footer(text=f"Uptime: {days}d, {hours}h and {minutes}m")
    await ctx.reply(embed=embed)

#ADMIN

#PENDING
@bot.command(aliases=["Lock", "lock", "LOCK", "shutdown", "Shutdown"])
@commands.is_owner()
async def lockdown(ctx):
    view = lockdownbuttons()
    await ctx.reply("```diff\n- Are you sure? Please interact below```", view=view, mention_author=False)
    await view.wait()
    if view.value:
        time.sleep(5)
        await ctx.send("```fix\nHold on... This might take a few seconds```")
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Shutting down..."))
        time.sleep(30)
        data = read_json("status")
        data["Bot Working"] = False

        try:
            bot.unload_extension('admincommands')
            data["Admin Cog"] = False
            data["Admin Cog Error"] = False
            await ctx.send("```diff\n+ Unloaded admincommands.py cog```")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data["Admin Cog"] = False
            data["Admin Cog Error"] = True
            await ctx.send(f'```css\nAn error logs occurred when unloading admincommands.py cog:\n[{error}]```')

        time.sleep(5)

        try:
            bot.unload_extension('misc')
            data["Misc Cog"] = False
            data["Misc Cog Error"] = False
            await ctx.send("```diff\n+ Unloaded misc.py cog```")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data["Misc Cog"] = False
            data["Misc Cog Error"] = True
            await ctx.send(f'```css\nAn error logs occurred when unloading misc.py cog:\n[{error}]```')

        time.sleep(5)

        try:
            bot.unload_extension('moderation')
            data["Moderation Cog"] = False
            data["Moderation Cog Error"] = False
            await ctx.send("```diff\n+ Unloaded moderation.py cog```")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data["Moderation Cog"] = False
            data["Moderation Cog Error"] = True
            await ctx.send(f'```css\nAn error logs occurred when unloading moderation.py cog:\n[{error}]```')

        time.sleep(5)

        try:
            bot.unload_extension('currency')
            data["Currency Cog"] = False
            data["Currency Cog Error"] = False
            await ctx.send("```diff\n+ Unloaded currency.py cog```")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data["Currency Cog"] = False
            data["Currency Cog Error"] = True
            await ctx.send(f'```css\nAn error logs occurred when unloading currency.py cog:\n[{error}]```')

        await ctx.send("```diff\n+ Unloaded commandusage.json...```")
        time.sleep(1)
        await ctx.send("```diff\n+ Unloaded daily.json...```")
        time.sleep(1)
        await ctx.send("```diff\n+ Unloaded serverdb.json...```")
        time.sleep(1)
        await ctx.send("```diff\n+ Unloaded status.json...```")
        time.sleep(1)
        await ctx.send("```diff\n+ Unloaded stocks.json...```")
        time.sleep(5)
        await ctx.send("```diff\n+ Unloaded mongodb://localhost:27017/...```")
        time.sleep(10)
        bot.remove_command('setprefix')
        bot.remove_command('ping')
        bot.remove_command('serverinfo')
        bot.remove_command('botinfo')
        bot.remove_command('guess')
        bot.remove_command('version')
        bot.remove_command('uptime')
        bot.remove_command('setmuterole')
        await bot.change_presence(status=discord.Status.offline)
        time.sleep(15)
        write_json(data, "status")
        await ctx.send("```Bot is inactive```")
class lockdownbuttons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.grey, emoji="<:checkmark:865377261896466442>")
    async def yes(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = True
        await interaction.response.edit_message(content='```Confirming...```', view=None)
        self.stop()

    @discord.ui.button(label='No', style=discord.ButtonStyle.grey, emoji="<:block:864236511612239873>")
    async def no(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.value = False
        await interaction.response.edit_message(content='```Cancelled```', view=None)
        self.stop()

@bot.command()
@commands.is_owner()
async def run(ctx):
    time.sleep(5)
    await ctx.send("```fix\nHold on... This might take a few seconds```")
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Starting Up..."))
    time.sleep(30)
    data = read_json("status")
    data["Bot Working"] = True

    try:
        bot.load_extension('admincommands')
        data["Admin Cog"] = True
        data["Admin Cog Error"] = False
        await ctx.send("```diff\n+ Loaded admincommands.py cog```")
    except Exception as error:
        file = open(efile, "a")
        file.write(f"{str(error)} - {ctx.author.id}")
        file.write("\n")
        file.close()
        data["Admin Cog"] = False
        data["Admin Cog Error"] = True
        await ctx.send(f'```css\nAn error occurred when loading admincommands.py cog:\n[{error}]```')

    time.sleep(5)

    try:
        bot.load_extension('misc')
        data["Misc Cog"] = True
        data["Misc Cog Error"] = False
        await ctx.send("```diff\n+ Loaded misc.py cog```")
    except Exception as error:
        file = open(efile, "a")
        file.write(f"{str(error)} - {ctx.author.id}")
        file.write("\n")
        file.close()
        data["Misc Cog"] = False
        data["Misc Cog Error"] = True
        await ctx.send(f'```css\nAn error occurred when loading misc.py cog:\n[{error}]```')

    time.sleep(5)

    try:
        bot.load_extension('moderation')
        data["Moderation Cog"] = True
        data["Moderation Cog Error"] = False
        await ctx.send("```diff\n+ Loaded moderation.py cog```")
    except Exception as error:
        file = open(efile, "a")
        file.write(f"{str(error)} - {ctx.author.id}")
        file.write("\n")
        file.close()
        data["Moderation Cog"] = False
        data["Moderation Cog Error"] = True
        await ctx.send(f'```css\nAn error occurred when loading moderation.py cog:\n[{error}]```')

    time.sleep(5)

    try:
        bot.load_extension('currency')
        data["Currency Cog"] = True
        data["Currency Cog Error"] = False
        await ctx.send("```diff\n+ Loaded currency.py cog```")
    except Exception as error:
        file = open(efile, "a")
        file.write(f"{str(error)} - {ctx.author.id}")
        file.write("\n")
        file.close()
        data["Currency Cog"] = False
        data["Currency Cog Error"] = True
        await ctx.send(f'```css\nAn error occurred when loading currency.py cog:\n[{error}]```')

    await ctx.send("```diff\n+ Loaded commandusage.json...```")
    time.sleep(1)
    await ctx.send("```diff\n+ Loaded daily.json...```")
    time.sleep(1)
    await ctx.send("```diff\n+ Loaded serverdb.json...```")
    time.sleep(1)
    await ctx.send("```diff\n+ Loaded status.json...```")
    time.sleep(1)
    await ctx.send("```diff\n+ Loaded stocks.json...```")
    time.sleep(5)
    await ctx.send("```diff\n+ Loaded mongodb://localhost:27017/...```")
    time.sleep(10)
    bot.add_command(setprefix)
    bot.add_command(ping)
    bot.add_command(serverinfo)
    bot.add_command(botinfo)
    bot.add_command(guess)
    bot.add_command(version)
    bot.add_command(uptime)
    bot.add_command(setmuterole)
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name="r!help", type=2))
    time.sleep(15)
    write_json(data, "status")
    await ctx.send("```Bot is active```")

#PENDING
@bot.command(aliases=["Load", "LOAD"])
@commands.is_owner()
async def load(ctx, arg):
    message = await ctx.reply("```fix\nHold on... This might take a few seconds```", mention_author=True)
    if arg == "admincommands" or arg == "AdminCommands" or arg == "ac" or arg == "AC" or arg == "admin" or arg == "Admin" or arg == "ADMIN" or arg == "adminc" or arg == "Adminc":
        time.sleep(1)
        try:
            bot.load_extension('admincommands')
            await message.edit('```🟢 Successfully loaded cog: "admincommands.py"```')
            data = read_json("status")
            data["Admin Cog"] = False
            data["Admin Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Admin Cog"] = False
            data["Admin Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to load cog: "admincommands.py"```')
            await ctx.send(f'```css\n[{error}]```')
    elif arg == "misc" or arg == "Misc" or arg == "m" or arg == "M":
        time.sleep(1)
        try:
            bot.load_extension('misc')
            await message.edit('```🟢 Successfully loaded cog: "misc.py"```')
            data = read_json("status")
            data["Misc Cog"] = False
            data["Misc Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Misc Cog"] = False
            data["Misc Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to load cog: "misc.py"```')
            await ctx.send(f'```css\n[{error}]```')
    elif arg == "moderation" or arg == "Moderation" or arg == "Mod" or arg == "mod":
        time.sleep(1)
        try:
            bot.reload_extension('moderation')
            await message.edit('```🟢 Successfully loaded cog: "moderation.py"```')
            data = read_json("status")
            data["Moderation Cog"] = False
            data["Moderation Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Moderation Cog"] = False
            data["Moderation Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to load cog: "moderation.py"```')
            await ctx.send(f'```css\n[{error}]```')
    elif arg == "currency" or arg == "Currency" or arg == "cur" or arg == "Cur":
        time.sleep(1)
        try:
            bot.load_extension('currency')
            await message.edit('```🟢 Successfully loaded cog: "currency.py"```')
            data = read_json("status")
            data["Currency Cog"] = True
            data["Currency Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Currency Cog"] = False
            data["Currency Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to load cog: "currency.py"```')
            await ctx.send(f'```css\n[{error}]```')

#PENDING
@bot.command(aliases=["r", "R", "Reload", "RELOAD"])
@commands.is_owner()
async def reload(ctx, arg):
    message = await ctx.reply("```fix\nHold on... This might take a few seconds```", mention_author=True)
    if arg == "admincommands" or arg == "AdminCommands" or arg == "ac" or arg == "AC" or arg == "admin" or arg == "Admin" or arg == "ADMIN" or arg == "adminc" or arg == "Adminc":
        time.sleep(1)
        try:
            bot.reload_extension('admincommands')
            await message.edit('```🟢 Successfully reloaded cog: "admincommands.py"```')
            data = read_json("status")
            data["Admin Cog"] = False
            data["Admin Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Admin Cog"] = False
            data["Admin Cog Error"] = False
            write_json(data, "status")
            await message.edit('```🔴 Failed to reload cog: "admincommands.py"```')
            await ctx.send(f'```css\n[{error}]```')
    elif arg == "misc" or arg == "Misc" or arg == "m" or arg == "M":
        time.sleep(1)
        try:
            bot.reload_extension('misc')
            await message.edit('```🟢 Successfully reloaded cog: "misc.py"```')
            data = read_json("status")
            data["Misc Cog"] = False
            data["Misc Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Misc Cog"] = False
            data["Misc Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to reload cog: "misc.py"```')
            await ctx.send(f'```css\n[{error}]```')
    elif arg == "moderation" or arg == "Moderation" or arg == "Mod" or arg == "mod":
        time.sleep(1)
        try:
            bot.reload_extension('moderation')
            await message.edit('```🟢 Successfully reloaded cog: "moderation.py"```')
            data = read_json("status")
            data["Moderation Cog"] = False
            data["Moderation Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Moderation Cog"] = False
            data["Moderation Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to reload cog: "moderation.py"```')
            await ctx.send(f'```css\n[{error}]```')
    elif arg == "currency" or arg == "Currency" or arg == "cur" or arg == "Cur":
        time.sleep(1)
        try:
            bot.reload_extension('currency')
            await message.edit('```🟢 Successfully reloaded cog: "currency.py"```')
            data = read_json("status")
            data["Currency Cog"] = True
            data["Currency Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Currency Cog"] = False
            data["Currency Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to reload cog: "currency.py"```')
            await ctx.send(f'```css\n[{error}]```')

#PENDING
@bot.command(aliases=["u", "U", "Unload", "UNLOAD"])
@commands.is_owner()
async def unload(ctx, arg):
    message = await ctx.reply("```fix\nHold on... This might take a few seconds```", mention_author=True)
    if arg == "admincommands" or arg == "AdminCommands" or arg == "ac" or arg == "AC" or arg == "admin" or arg == "Admin" or arg == "ADMIN" or arg == "adminc" or arg == "Adminc":
        time.sleep(1)
        try:
            bot.unload_extension('admincommands')
            await message.edit('```🟢 Successfully unloaded cog: "admincommands.py"```')
            data = read_json("status")
            data["Admin Cog"] = False
            data["Admin Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Admin Cog"] = False
            data["Admin Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to unload cog: "admincommands.py"```')
            await ctx.send(f'```css\n[{error}]```')
    elif arg == "misc" or arg == "Misc" or arg == "m" or arg == "M":
        time.sleep(1)
        try:
            bot.unload_extension('misc')
            await message.edit('```🟢 Successfully unloaded cog: "misc.py"```')
            data = read_json("status")
            data["Misc Cog"] = False
            data["Misc Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Misc Cog"] = False
            data["Misc Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to unload cog: "misc.py"```')
            await ctx.send(f'```css\n[{error}]```')
    elif arg == "moderation" or arg == "Moderation" or arg == "Mod" or arg == "mod":
        time.sleep(1)
        try:
            bot.unload_extension('moderation')
            await message.edit('```🟢 Successfully unloaded cog: "moderation.py"```')
            data = read_json("status")
            data["Moderation Cog"] = False
            data["Moderation Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Moderation Cog"] = False
            data["Moderation Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to unload cog: "moderation.py"```')
            await ctx.send(f'```css\n[{error}]```')
    elif arg == "currency" or arg == "Currency" or arg == "cur" or arg == "Cur":
        time.sleep(1)
        try:
            bot.unload_extension('currency')
            await message.edit('```🟢 Successfully unloaded cog: "currency.py"```')
            data = read_json("status")
            data["Currency Cog"] = False
            data["Currency Cog Error"] = False
            write_json(data, "status")
        except Exception as error:
            file = open(efile, "a")
            file.write(f"{str(error)} - {ctx.author.id}")
            file.write("\n")
            file.close()
            data = read_json("status")
            data["Currency Cog"] = False
            data["Currency Cog Error"] = True
            write_json(data, "status")
            await message.edit('```🔴 Failed to unload cog: "currency.py"```')
            await ctx.send(f'```css\n[{error}]```')

@bot.command(aliases=["Change", "CHANGE", "c", "C"])
@commands.is_owner()
async def change(ctx):
    await ctx.send("```yaml\nTYPES: \n1 = Playing\n2 = Listening\n3 = Watching\n4 = Streaming\n5 = Competing\n\nSyntax: +exec bot.change_presence(status=discord.Status.{status}, activity=discord.Activity(name='{name}', type={type}))```")

@bot.command(aliases=["EXEC", "Exec", "e", "E"])
@commands.is_owner()
async def exec(ctx, *, command: str):
    try:
        command = command.replace("```", "")
        return await eval(command.strip())
    except Exception as e:
        await ctx.send(f"```diff\n- {str(e)}```")

@bot.event
async def on_guild_remove(guild):
    with open('serverdb.json', "r") as f:
        p = json.load(f)

    del p[str(guild.id)]

    with open('serverdb.json', "w") as f:
        json.dump(p, f, indent=4)

@bot.event
async def on_message(message):
    with open('serverdb.json', 'r') as f: sdb = json.load(f)

    col = db["currency"]
    a = []
    for x in col.find({}, {"_id": 0, "USER ID": 1}): a.append(x)
    if {"USER ID": message.author.id} not in a: col.insert_one({"USER ID": message.author.id, "USER": str(message.author), "Wallet": 1000, "Bank": 0, "Bank Limit": 10000})
    wallet = col.find_one({"USER ID": message.author.id}, {"_id": 0, "Wallet": 1})["Wallet"]
    bank = col.find_one({"USER ID": message.author.id}, {"_id": 0, "Bank": 1})["Bank"]
    bankl = col.find_one({"USER ID": message.author.id}, {"_id": 0, "Bank Limit": 1})["Bank Limit"]

    mention = f'<@!{bot.user.id}> prefix'
    oneof5 = random.randint(1, 5)
    coins = random.randint(1, 1000)

    if str(message.guild.id) not in sdb:
        await udb(str(message.guild.id), sdb)
        with open('serverdb.json', 'w') as f: json.dump(sdb, f, indent=4)
    await ctm(str(message.guild.id), sdb)
    with open('serverdb.json', 'w') as f: json.dump(sdb, f, indent=4)

    if oneof5 == 1:
        col.update_one({"USER ID": message.author.id, "Bank Limit": bankl}, {"$set": {"Bank Limit": bankl+coins}})

    if str(message.guild.id) in sdb: sp = sdb[str(message.guild.id)]["Prefix"]
    else: sp = default

    if message.content.lower() == mention: await message.channel.send(f"My prefix in this server is **`{sp}`**")
    elif message.content.startswith(f'{sp}') == True:
        if str(message.guild.id) not in sdb:
            await udb(str(message.guild.id), sdb)
            with open('serverdb.json', 'w') as f: json.dump(sdb, f, indent=4)
        await ctc(str(message.guild.id), sdb)
        with open('serverdb.json', 'w') as f: json.dump(sdb, f, indent=4)
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandError):
        file = open(efile, "a")
        file.write(f"{str(error)} - {ctx.author.id}\n")
        file.close()
    elif isinstance(error, commands.BadArgument):
        file = open(efile, "a")
        file.write(f"{str(error)} - {ctx.author.id}\n")
        file.close()
    elif isinstance(error, commands.ExtensionAlreadyLoaded):pass
    elif isinstance(error, commands.CommandInvokeError):
        file = open(efile, "a")
        file.write(f"Unknown Error - {ctx.author.id} | {ctx.message.id}\n")
        file.close()
    return

@bot.event
async def on_ready():
    global start_time
    start_time = datetime.utcnow()

    memberCount = len(set(bot.get_all_members()))
    data = read_json("status")

    bot.load_extension('misc')
    bot.load_extension('admincommands')
    bot.load_extension('moderation')
    bot.load_extension('currency')
    data["Bot Working"],data["Admin Cog"], data["Admin Cog Error"], data["Misc Cog"], data["Misc Cog Error"],data["Moderation Cog"], data["Moderation Cog Error"], data["Currency Cog"], data["Currency Cog Error"] = True, True, False,True, False,True, False, True, False
    write_json(data, "status")

    print(f"Logged in as {bot.user} (ID: {bot.user.id})\n------\nOwners: {bot.owner_ids}\n------\n{str(len(bot.guilds))} Servers Total | {memberCount} Users Total\n------\nAll cogs (admincommands.py, misc.py, moderation.py and currency.py) have been loaded")
    await bot.change_presence(status=discord.Status.online)

bot.run('ODY3MTQ4ODIzNTQ4OTE5ODA5.YPc5Rg.CT8E_IzkAM4eChQMZrhiUIOu-_A')
