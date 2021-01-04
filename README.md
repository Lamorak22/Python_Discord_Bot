# Python_Discord_Bot

This is a fun discord bot I made with discord.py for my friends and I to use on our server.

As of right now there are only a few commands.  

## mp3: 
mp3 is called by typing `=mp3 <soundbite name>`  
  These soundbites are in a folder and the path is hidden in a .env file  
  
## tts:   
tts is called by typing `=tts <tts message>`  
  Discord already has a default tts, but I did not know that before making this.  
  Regardless, the tts is different because the bot joins the voice channel to say its message.  
  
## ytmp3: 
ytmp3 is called by typing `=ytmp3 <youtube url>`  
  This command will download a YouTube video's audio and then play it in the voice channel.  
  If a video is over 45 seconds long, it will not be played. However, an admin can override this.  
