# command_desc.py
# This file contains the strings that are shown when the help
# command is called. I put this into a python file rather
# than a text file so that it would be easier to retrieve
# the names of the .mp3 files. This way they would not
# have to be updated manually.

import os
from dotenv import load_dotenv
load_dotenv()
mp3_filepath = os.getenv('MP3_FILEPATH')
def mp3_description():
    soundbytes = ""
    for files in os.listdir(mp3_filepath):
        soundbytes = soundbytes + files[:-4] + "\n"
        
    mp3_desc = f"""
Invoked by "== <soundbyte>"
The Bot will join the voice call and play the selected soundbyte.
Selectable soundbytes:
{soundbytes}
"""
    return mp3_desc

def ytmp3_description():
    ytmp3_desc = f"""
Invoked by "=ytmp3 <YouTube URL>"
The Bot will download the YouTube URL audio as an mp3 and play it.
"""
    return ytmp3_desc

def tts_description():
    tts_desc = f"""
Invoked by "=tts <message>"
The Bot will play the message with text to speech.
"""
    return tts_desc
