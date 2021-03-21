#####################################
# Daniel Eberhart
# 3/21/2021
# soundbites.py
#
# This file contains the code that will have the bot
# join the discord voice channel and play the 
# selected soundbite.
#####################################

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
import os
import asyncio
from dotenv import load_dotenv

class Soundbites(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.ffmpeg = os.getenv('FFMPEG_FILEPATH')
        self.mp3filepath = os.getenv('MP3_FILEPATH')
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded Soundbites Cog")


    #####################################
    # Function: mp3
    #
    # Purpose: Play a soundbite to the discord voice chat
    #
    # Input: Invoked by '== {soundbite}'
    #
    # Output: The bot will join the voice channel, play
    #   the selected soundbite, and then leave.
    #####################################
    @commands.command(aliases=['='])
    async def mp3(self, ctx, *, src: str):
        try:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            channel = ctx.message.author.voice.channel

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                print(f"Bot has connected to {channel}\n")
            
            voice.play(discord.FFmpegPCMAudio(executable=self.ffmpeg,source=f"{self.mp3filepath}\\{src}.mp3"))

            while voice.is_playing():
                await asyncio.sleep(0.1)

            await voice.disconnect()# Disconnect after audio is done playing

        except:
            await ctx.send(f"{ctx.author} you must be in a voice channel to call this command.")

def setup(bot):
    bot.add_cog(Soundbites(bot))