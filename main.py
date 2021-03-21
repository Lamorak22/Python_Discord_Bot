#####################################
# Daniel Eberhart
# 3/21/2021
# main.py
#
# This is a Python Discord bot that I created for my friends and I to use.
# The current functions of the bot mainly concern the discord voice chat.
# The three commands allow a user to play an MP3 sound bite, download and
# play the MP3 audio of any youtube video, and have the bot use text-to-speech
# to say the message they typed in.
#####################################

import logging
import random
import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
import command_desc

# Set up logging to the console
logging.basicConfig(level=logging.INFO)

# Set command prefix and remove default help command
bot = commands.Bot(command_prefix='=')
bot.remove_command('help') 

# load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COGS = os.getenv('COGS')

# Load descriptions for help command from command_desc module
mp3_desc = command_desc.mp3_description()
ytmp3_desc = command_desc.ytmp3_description()
tts_desc = command_desc.tts_description()

#####################################
# Function: on_ready
# Purpose: When the bot is started, this code will run
# Output: Bots discord activity is set
#####################################
@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    print("Setting activity")
    activity = discord.Activity(name="Type =help for help", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)


#####################################
# Function: stopmp3
# Purpose: Force bot to disconnect from voice channel
# Input: Invoked by '=stopmp3'
# Output: Bot disconnects from channel
#####################################
@bot.command(aliases=['stop', 's'])
@commands.has_role('admin')
async def stopmp3(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect(force=True)
    print("Forced Voice Disconnect by user:", ctx.author)
    await ctx.send("Forced Voice Disconnect by user:", ctx.author)

#####################################
# Function: help
# Purpose: Displays help command window in Discord chat
# Input: Invoked by '=help'
# Output: Help page is displayed in the Discord chat
#####################################
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title="Lamorak's Bot's Help Page",
        description="This page shows the Bot's commands and explains how to use them"
    )
    embed.set_author(name="Author: Lamorak",)
    embed.add_field(name="mp3", value=mp3_desc, inline=False)
    embed.add_field(name="ytmp3", value=ytmp3_desc, inline=False)
    embed.add_field(name="tts", value=tts_desc, inline=False)

    await ctx.send(embed=embed)


#####################################
# Function: on_member_join
# Purpose: Shows when a member joins the server
#####################################
@bot.event
async def on_member_join(member):
    channel = member.channel
    await channel.send(f'{member} has joined the server')
    print(f'{member} has joined the server')

#####################################
# Function: on_member_remove
# Purpose: Shows when a member joins the server
#####################################
@bot.event
async def on_member_remove(member):
    channel = member.channel
    await channel.send(f'{member} has left the server')
    print(f'{member} has left the server')

#####################################
# Function: clear
# Purpose: Clears the specified amount of messages from the chat
#####################################
@bot.command()
@commands.has_role('admin')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

#####################################
# Function: load
# Purpose: Loads a cog if they were not loaded in by default
#####################################
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

#####################################
# Function: unload
# Purpose: Unloads a cog
#####################################
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

# Load all cogs in
for filename in os.listdir(COGS):
    print(filename)
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)