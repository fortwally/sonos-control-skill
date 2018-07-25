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



