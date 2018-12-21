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
VOL_LOUD = 75
VOL_MID = 50
VOL_SOFT = 25

LOGGER = getLogger(__name__)


class SonosControl(MycroftSkill):
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(SonosControl, self).__init__(name="SonosControl")
        # Initialize working variables used within the skill.
        self.need_speakers = True

    # Now get the sonos info.
    # self.members all the speakers that we need to talk to
    # self.volume the current volume of each speaker
    def initialize(self):
        coord = self.findspeakers()
        if coord == "":
            LOGGER.debug("Did not find any Sonos speakers")
            self.speak_dialog("sonos.nospeakers")
            return
        LOGGER.debug("Found Speakers")
        self.need_speakers = False
        self.coordinator = coord  # the coordinator obj

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
        utt = message.data.get('utterance', '')
        LOGGER.debug("utterance is: {}".format(utt))
        if 'loud' in utt.split():
            s = self.set_vol(VOL_LOUD, 0, True)
        elif 'middle' in utt.split():
            s = self.set_vol(VOL_MID, 0, True)
        else:
            s = self.set_vol(10, 0, False)
        if s:
            self.speak_dialog("sonos.volume.up")
        else:
            self.speak_dialog("no_volume_change")

    # Lower the volume of the speakers
    @intent_handler(IntentBuilder("sonosvolumedownintent").require("Sonos").require("Volume").require("Decrease"))
    def handle_sonos_volume_down_intent(self, message):
        utt = message.data.get('utterance', '')
        LOGGER.debug("utterance is: {}".format(utt))
        if 'soft' in utt.split():
            s = self.set_vol(VOL_SOFT, 0, True)
        else:
            s = self.set_vol(0, 10, False)
        if s:
            self.speak_dialog("sonos.volume.down")
        else:
            self.speak_dialog("no_volume_change")

    # Get the title and artist and say to user
    @intent_handler(IntentBuilder("songnameintent").require("Sonos").require("query").require("song"))
    def handle_song_name_intent(self, message):
        track = self.coordinator.get_current_track_info()
        title = track.get('title')
        artist = track.get('artist')
        album = track.get('album')
        self.speak_dialog('song_name', {'title': title, 'album': album, 'artist': artist})

    # Find the speakers return the controler
    def findspeakers(self):
        speakers = soco.discover()
        if speakers == None:
            return ""
        if len(speakers) == 0:
            return ""
        members = {}
        vol = {}
        for spk in speakers:
            n = spk._player_name
            members[n] = spk
            vol[n] = spk.volume

        self.members = members
        self.volume = vol
        group = spk.group
        coordinator = group.coordinator
        return coordinator

    def set_vol(self, up=0, down=0, fixed=False):
        vol = self.volume
        status = True
        for sp in self.members:
            v = vol[sp]
            v = vol_check(v + up - down)
            if fixed:
                v = vol_check(up)
            else:
                vol[sp] = v
            # Save new volume
            self.volume[sp] = v
            try:
                self.members[sp].volume = v

            except Exception as e:
                LOGGER.debug(e.message)
                status = False
        return status

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    def stop(self):
        pass


# Check that the volume value is in range
def vol_check(v):
    if v <= 5:
        v = 5
    if v >= 99:
        v = 99
    return v


def create_skill():
    return SonosControl()
