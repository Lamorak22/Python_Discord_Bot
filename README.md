# Python_Discord_Bot

This is a fun discord bot I made with discord.py for my friends and I to use on our server.

As of right now there are only a few commands.

mp3, tts, and ytmp3

mp3: mp3 is called by typing __=mp3 <soundbite name>__
  These soundbites are in a folder and the path is hidden in a .env file
  
tts: tts is called by typing __=tts <tts message>__
  Discord already has a default tts, but I did not know that before making this.
  Regardless, the tts is different because the bot joins the voice channel to say its message.
  
ytmp3: ytmp3 is called by typing __=ytmp3 <youtube url>__
  This command will download a YouTube video's audio and then play it in the voice channel.
  If a video is over 45 seconds long, it will not be played. However, an admin can override this.
