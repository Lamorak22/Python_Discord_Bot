# main.py

import logging
import random
import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
import command_desc

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set command prefix and remove default help command
bot = commands.Bot(command_prefix='=')
bot.remove_command('help') 

# load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COGS = os.getenv('COGS')

# Load descriptions for help command
mp3_desc = command_desc.mp3_description()
ytmp3_desc = command_desc.ytmp3_description()
tts_desc = command_desc.tts_description()


@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name)
    print("Setting activity")
    activity = discord.Activity(name="Type =help for help", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)


# Forces the bot to disconnect from voice
@bot.command(aliases=['stop', 's'])
#@commands.has_role('admin')
async def stopmp3(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect(force=True)
    print("Forced Voice Disconnect by user:", ctx.author)

# Custom help command
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


# Basic events/commands
@bot.event
async def on_member_join(member):
    print(f'{member} has joined the server')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left the server')

@bot.command()
@commands.has_role('admin')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

# Load all cogs in
for filename in os.listdir(COGS):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)