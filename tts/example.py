from pygame import mixer

import pygame._sdl2 as sdl2
import time

mixer.init() # Initialize the mixer, this will allow the next command to work
print(sdl2.audio.get_audio_device_names(True)) # Returns playback devices, Boolean value determines whether they are Input or Output devices.
mixer.quit() # Quit the mixer as it's initialized on your main playback device

mixer.init(devicename = 'Line (2- AG06/AG03)') # Initialize it with the correct device
mixer.music.load("cat.mp3") # Load the mp3
mixer.music.play() # Play it

while mixer.music.get_busy():  # wait for music to finish playing
    time.sleep(1)
