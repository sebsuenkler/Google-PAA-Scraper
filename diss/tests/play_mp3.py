import soundcard as sc
import soundfile as sf
import numpy
import time


# get a list of all speakers:
speakers = sc.all_speakers()
# get the current default speaker on your system:
default_speaker = sc.default_speaker()
# get a list of all microphones:
mics = sc.all_microphones()
# get the current default microphone on your system:
default_mic = sc.default_microphone()

# fuzzy-search to get the same results:
one_speaker = sc.get_speaker('Line')
one_mic = sc.get_microphone('Line')

import pygame
import pygame._sdl2 as sdl2
from pygame import mixer

mixer.init() # Initialize the mixer, this will allow the next command to work
print(sdl2.audio.get_audio_device_names(False)) # Returns playback devices, Boolean value determines whether they are Input or Output devices.
mixer.quit() # Quit the mixer as it's initialized on your main playback device

mixer.init(devicename = 'Line (2- AG06/AG03)') # Initialize it with the correct device
mixer.music.load("harry.mp3") # Load the mp3
mixer.music.play() # Play it

while mixer.music.get_busy():  # wait for music to finish playing

    OUTPUT_FILE_NAME = "out.wav"    # file name.
    SAMPLE_RATE = 48000              # [Hz]. sampling rate.
    RECORD_SEC = 5                  # [sec]. duration recording audio.

    with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
        # record audio with loopback from default speaker.
        data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)

        one_speaker.play(data/numpy.max(data), samplerate=48000)

        # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
        sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

    time.sleep(1)
