# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.
# Added soco to requirments.txt
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import LOG
import sonosctl as SC

__author__ = 'fortwally'

LOGGER = getLogger(__name__)

class SonosControl(MycroftSkill):
    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(SonosControl, self).__init__(name="SonosControl")

        # Initialize working variables used within the skill.
        self.count = 0
        work = SC.findspeakers()
        LOGGER.debug("Found Speakers {}".format(word[0]))
        self.need_speakers = work[0] # 1 no speakers
        self.coordinator = work[1] # the coordinator
        self.ip_address = self.coordinator.ip_address # python object
        self.settings['coordinator_ip']=self.ip_address

    @intent_file_handler('control.sonos.intent')
    def handle_control_sonos(self, message):
        self.speak_dialog('control.sonos')


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
    @intent_handler(IntentBuilder("").require("Sonos").require("Play"))
    def handle_sonos_play_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        if self.need_speakers:
            self.speak_dialog("No speakers found")
            return
        try:
            SC.play(self.coordinator)
        except:
            needspeakers()

    @intent_handler(IntentBuilder("").require("Sonos").require("pause"))
    def handle_sonos_pause_intent(self, message):
        if self.need_speakers:
            self.speak_dialog("No speakers found") 
            return
        try:
            SC.pause(self.coordinator)
        except:
            needspeakers()

    def needSpeakers(self)
        self.speak_dialog("need to find speakers")
        try:
            coordinator = SC.rescan(self.ip_address)
        except:
            coorinator = SC.rescan(self.settings.get('coordinatr_ip')

    @intent_handler(IntentBuilder("").require("Sonos").require("stop")
    def handle_sonos_stop_intent(self, message)
        SC.pause(SC.coordinator)


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    def stop(self, message)
        pass

        

def create_skill():
    return SonosControl()

