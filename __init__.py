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
from mycroft.util.log import getLogger
import soco

__author__ = 'fortwally'

LOGGER = getLogger(__name__)


class SonosControl(MycroftSkill):
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(SonosControl, self).__init__(name="SonosControl")
        # Initialize working variables used within the skill.
        self.need_speakers = True

    # Now get the sonos info.
    def initialize(self):
        coord = findspeakers()
        if coord == "":
            LOGGER.debug("Did not find any Sonos speakers")
            return
        LOGGER.debug("Found Speakers")
        self.need_speakers = False
        self.coordinator = coord  # the coordinator obj
        ip = self.coordinator.ip_address
        self.settings['coordinator_ip'] = ip
        LOGGER.debug('Coordinator IP is {}'.format(ip))
        self.volume = self.coordinator.volume
        

    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.

    # Continue playing whatever was playing before play was pasued.
    @intent_handler(IntentBuilder("sonosplayintent").require("Sonos").require("play"))
    def handle_sonos_play_intent(self, message):
        if self.need_speakers:
            self.speak_dialog("sonos.nospeakers")
            return
        try:
            LOGGER.debug("In Play Intent")
            self.coordinator.play()
            self.speak_dialog("sonos.play")
        except Exception as e:
            LOGGER.debug(e.message)
            pass

    # Pause whatever is playing.
    @intent_handler(IntentBuilder("sonospauseintent").require("Sonos").require("pause"))
    def handle_sonos_pause_intent(self, message):
        if self.need_speakers:
            self.speak_dialog("sonos.nospeakers")
            return
        try:
            LOGGER.debug("In Pause Intent")
            self.coordinator.pause()
            self.speak_dialog("sonos.pause")
        except Exception as e:
            LOGGER.debug(e.message)
            # self.buildspeakers()
            pass

    # Skip to the next track
    @intent_handler(IntentBuilder("sonosskipintent").require("Sonos").require("skip"))
    def handle_sonos_skip_intent(self, message):
        try:
            LOGGER.debug("In skip Intent")
            self.coordinator.next()
            self.speak_dialog("sonos.skip")
        except Exception as e:
            LOGGER.debug(e.message)
            self.speak("Can not skip what is playing")

    # Raise the volume of the speakers
    @intent_handler(IntentBuilder("sonosvolumeupintent").require("Sonos").require("Volume").require("Increase"))
    def handle_sonos_volume_up_intent(self, message):
        utt = message.data.get('utterance','')
        LOGGER.debug("utterance is: {}".format(utt))
        if 'loud' in utt.split():
            v = 75
        v = vol_check(self.volume + 10)
        self.volume = v
        try:
            LOGGER.debug("In Volume up Intent")
            self.coordinator.volume = v
            self.speak_dialog("sonos.volume.up")
        except Exception as e:
            LOGGER.debug(e.message)
            self.speak_dialog("no_volume_change")

    # Lower the volume of the speakers
    @intent_handler(IntentBuilder("sonosvolumedownintent").require("Sonos").require("Volume").require("Decrease"))
    def handle_sonos_volume_down_intent(self, message):
        utt = message.data.get('utterance','')
        LOGGER.debug("utterance is: {}".format(utt))
        if 'soft' in utt.split():
            v = 25
        v = vol_check(self.volume - 10)
        self.volume = v
        try:
            LOGGER.debug("In Volume down Intent")
            self.coordinator.volume = v
            self.speak_dialog("sonos.volume.down")
        except Exception as e:
            LOGGER.debug(e.message)
            self.speak_dialog("no_volume_change")

    # Get the title and artist and say to user
    @intent_handler(IntentBuilder("songnameintent").require("Sonos").require("query").require("song"))
    def handle_song_name_intent(self, message):
        track = self.coordinator.get_current_track_info()
        title = track.get('title')
        artist = track.get('artist')
        album = track.get('album')
        self.speak_dialog('song_name', {'title': title, 'album': album, 'artist': artist})

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    def stop(self):
        pass

#    def buildspeakers(self):
#        spk = findspeakers()
#        if len(spk) == 0:
#            LOGGER.debug("Did not find any Sonos speakers")
#            return
#        LOGGER.debug("Found Speakers")
#        self.need_speakers = 0 # 1 = no speakers
#        self.coordinator = spk # the coordinator obj
#        self.settings['coordinator_ip']=self.coordinator.ip_address
#        LOGGER.debug('Coordinator IP is {}'.format(self.ip_address))
#        self.volume = self.coordinator.volume

# Check that the volume value is in range
def vol_check(v):
    if v <= 10:
        v = 10
    if v >= 99:
        v=99
    return v

# Find the speakers return the controler
def findspeakers():
    speakers = soco.discover()
    if len(speakers) == 0:
        return ""
    spk = speakers.pop()
    group = spk.group
    coordinator = group.coordinator
    return coordinator


def create_skill():
    return SonosControl()

