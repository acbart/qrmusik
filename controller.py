import sys
import time
from os import path
import pygame

import process
import settings
import util


"""

Main controller, runs in an infinite loop, reads and acts on QR codes

Data in QR codes is defined as follows:
    * music vol <integer> : set music volume to given percentage
    * music play <file name> : play given music file, from music root

Autostart: 'crontab -e', then add line
@reboot cd /home/pi/src/qrmusik && python -u controller.py 2>&1 >> /home/pi/tmp/qrmusik.log.txt &

"""


# image processor instance 
proc = process.Processor(settings.TEMP_IMAGE_FILE)

# initialize music mixer
pygame.mixer.init()

# set default volume
util.set_volume(settings.DEFAULT_VOLUME)

# currently playing file
current_music = None

# current volume setting
current_volume = None

# run the controller in an infinite loop
while True:
    # sleep a bit
    time.sleep(settings.CAPTURE_SLEEP)

    # capture an image
    qr_found = proc.capture()

    if qr_found:
        # process event, catch any error
        data = proc.qr.data.decode('utf-8')
        print("QR code found, data is " + data)

        try:

            words = data.split()

            if len(words) == 0:
                print("No data found")
                continue

            if words[0] == "music":

                if len(words) < 2:
                    print("Found class 'music' but no command")
                    continue

                if words[1] == "vol":

                    if len(words) < 3:
                        print("Found command 'music vol' but no value")
                        continue

                    # get volume value
                    value = int(words[2])

                    # do nothing if current volume is the same
                    if value == current_volume:
                        continue

                    print("Setting volume to :" + str(value))
                    current_volume = value
                    util.set_volume(value)
                        
                elif words[1] == "play":

                    if len(words) < 3:
                        print("Found command 'music play' but no value")
                        continue

                    # file name may contain spaces, re-assemble it
                    music_file = path.join(settings.MUSIC_ROOT, " ".join(words[2:]))

                    if not path.exists(music_file):
                        print("File not found: " + music_file)

                    # if playing the file already, do nothing
                    if pygame.mixer.music.get_busy() and current_music == music_file:
                        continue

                    # play
                    print("Playing " + music_file)
                    current_music = music_file
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.play()

        except Exception as e:
            print("")
            print("Exception: " + str(e))
            print("Command was: " + str(e))
            continue
            
