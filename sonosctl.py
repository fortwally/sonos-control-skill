"""
The MIT License (MIT)   

Copyright (c) 2018 Wally Fort

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# Control Sonos speakers from Mycroft
import soco
# Find the speakers return the controler
def findspeakers():
    speakers = soco.discover()
    if len(speakers) == 0 :
        return [1, "no.sonos.speakers"]
    spk = speakers.pop()
    group = spk.group
    coordinator = group.coordinator
    return [0, coordinator]

# Called if coordinator object is not valid
# try using old IP address
def rescan(ip):
    coordinator = soco.SoCo(ip)
    return coordinator

# Will see if can pass object around.
#Start continue playing whatever was playing
def play(coordinator):
    coordinator.play()

#Pause play
def pause(coordinator):
    coordinator.pause()



