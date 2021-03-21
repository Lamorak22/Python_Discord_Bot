#####################################
# Daniel Eberhart
# 3/21/2021
# yt-to-mp3.py
#
# This file contains the code that will have the bot
# join the discord voice channel and play the 
# selected soundbite.
#####################################

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
import youtube_dl
import os
import asyncio
import pafy
from dotenv import load_dotenv

class YoutubeToMp3(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.ffmpeg = os.getenv('FFMPEG_FILEPATH')
        self.ytdlfilepath = os.getenv('YTMP3_FILEPATH')

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loaded YouTube to Mp3 Cog")

    #####################################
    # Function: ytmp3
    #
    # Purpose: Play the audio from a youtube video
    #   to the discord voice chat
    #
    # Input: Invoked by '=ytmp3 {youtube link}'
    #
    # Output: The bot will download the youtube audio,
    #   join the voice channel, play the audio,
    #   and then leave.
    #####################################
    @commands.command()
    async def ytmp3(self, ctx, url: str):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.ytdlfilepath}\\song.mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }   
        
        async def download_video_mp3():    
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'{url}'])

            voice = get(self.bot.voice_clients, guild=ctx.guild)
            channel = ctx.message.author.voice.channel

            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
                print(f"Bot has connected to {channel}\n")

            voice.play(discord.FFmpegPCMAudio(executable=self.ffmpeg,source=f"{self.ytdlfilepath}\\song.mp3"))
            
            while voice.is_playing():
                await asyncio.sleep(0.1) #Don't disconnect until mp3 is done playing

            await voice.disconnect() 

            os.remove(f"{self.ytdlfilepath}\\song.mp3")# Delete file

        # Checking video length
        video = pafy.new(url)
        vidlength = video.length

        if discord.utils.get(ctx.message.author.roles, name="admin") or vidlength <= 45:
            await download_video_mp3()
        
        else:
            await ctx.send("Only admins can play videos over 45 seconds.")
            await ctx.send("If you are an admin, type 'override' to download anyway.")
            msg = await self.bot.wait_for('message', timeout=10.0)

            if msg.content == "override" and discord.utils.get(msg.author.roles, name="admin"):
                await ctx.send(f"Override for videolength > {vidlength} seconds initiated by admin: {msg.author}")
                await download_video_mp3()
            else:
                await ctx.send("Override denied. You aren't an admin.")
def setup(bot):
    bot.add_cog(YoutubeToMp3(bot))
