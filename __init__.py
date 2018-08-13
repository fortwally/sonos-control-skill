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

# Below is the list of outside modules used in the skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.
# Added soco to requirments.txt
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler, intent_handler
from mycroft.util.log import getLogger, LOG
import soco

__author__ = 'fortwally'

LOGGER = getLogger(__name__)

class SonosControl(MycroftSkill):
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(SonosControl, self).__init__(name="SonosControl")

        # Initialize working variables used within the skill.
        self.count = 0
        work = findspeakers()
        LOG.debug("Found Speakers {}".format(work[0]))
        self.need_speakers = work[0] # 1 no speakers
        self.coordinator = work[1] # the coordinator
        self.ip_address = self.coordinator.ip_address # python object
        self.settings['coordinator_ip']=self.ip_address
        LOG.debug('Coordinator IP is {}'.format(self.ip_address))
        self.volume = coorinator.volume

    #@intent_file_handler('control.sonos.intent')
    #def handle_control_sonos(self, message):
    #    self.speak_dialog('control.sonos')


    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'

    # Continue playing whatever was playing before play was pasued.
    @intent_handler(IntentBuilder("sonosplayintent").require("sonos").require("play"))
    def handle_sonos_play_intent(self, message):
        if self.need_speakers:
            self.speak_dialog("sonos.nospeakers")
            return
        try:
            LOG.debug("In Play Intent")
            play(self.coordinator)
            self.speak_dialog("sonos.play")
        except:
            needspeakers()

    # Pause whatever is playing.
    @intent_handler(IntentBuilder("sonospauseintent").require("sonos").require("pause"))
    def handle_sonos_pause_intent(self, message):
        if self.need_speakers:
            self.speak_dialog("sonos.nospeakers") 
            return
        try:
            LOG.debug("In Pause Intent")
            self.coordinator.pause()
            self.speak_dialog("sonos.pause")
        except:
            needspeakers()


    # Handle this the same as a pause
    @intent_handler(IntentBuilder("sonosstopintent").require("sonos").require("stop"))
    def handle_sonos_stop_intent(self, message):
        self.coordinator.pause()
        self.speak_dialog("sonos.pause")

    # Skip to the next track
    @intent_handler(IntentBuilder("sonosskipintent").require("sonos").require("skip"))
    def handle_sonos_skip_intent(self, message):
        try:
            self.coordinator.next()
            self.speak_dialog("sonos.skip")
        except Exception as e:
            LOG.debug(e.message)
            self.speak("Can not skip what is playing")


    # Raise the volume of the speakers
    @intent_handler(IntentBuilder("sonosvolumeupintent").require("sonos").require("volume").require("up"))
    def handle_sonos_volume_up_intent(self, message):
        v = self.volume + 10
        if v => 99:
            v = 99
        try:
            self.coordinator.volume() = v
            self.speak_dialog("sonos.volume.up")
        except Exception as e:
            LOG.debug(e.message)
            self.speak("Can not change volume")

    # Lower the volume of the speakers
    @intent_handler(IntentBuilder("sonosvolumedownintent").require("sonos").require("volume").require("down"))
    def handle_sonos_volume_down_intent(self, message):
        v = self.volume - 10
        if v <= 10:
            v = 10
        try:
            self.coordinator.volume() = v
            self.speak_dialog("sonos.volume.down")
        except Exception as e:
            LOG.debug(e.message)
            self.speak("Can not change volume")

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    def stop(self):
        pass

    def needSpeakers(self):
        self.speak_dialog("sonos.findspeakers")
        try:
            coordinator = rescan(self.ip_address)
        except:
            coorinator = rescan(self.settings.get('coordinatr_ip'))

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

# Continue playing whatever was playing
def play(coordinator):
    coordinator.play()


        

def create_skill():
    return SonosControl()

