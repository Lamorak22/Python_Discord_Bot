#####################################
# Daniel Eberhart
# 3/21/2021
# tts.py
#
# This file contains the code that will have the bot
# join the discord voice channel and play the
# text-to-speech.
#####################################

from gtts import gTTS
import asyncio
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from dotenv import load_dotenv
import os

class TextToSpeech(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.ffmpeg = os.getenv('FFMPEG_FILEPATH')
        self.tts_filepath = os.getenv('TTS_FILEPATH')

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded TTS Cog")


    #####################################
    # Function: tts
    #
    # Purpose: Play message over text-to-speech
    #
    # Input: Invoked by '=tts {message}'
    #
    # Output: The bot will join the voice channel, play
    #   the text-to-speech, and then leave.
    #####################################
    @commands.command()
    async def tts(self, ctx, *, message: str):
        try:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            channel = ctx.message.author.voice.channel

            # Set up text to speech
            tts = gTTS(text=message, lang='en') # convert message
            tts.save(f"{self.tts_filepath}\\temp.mp3") # download message as .mp3

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                print(f"Bot has connected to {channel}\n")
            
            voice.play(discord.FFmpegPCMAudio(executable=self.ffmpeg, source=f"{self.tts_filepath}\\temp.mp3"))

            while voice.is_playing():
                await asyncio.sleep(0.1)

            await voice.disconnect()#Disconnect after audio is done playing

            os.remove(f"{self.tts_filepath}\\temp.mp3") # Delete mp3
        except:
            await ctx.send(f"{ctx.author} you must be in a voice channel to call this command.")
        

def setup(bot):
    bot.add_cog(TextToSpeech(bot))